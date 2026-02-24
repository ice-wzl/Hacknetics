# Web Reconnaissance

## HTTP Headers Reference

### Request Headers (Useful for Recon)

| Header | Description |
|--------|-------------|
| `Host` | Target hostname - useful for vhost discovery |
| `User-Agent` | Client identifier - spoofable to bypass restrictions |
| `Cookie` | Session tokens, auth data |
| `Authorization` | Basic/Bearer tokens |
| `Referer` | Previous page - spoofable for access bypasses |
| `X-Forwarded-For` | Client IP (via proxy) - spoofable for IP bypasses |

### Response Headers (Look For)

| Header | Description |
|--------|-------------|
| `Server` | Web server software & version |
| `X-Powered-By` | Backend technology (PHP, ASP.NET, Express) |
| `X-Redirect-By` | CMS identification (WordPress, Drupal) |
| `Set-Cookie` | Session handling, flags (Secure, HttpOnly) |
| `Content-Type` | Response type and encoding |
| `WWW-Authenticate` | Auth mechanism required |

### Security Headers (Missing = Potential Issue)

| Header | Description |
|--------|-------------|
| `Content-Security-Policy` | XSS prevention - script sources |
| `X-Frame-Options` | Clickjacking protection |
| `Strict-Transport-Security` | HTTPS enforcement (HSTS) |
| `X-Content-Type-Options` | Prevent MIME sniffing |
| `Referrer-Policy` | Control referrer information |
| `Permissions-Policy` | Feature restrictions |

---

## Web Fingerprinting

### Identify Server & Tech Stack (curl)

```bash
curl -I http://TARGET
curl -I https://TARGET

# Follow redirects
curl -IL http://TARGET
```

Look for:
- `Server:` header (e.g., Apache/2.4.41, nginx/1.18.0)
- `X-Powered-By:` header (e.g., PHP/7.4, Express)
- `X-Redirect-By:` header (e.g., WordPress)

### whatweb (tech stack)

```bash
# Single URL
whatweb http://TARGET

# Single URL, no errors
whatweb --no-errors http://TARGET

# Range (e.g. /24)
whatweb --no-errors 10.10.10.0/24
```

Reports server, CMS, frameworks, PHP/version, cookies, redirects. Useful to confirm tech and redirect chains (e.g. to installer or login).

---

### WAF Detection (wafw00f)

```bash
# Install
pip3 install git+https://github.com/EnableSecurity/wafw00f

# Detect WAF
wafw00f TARGET
```

---

### Nikto Fingerprinting

```bash
# Install
sudo apt update && sudo apt install -y perl
git clone https://github.com/sullo/nikto
cd nikto/program && chmod +x ./nikto.pl

# Fingerprint only (no vuln scan)
nikto -h TARGET -Tuning b
```

---

## robots.txt Analysis

```bash
curl http://TARGET/robots.txt
```

### Key Directives

| Directive | Description |
|-----------|-------------|
| `Disallow:` | Paths the bot shouldn't crawl (interesting for recon!) |
| `Allow:` | Explicitly permitted paths |
| `Sitemap:` | URL to sitemap.xml |
| `Crawl-delay:` | Seconds between requests |

**Recon Value**: Disallowed paths often reveal admin panels, backup directories, or sensitive endpoints.

---

## Exposed .git Directory

If a `.git` directory is accessible, dump and extract for source code, credentials, and history.

### Detection

```bash
# Check for exposed .git
curl -s http://TARGET/.git/HEAD
# Valid response: ref: refs/heads/master

# Nmap detection
nmap -sC -sV TARGET
# http-git: 10.129.x.x:80/.git/
#   Git repository found!
```

### Dumping with git-dumper

```bash
# Install
pip3 install git-dumper

# Or use GitTools
git clone https://github.com/internetwache/GitTools.git

# Dump repository
./GitTools/Dumper/gitdumper.sh http://TARGET/.git/ ./git-dump

# Extract all commits
./GitTools/Extractor/extractor.sh ./git-dump ./extracted
```

