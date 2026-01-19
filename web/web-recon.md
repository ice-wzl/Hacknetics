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
