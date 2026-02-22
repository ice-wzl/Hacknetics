# ffuf

Fast web fuzzer written in Go. Excellent for directories, files, parameters, vhosts.

**Install:**

```bash
go install github.com/ffuf/ffuf/v2@latest
```

---

## Wordlist and keyword

Assign a wordlist to a keyword with `-w PATH:KEYWORD`. Default keyword is `FUZZ`; use `:FUZZ` explicitly for clarity.

```bash
ffuf -w /path/to/wordlist.txt:FUZZ -u http://TARGET/FUZZ
```

---

## Directory Fuzzing

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt:FUZZ \
  -u http://TARGET/FUZZ

# With status code filtering
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -mc 200,301,302
```

---

## File Fuzzing

```bash
# Single extension
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt:FUZZ \
  -u http://TARGET/FUZZ.php

# Multiple extensions
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -e .php,.html,.txt,.bak,.js

# Extension fuzzing (wordlist contains the dot, e.g. .php, .html)
ffuf -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt:FUZZ \
  -u http://TARGET/blog/indexFUZZ
```

---

## Recursive Fuzzing

URL must end with `FUZZ` for recursion. Automatically fuzz discovered directories:

```bash
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -recursion

# Limit recursion depth
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -recursion -recursion-depth 2

# With extensions; -ic = ignore wordlist lines starting with #
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -e .php -recursion -ic
```

---

## Parameter Fuzzing

POST form data needs `-H "Content-Type: application/x-www-form-urlencoded"`. JSON body needs `-H "Content-Type: application/json"`.

### GET Parameters

```bash
# Fuzz parameter name (filter by size to drop default response)
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ \
  -u "http://TARGET/page.php?FUZZ=key" -fs 1234

# Fuzz parameter value (e.g. id=FUZZ with ids/values wordlist)
ffuf -w wordlist.txt:FUZZ -u "http://TARGET/page.php?id=FUZZ" -fs 1234
```

### POST Parameters

```bash
ffuf -w wordlist.txt:FUZZ \
  -u http://TARGET/login.php \
  -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=FUZZ"
```

### JSON Body

```bash
ffuf -w wordlist.txt:FUZZ \
  -u http://TARGET/api/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","pass":"FUZZ"}'
```

---

## VHost / Subdomain Fuzzing

VHost = same IP, fuzz `Host` header; filter by default response size (`-fs`) to see only different vhosts.

```bash
# VHost fuzzing via Host header
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ \
  -u http://TARGET -H "Host: FUZZ.target.com"

# Filter by response size (default vhost returns fixed size; -fs drops it)
ffuf -w subdomains.txt:FUZZ -u http://target.com -H "Host: FUZZ.target.com" -fs 1234

# HTTPS: -k skip TLS verify; -fc 200 to exclude 200 (default vhost)
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt:FUZZ \
  -u https://target.htb -H "Host: FUZZ.target.htb" -k -fc 200

# HTTP: filter by fixed size of default response
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt:FUZZ \
  -u http://target.htb -H "Host: FUZZ.target.htb" -fs 178
```

---

## Filtering Output

### Match Filters (include results)

| Flag | Description |
|------|-------------|
| `-mc` | Match status codes (default: 200,204,301,302,307,401,403,405,500) |
| `-ms` | Match response size |
| `-mw` | Match word count |
| `-ml` | Match line count |
| `-mt` | Match response time (e.g., `>500` for > 500ms) |

### Filter Filters (exclude results)

| Flag | Description |
|------|-------------|
| `-fc` | Filter (exclude) status codes |
| `-fs` | Filter response size |
| `-fw` | Filter word count |
| `-fl` | Filter line count |
| `-fr` | Filter by regex |

### Examples

```bash
# Match only 200 responses
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -mc 200

# Filter out 404 and 403
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -fc 404,403

# Filter by response size (remove false positives)
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -fs 0

# Filter by word count
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -fw 12

# Match all, then filter
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -mc all -fc 404

# Filter by regex
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -fr "not found"
```

---

## Multiple Wordlists

Use different keywords for multiple positions:

```bash
# Username:Password brute force
ffuf -w users.txt:USER -w passwords.txt:PASS \
  -u http://TARGET/login \
  -X POST -d "user=USER&pass=PASS"

# Clusterbomb mode (all combinations)
ffuf -w list1.txt:W1 -w list2.txt:W2 -u http://TARGET/W1/W2 -mode clusterbomb
```

---

## Request from file (Burp / raw HTTP)

Use a saved HTTP request so headers and body match exactly (e.g. for API user enum, JSON POST):

```bash
# FUZZ in the request file is replaced by wordlist; --request-proto http or https
ffuf -request users.req --request-proto http -w /usr/share/seclists/Usernames/Names/names.txt:FUZZ

# Filter status code
ffuf -request users.req --request-proto http -w wordlist.txt:FUZZ -fc 403
```

Save the request from Burp (e.g. Paste from file) with `FUZZ` where the payload goes.

---

## Authentication

```bash
# Cookie
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -b "session=abc123"

# Header
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -H "Authorization: Bearer TOKEN"

# Basic Auth
ffuf -w wordlist.txt:FUZZ -u http://admin:password@TARGET/FUZZ
```

---

## Performance Options

```bash
# Threads (default 40)
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -t 100

# Rate limit (requests per second)
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -rate 50

# Timeout
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -timeout 5
```

---

## Output

```bash
# JSON output
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -o results.json -of json

# CSV output
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -o results.csv -of csv

# HTML output
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -o results.html -of html

# Verbose mode
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -v
```

---

## Proxy

```bash
# Through Burp
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -x http://127.0.0.1:8080

# Replay proxy (for matched results only)
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -replay-proxy http://127.0.0.1:8080
```

---

## Common Wordlists

```
/usr/share/seclists/Discovery/Web-Content/common.txt
/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
/usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt
/usr/share/seclists/Discovery/Web-Content/big.txt
/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
/usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt
/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
/usr/share/seclists/Discovery/Web-Content/web-extensions.txt
/usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt
```

---

## Quick Reference Commands

```bash
# Directory brute
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt:FUZZ -u http://TARGET/FUZZ

# File brute with extensions
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -e .php,.html,.txt,.bak

# Recursive directory scan (URL must end with FUZZ)
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -recursion -recursion-depth 2 -e .php -ic

# Subdomain/VHost enum (filter default response size)
ffuf -w subdomains.txt:FUZZ -u http://target.com -H "Host: FUZZ.target.com" -fs 1234

# POST form fuzz (include Content-Type)
ffuf -w wordlist.txt:FUZZ -u http://TARGET/login -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" -d "user=admin&pass=FUZZ" -fc 401

# API endpoint discovery
ffuf -w wordlist.txt:FUZZ -u http://TARGET/api/FUZZ -mc 200,401,403

# LFI fuzz
ffuf -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u "http://TARGET/page.php?file=FUZZ" -fs 0

# LFI fuzz with auth (cookie + Referer), filter by word count
ffuf -X GET -H "Host: target.htb" -H "Referer: http://target.htb/manage.php" -b "PHPSESSID=abc" \
  -u "http://target.htb/manage.php?notes=files/FUZZ" -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -fw 280

# LFI fuzz param name (FUZZ=value)
ffuf -X GET -H "Host: target.htb" -b "PHPSESSID=abc" \
  -u "http://target.htb/manage.php?notes=FUZZ" -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -fw 280
```