**Alternative: arthaud/git-dumper (Python)** — Dumps and extracts in one step; often works when GitTools fails (e.g. incomplete packs):

```bash
git clone https://github.com/arthaud/git-dumper.git
python3 git_dumper.py http://TARGET/.git /tmp/out
# Files appear in /tmp/out; then check git diff --cached for staged secrets
```

### Manual Enumeration

```bash
# List commits
cd extracted/0-*
git log --oneline

# View specific commit
git show COMMIT_HASH

# Search for secrets
grep -r "password" .
grep -r "secret" .
grep -r "api_key" .
grep -r "@" . | grep -i mail  # Find email addresses

# Staged but uncommitted changes (passwords in test fixtures, config)
git diff --cached
# Without --cached only unstaged changes are shown
```

### Common Findings

| File | Content |
|------|---------|
| `settings.php` | Database credentials |
| `.env` | Environment variables, API keys |
| `config/*.json` | Application configuration |
| `wp-config.php` | WordPress DB creds |
| `.htpasswd` | HTTP basic auth hashes |

### Example: Backdrop/Drupal settings.php

```bash
# Parse settings.php for DB creds
cat settings.php | grep -Ev "^//|\*"

# Output format:
$database = 'mysql://root:BackDropJ2024DS2024@127.0.0.1/backdrop';
```

---

## .well-known URIs

```bash
# Security contacts
curl http://TARGET/.well-known/security.txt

# OpenID Connect config (OAuth endpoints)
curl http://TARGET/.well-known/openid-configuration

# Password change URL
curl http://TARGET/.well-known/change-password
```

### Useful .well-known URIs

| URI | Description |
|-----|-------------|
| `security.txt` | Security contact info |
| `openid-configuration` | OAuth2/OIDC endpoints, supported scopes |
| `assetlinks.json` | Android app asset links |
| `mta-sts.txt` | Email MTA-STS policy |

Full list: https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml

---

## Google Dorking

### Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `site:` | Limit to domain | `site:example.com` |
| `inurl:` | Term in URL | `inurl:admin` |
| `intitle:` | Term in page title | `intitle:"index of"` |
| `filetype:` | Specific file type | `filetype:pdf` |
| `ext:` | File extension | `ext:conf` |
| `intext:` | Term in page body | `intext:password` |
| `cache:` | Cached version | `cache:example.com` |
| `link:` | Pages linking to URL | `link:example.com` |

### Common Dorks

```
# Login pages
site:TARGET inurl:login
site:TARGET (inurl:login OR inurl:admin)

# Exposed files
site:TARGET filetype:pdf
site:TARGET (filetype:xls OR filetype:docx)
site:TARGET filetype:sql

# Config files
site:TARGET inurl:config.php
site:TARGET (ext:conf OR ext:cnf OR ext:ini)
site:TARGET ext:env

# Backups
site:TARGET inurl:backup
site:TARGET (ext:bak OR ext:old OR ext:backup)

# Directory listings
site:TARGET intitle:"index of"

# Passwords/secrets
site:TARGET intext:password filetype:txt
site:TARGET intext:api_key
```

### Google Hacking Database

https://www.exploit-db.com/google-hacking-database

---

## Wayback Machine

### Web Interface

https://web.archive.org/

Enter URL to view historical snapshots.

### Command Line

```bash
# Fetch all archived URLs for a domain
curl "https://web.archive.org/cdx/search/cdx?url=*.TARGET&output=txt&fl=original&collapse=urlkey" | sort -u

# View specific snapshot
https://web.archive.org/web/TIMESTAMP/http://TARGET/
```

### Recon Value
- Find old pages, endpoints, files no longer linked
- Discover removed sensitive content
- Track tech stack changes over time
- Passive (no direct target interaction)

---

## VHost / subdomain fuzzing

When the main site uses a single vhost or redirects, enumerate subdomains by fuzzing the `Host` header. Filter by word count (`-fw`) or size (`-fs`) to drop the default response.

