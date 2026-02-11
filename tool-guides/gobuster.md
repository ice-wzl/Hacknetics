# gobuster

Fast directory/file, DNS, and vhost brute-forcer written in Go.

**Install:**

```bash
go install github.com/OJ/gobuster/v3@latest
```

---

## Directory Mode (dir)

```bash
# Basic directory scan
gobuster dir -u http://TARGET -w /usr/share/seclists/Discovery/Web-Content/common.txt

# With extensions
gobuster dir -u http://TARGET -w wordlist.txt -x php,html,txt,bak

# More threads
gobuster dir -u http://TARGET -w wordlist.txt -t 50
```

### Filtering

```bash
# Exclude status codes (blacklist)
gobuster dir -u http://TARGET -w wordlist.txt -b 302,404

# Include only specific codes
gobuster dir -u http://TARGET -w wordlist.txt -s 200,301

# Exclude response size
gobuster dir -u http://TARGET -w wordlist.txt --exclude-length 0,404
```

### Options

| Flag | Description |
|------|-------------|
| `-x` | File extensions to search |
| `-t` | Number of threads (default 10) |
| `-s` | Include only these status codes |
| `-b` | Exclude these status codes |
| `--exclude-length` | Exclude responses by size |
| `-k` | Skip TLS certificate verification (use with `-u https://`) |
| `-a` | Custom User-Agent |
| `-c` | Cookies to use |
| `-H` | Custom headers |
| `-o` | Output file |
| `-r` | Follow redirects |
| `-n` | Don't print status codes |

---

## VHost Mode (vhost)

```bash
# Basic vhost scan
gobuster vhost -u http://target.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain

# Filter false positives by excluding status codes
gobuster vhost -u http://target.htb -w subdomains.txt --append-domain --exclude-status 400,403
```

**Important:** Use `--append-domain` to append the base domain to each word.

---

## DNS Mode (dns)

Subdomain enumeration via DNS resolution:

```bash
# Basic DNS brute
gobuster dns -d target.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Show IP addresses
gobuster dns -d target.com -w subdomains.txt -i

# Custom resolver
gobuster dns -d target.com -w subdomains.txt -r 8.8.8.8
```

---

## Authentication

```bash
# Basic auth
gobuster dir -u http://TARGET -w wordlist.txt -U admin -P password

# Cookie
gobuster dir -u http://TARGET -w wordlist.txt -c "session=abc123"

# Header
gobuster dir -u http://TARGET -w wordlist.txt -H "Authorization: Bearer TOKEN"
```

---

## Common Wordlists

```
/usr/share/seclists/Discovery/Web-Content/common.txt
/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
/usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt
/usr/share/seclists/Discovery/Web-Content/raft-small-words.txt
/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
/usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt
```

---

## Quick Reference

```bash
# Directory brute
gobuster dir -u http://TARGET -w /usr/share/seclists/Discovery/Web-Content/common.txt -x php,html -t 50

# Vhost enum
gobuster vhost -u http://target.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain

# DNS subdomain enum
gobuster dns -d target.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -i

# HTTPS directory scan (skip cert verify, lowercase wordlist, more threads)
gobuster dir -k -u https://target.htb -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -t 20
```
