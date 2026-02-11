# feroxbuster

Fast, recursive content discovery tool written in Rust. Excels at finding unlinked content.

**Install:**

```bash
curl -sL https://raw.githubusercontent.com/epi052/feroxbuster/main/install-nix.sh | sudo bash -s /usr/local/bin
```

---

## Basic Usage

```bash
# Default scan (uses built-in wordlist)
feroxbuster -u http://TARGET

# Custom wordlist
feroxbuster -u http://TARGET -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

---

## Recursive Scanning

Feroxbuster is recursive by default - automatically scans discovered directories.

```bash
# Limit recursion depth
feroxbuster -u http://TARGET -d 2

# Disable recursion
feroxbuster -u http://TARGET -n

# Only recurse on specific status codes
feroxbuster -u http://TARGET --force-recursion -s 200,301
```

---

## Extensions

```bash
# Add file extensions
feroxbuster -u http://TARGET -x php,html,txt,bak,js

# With dot prefix (some setups)
feroxbuster -u http://TARGET -x .php,.txt,.conf

# Multiple extensions
feroxbuster -u http://TARGET -x php -x html -x txt
```

## HTTPS

```bash
# Skip TLS verification (-k)
feroxbuster -u https://TARGET -k -E -g -t 10
```

---

## Filtering Output

| Flag | Description |
|------|-------------|
| `-s` | Status codes to include (whitelist) |
| `-C` | Status codes to exclude (blacklist) |
| `-S` | Filter by response size |
| `-W` | Filter by word count |
| `-N` | Filter by line count |
| `-X` | Filter by regex pattern |
| `--filter-similar-to` | Exclude pages similar to a reference |
| `--dont-scan` | Exclude specific paths from scanning |

### Examples

```bash
# Only show 200 responses
feroxbuster -u http://TARGET -s 200

# Exclude 404 and 500
feroxbuster -u http://TARGET -C 404,500

# Exclude by response size
feroxbuster -u http://TARGET -S 1234

# Filter by word count
feroxbuster -u http://TARGET -W 100

# Filter by regex (exclude error pages)
feroxbuster -u http://TARGET -X "not found|error"

# Don't scan specific paths
feroxbuster -u http://TARGET --dont-scan /uploads --dont-scan /static
```

---

## Performance

```bash
# Threads (default 50)
feroxbuster -u http://TARGET -t 100

# Rate limit (requests per second)
feroxbuster -u http://TARGET --rate-limit 100

# Timeout
feroxbuster -u http://TARGET -T 10
```

---

## Authentication

```bash
# Cookie
feroxbuster -u http://TARGET -b "session=abc123"

# Header
feroxbuster -u http://TARGET -H "Authorization: Bearer TOKEN"
```

---

## Proxy

```bash
# Through Burp
feroxbuster -u http://TARGET --insecure --proxy http://127.0.0.1:8080

# Through SOCKS proxy
feroxbuster -u http://TARGET --proxy socks5h://127.0.0.1:9050
```

---

## Output

```bash
# Save to file
feroxbuster -u http://TARGET -o results.txt

# JSON output
feroxbuster -u http://TARGET --json -o results.json

# Quiet mode (less output)
feroxbuster -u http://TARGET -q
```

---

## File Extensions & Word Extraction

```bash
# Auto adds extensions found when directory searching. If the web app is written in php feroxbuster will automatically start scanning for .php extensions
feroxbuster -u http://TARGET -E

# Collect words from responses (builds custom wordlist)
feroxbuster -u http://TARGET -g

# Both together - comprehensive discovery
feroxbuster -u http://TARGET -Eg -t 15
```

**Use case:** `-Eg` is great for initial recon - file extensions AND builds a wordlist from page content for further fuzzing.

---

## Advanced Options

```bash
# Follow redirects
feroxbuster -u http://TARGET -r

# Custom User-Agent
feroxbuster -u http://TARGET -a "Mozilla/5.0"

# Scan multiple URLs from file
feroxbuster --stdin < urls.txt

# Resume scan from state file
feroxbuster --resume-from ferox-state.json

# Auto-tune (smart throttling)
feroxbuster -u http://TARGET --auto-tune
```

---

## Quick Reference

```bash
# Standard recursive scan
feroxbuster -u http://TARGET -w /usr/share/seclists/Discovery/Web-Content/common.txt -x php,html -d 2

# Fast scan with filtering
feroxbuster -u http://TARGET -t 100 -C 404,403 -S 0

# Through proxy
feroxbuster -u http://TARGET --insecure --proxy http://127.0.0.1:8080 -k

# HTTPS dir bust with extensions and word extraction
feroxbuster -u https://TARGET -k -E -g -t 10 -x .txt,.php

# Save results
feroxbuster -u http://TARGET -o scan_results.txt
```