```bash
# Subdomains: FUZZ.TARGET.htb (add TARGET.htb and discovered hosts to /etc/hosts)
ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-large-words.txt:FUZZ \
     -u http://TARGET \
     -H "Host: FUZZ.TARGET" \
     -fw 21
```

Use `-fs 230` (or similar) to filter by response size if that better separates valid vhosts. Combine with nuclei as needed: `nuclei -u http://vhost.TARGET -rl 13 -c 12 -as`.

---

## Parameter Discovery & Fuzzing

### GET Parameter Fuzzing

```bash
# Fuzz for hidden GET parameters
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ \
     -u "http://TARGET/index.php?FUZZ=test" \
     -fs 1234  # Filter by response size

# Common hidden parameters
?debug=true
?test=1
?admin=1
?source=1
?mode=admin
?expertmode=tcp
```

### POST Parameter Fuzzing

```bash
# Fuzz POST parameters
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ \
     -u "http://TARGET/index.php" \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "FUZZ=test" \
     -fs 1234
```

### Parameter Value Fuzzing

```bash
# Fuzz parameter values (e.g., find valid modes)
ffuf -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ \
     -u "http://TARGET/index.php?mode=FUZZ" \
     -fs 1234
```

### Using Burp Intruder

1. Capture request in Proxy
2. Send to Intruder (Ctrl+I)
3. Add § markers around parameter name or value
4. Load wordlist in Payloads tab
5. Look for different response lengths/status codes

### Source Code Analysis

When you obtain source code (via LFI/SSRF), look for:

```php
// Hidden parameters in conditionals
if (isset($_GET['expertmode']) && $_GET['expertmode'] === 'tcp') {
    // Hidden functionality
}

if (isset($_GET['debug'])) {
    error_reporting(E_ALL);
}
```

### Useful Wordlists for Parameter Discovery

```bash
/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
/usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt
/usr/share/seclists/Discovery/Web-Content/common.txt
```

---

## Web Crawling

### Burp Suite Spider

1. Set scope to target domain
2. Right-click target in Site Map → Spider this host
3. Review discovered endpoints in Site Map

### OWASP ZAP Spider

1. Set target URL
2. Right-click → Attack → Spider
3. Review Sites tree for discovered content

### ReconSpider (Custom Tool)

```bash
wget -O ReconSpider.zip https://academy.hackthebox.com/storage/modules/144/ReconSpider.v1.2.zip
unzip ReconSpider.zip
python3 ReconSpider.py http://TARGET
```

Output in `results.json`:
- Emails, links, external files
- JavaScript files
- Form fields
- Images, videos, audio
- HTML comments

### Scrapy (Python)

```bash
pip3 install scrapy
```

Custom spider for large-scale crawling.

---

## Automation Frameworks

| Tool | Description |
|------|-------------|
| [FinalRecon](https://github.com/thewhiteh4t/FinalRecon) | Python-based, modular (SSL, WHOIS, headers, crawl) |
| [Recon-ng](https://github.com/lanmaster53/recon-ng) | Framework with modules for DNS, subdomains, ports, etc. |
| [theHarvester](https://github.com/laramies/theHarvester) | Email, subdomain, host gathering from multiple sources |
| [Amass](https://github.com/owasp-amass/amass) | Comprehensive subdomain enumeration |
| [Photon](https://github.com/s0md3v/Photon) | Fast crawler extracting URLs, emails, files, endpoints |

### FinalRecon

```bash
git clone https://github.com/thewhiteh4t/FinalRecon.git
cd FinalRecon
pip3 install -r requirements.txt

python3 finalrecon.py --full http://TARGET
```

### Recon-ng

```bash
# Start framework
recon-ng

# Create workspace
workspaces create TARGET

# Add target domain
db insert domains TARGET.com

# Use module
modules load recon/domains-hosts/hackertarget
run

# View results
show hosts
```
