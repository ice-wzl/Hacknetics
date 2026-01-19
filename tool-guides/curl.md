# curl

Command-line tool for transferring data with URLs. Essential for web pentesting.

---

## Basic Usage

```bash
# Simple GET request
curl http://TARGET

# Download file
curl -O http://TARGET/file.txt

# Download with custom name
curl -o output.txt http://TARGET/file.txt

# Silent mode (no progress)
curl -s http://TARGET

# Follow redirects
curl -L http://TARGET
```

---

## Viewing Headers & Verbose

```bash
# Response headers only (HEAD request)
curl -I http://TARGET

# Include response headers with body
curl -i http://TARGET

# Verbose output (full request/response)
curl -v http://TARGET

# Extra verbose
curl -vvv http://TARGET
```

---

## Request Methods

```bash
# GET (default)
curl http://TARGET

# POST
curl -X POST http://TARGET

# PUT
curl -X PUT http://TARGET/resource/1

# DELETE
curl -X DELETE http://TARGET/resource/1

# PATCH
curl -X PATCH http://TARGET/resource/1

# OPTIONS (check allowed methods)
curl -X OPTIONS http://TARGET -i
```

---

## POST Data

### Form Data (application/x-www-form-urlencoded)

```bash
curl -X POST -d "username=admin&password=admin" http://TARGET/login
```

### JSON Data

```bash
curl -X POST http://TARGET/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

### File Upload

```bash
# Single file
curl -X POST http://TARGET/upload -F "file=@shell.php"

# Multiple files
curl -X POST http://TARGET/upload -F "file1=@img.jpg" -F "file2=@doc.pdf"

# With form fields
curl -X POST http://TARGET/upload \
  -F "file=@shell.php" \
  -F "name=test" \
  -F "submit=Upload"
```

---

## Headers

```bash
# Add custom header
curl -H "X-Custom: value" http://TARGET

# Multiple headers
curl -H "Header1: value1" -H "Header2: value2" http://TARGET

# User-Agent
curl -A "Mozilla/5.0" http://TARGET

# Referer
curl -e "http://google.com" http://TARGET
```

---

## Authentication

### Basic Auth

```bash
# With -u flag
curl -u admin:password http://TARGET

# In URL
curl http://admin:password@TARGET

# Manual Authorization header
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQ=" http://TARGET
```

### Bearer Token

```bash
curl -H "Authorization: Bearer JWT_TOKEN" http://TARGET/api/resource
```

### Cookie

```bash
# Send cookie
curl -b "PHPSESSID=abc123" http://TARGET

# Cookie as header
curl -H "Cookie: PHPSESSID=abc123; other=value" http://TARGET

# Save cookies to file
curl -c cookies.txt http://TARGET/login -d "user=admin&pass=admin"

# Use saved cookies
curl -b cookies.txt http://TARGET/dashboard
```

---

## SSL/TLS

```bash
# Skip certificate verification (for self-signed)
curl -k https://TARGET

# Specify CA cert
curl --cacert ca.crt https://TARGET

# Client certificate
curl --cert client.crt --key client.key https://TARGET
```

---

## Proxy

```bash
# HTTP proxy
curl -x http://127.0.0.1:8080 http://TARGET

# SOCKS proxy
curl --socks5 127.0.0.1:1080 http://TARGET

# Through Burp/ZAP
curl -x http://127.0.0.1:8080 -k https://TARGET
```

---

## Output Control

```bash
# Write output to file
curl -o output.html http://TARGET

# Append to file
curl http://TARGET >> output.txt

# Only response body (default)
curl http://TARGET

# Write headers to separate file
curl -D headers.txt -o body.html http://TARGET

# Response code only
curl -s -o /dev/null -w "%{http_code}" http://TARGET
```

---

## Useful Options

| Flag | Description |
|------|-------------|
| `-s` | Silent (no progress) |
| `-S` | Show errors (use with -s) |
| `-L` | Follow redirects |
| `-I` | HEAD request (headers only) |
| `-i` | Include response headers |
| `-v` | Verbose |
| `-k` | Ignore SSL errors |
| `-X` | Request method |
| `-d` | POST data |
| `-F` | Form data (multipart) |
| `-H` | Add header |
| `-A` | User-Agent |
| `-e` | Referer |
| `-b` | Send cookies |
| `-c` | Save cookies |
| `-u` | Basic auth |
| `-x` | Proxy |
| `-o` | Output file |
| `-O` | Save with remote name |
| `--connect-timeout` | Connection timeout |
| `--max-time` | Max operation time |

---

## HTTP Methods Reference

| Method | Description |
|--------|-------------|
| `GET` | Retrieve resource |
| `POST` | Submit data (create) |
| `PUT` | Update/replace resource |
| `PATCH` | Partial update |
| `DELETE` | Remove resource |
| `HEAD` | Headers only (no body) |
| `OPTIONS` | Get allowed methods |

---

## Status Codes Quick Reference

| Code | Meaning |
|------|---------|
| `200` | OK |
| `201` | Created |
| `301` | Moved Permanently |
| `302` | Found (redirect) |
| `400` | Bad Request |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Not Found |
| `405` | Method Not Allowed |
| `500` | Internal Server Error |
| `502` | Bad Gateway |
| `503` | Service Unavailable |

---

## Common Pentest Commands

```bash
# Enumerate web server
curl -I http://TARGET

# Test for directory listing
curl http://TARGET/images/

# Check robots.txt
curl http://TARGET/robots.txt

# API endpoint with JSON
curl -s http://TARGET/api/users | jq

# POST login and follow redirect
curl -L -d "user=admin&pass=admin" http://TARGET/login

# Download with authentication
curl -u admin:pass -O http://TARGET/backup.zip

# Test for HTTP verb tampering
curl -X PUT http://TARGET/admin
curl -X DELETE http://TARGET/admin

# Check allowed methods
curl -X OPTIONS http://TARGET -i

# Send request through Burp
curl -x http://127.0.0.1:8080 -k http://TARGET

# Base64 encode credentials for Basic auth
echo -n "admin:password" | base64
# YWRtaW46cGFzc3dvcmQ=
```

---

## CRUD API Example

```bash
# READ - Get resource
curl -s http://TARGET/api/v1/users/1 | jq

# CREATE - Add new resource
curl -X POST http://TARGET/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"newuser","email":"new@test.com"}'

# UPDATE - Modify resource
curl -X PUT http://TARGET/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"updated","email":"updated@test.com"}'

# DELETE - Remove resource
curl -X DELETE http://TARGET/api/v1/users/1

# List all (empty path)
curl -s http://TARGET/api/v1/users/ | jq
```

---

## URL Structure Reference

```
http://admin:password@example.com:8080/path/file.php?param=value#section
|____| |____________| |__________||___||____________| |_________| |_____|
scheme   userinfo        host     port    path       query string fragment
```

| Component | Example | Notes |
|-----------|---------|-------|
| Scheme | `http://`, `https://` | Protocol |
| User Info | `admin:password@` | Basic auth in URL |
| Host | `example.com` | Domain or IP |
| Port | `:8080` | Default: 80 (http), 443 (https) |
| Path | `/path/file.php` | Resource location |
| Query String | `?param=value` | GET parameters |
| Fragment | `#section` | Client-side only |
