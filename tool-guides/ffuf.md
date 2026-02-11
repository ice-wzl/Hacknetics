# ffuf

Fast web fuzzer written in Go. Excellent for directories, files, parameters, vhosts.

**Install:**

```bash
go install github.com/ffuf/ffuf/v2@latest
```

---

## Basic Usage

```bash
ffuf -w WORDLIST -u http://TARGET/FUZZ
```

The `FUZZ` keyword is replaced with each word from the wordlist.

---

## Directory Fuzzing

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -u http://TARGET/FUZZ

# With status code filtering
ffuf -w wordlist.txt -u http://TARGET/FUZZ -mc 200,301,302
```

---

## File Fuzzing

```bash
# Single extension
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u http://TARGET/FUZZ.php

# Multiple extensions
ffuf -w wordlist.txt -u http://TARGET/FUZZ -e .php,.html,.txt,.bak,.js
```

---

## Recursive Fuzzing

Automatically fuzz discovered directories:

```bash
ffuf -w wordlist.txt -u http://TARGET/FUZZ -recursion

# Limit recursion depth
ffuf -w wordlist.txt -u http://TARGET/FUZZ -recursion -recursion-depth 2

# With extensions
ffuf -w wordlist.txt -u http://TARGET/FUZZ -e .html -recursion -ic
```

`-ic` = Ignore comments (lines starting with #)

---

## Parameter Fuzzing

### GET Parameters

```bash
# Fuzz parameter name
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u "http://TARGET/page.php?FUZZ=value"

# Fuzz parameter value
ffuf -w wordlist.txt -u "http://TARGET/page.php?id=FUZZ"
```

### POST Parameters

```bash
ffuf -w wordlist.txt \
  -u http://TARGET/login.php \
  -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=FUZZ"
```

### JSON Body

```bash
ffuf -w wordlist.txt \
  -u http://TARGET/api/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","pass":"FUZZ"}'
```

---

## VHost / Subdomain Fuzzing

```bash
# VHost fuzzing via Host header
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  -u http://TARGET \
  -H "Host: FUZZ.target.com"

# Filter by response size (find unique responses)
ffuf -w subdomains.txt -u http://target.com -H "Host: FUZZ.target.com" -fs 1234

# HTTPS subdomain enum: -k skip TLS verify; -fc 200 to exclude 200 (default vhost)
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt \
  -u https://target.htb -H "Host: FUZZ.target.htb" -k -fc 200

# HTTP subdomain enum: filter by fixed size of default response
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt \
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
| `-fw` | Filter word count (exclude responses with this many words) |

### Examples

```bash
# Match only 200 responses
ffuf -w wordlist.txt -u http://TARGET/FUZZ -mc 200

# Filter out 404 and 403
ffuf -w wordlist.txt -u http://TARGET/FUZZ -fc 404,403

# Filter by response size (remove false positives)
ffuf -w wordlist.txt -u http://TARGET/FUZZ -fs 0

# Filter by word count
ffuf -w wordlist.txt -u http://TARGET/FUZZ -fw 12

# Match all, then filter
ffuf -w wordlist.txt -u http://TARGET/FUZZ -mc all -fc 404

# Filter by regex
ffuf -w wordlist.txt -u http://TARGET/FUZZ -fr "not found"
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

## Authentication

```bash
# Cookie
ffuf -w wordlist.txt -u http://TARGET/FUZZ -b "session=abc123"

# Header
ffuf -w wordlist.txt -u http://TARGET/FUZZ -H "Authorization: Bearer TOKEN"

# Basic Auth
ffuf -w wordlist.txt -u http://admin:password@TARGET/FUZZ
```

---

## Performance Options

```bash
# Threads (default 40)
ffuf -w wordlist.txt -u http://TARGET/FUZZ -t 100

# Rate limit (requests per second)
ffuf -w wordlist.txt -u http://TARGET/FUZZ -rate 50

# Timeout
ffuf -w wordlist.txt -u http://TARGET/FUZZ -timeout 5
```

---

## Output

```bash
# JSON output
ffuf -w wordlist.txt -u http://TARGET/FUZZ -o results.json -of json

# CSV output
ffuf -w wordlist.txt -u http://TARGET/FUZZ -o results.csv -of csv

# HTML output
ffuf -w wordlist.txt -u http://TARGET/FUZZ -o results.html -of html

# Verbose mode
ffuf -w wordlist.txt -u http://TARGET/FUZZ -v
```

---

## Proxy

```bash
# Through Burp
ffuf -w wordlist.txt -u http://TARGET/FUZZ -x http://127.0.0.1:8080

# Replay proxy (for matched results only)
ffuf -w wordlist.txt -u http://TARGET/FUZZ -replay-proxy http://127.0.0.1:8080
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
/usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt
```

---

## Quick Reference Commands

```bash
# Directory brute
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://TARGET/FUZZ

# File brute with extensions
ffuf -w wordlist.txt -u http://TARGET/FUZZ -e .php,.html,.txt,.bak

# Recursive directory scan
ffuf -w wordlist.txt -u http://TARGET/FUZZ -recursion -recursion-depth 2 -e .php -ic

# Subdomain enum
ffuf -w subdomains.txt -u http://target.com -H "Host: FUZZ.target.com" -fs 1234

# POST parameter fuzz
ffuf -w wordlist.txt -u http://TARGET/login -X POST -d "user=admin&pass=FUZZ" -fc 401

# API endpoint discovery
ffuf -w wordlist.txt -u http://TARGET/api/FUZZ -mc 200,401,403

# LFI fuzz
ffuf -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt -u "http://TARGET/page.php?file=FUZZ" -fs 0

# LFI fuzz with auth (cookie + Referer), filter by word count
ffuf -X GET -H "Host: target.htb" -H "Referer: http://target.htb/manage.php" -b "PHPSESSID=abc" \
  -u "http://target.htb/manage.php?notes=files/FUZZ" -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt -fw 280

# LFI fuzz param name (FUZZ=value)
ffuf -X GET -H "Host: target.htb" -b "PHPSESSID=abc" \
  -u "http://target.htb/manage.php?notes=FUZZ" -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt -fw 280
```
