# Ghost CMS

Headless CMS (Node.js). Often detected as "Ghost" + version in Wappalyzer/nuclei (e.g. Ghost 5.58). Admin panel: `/ghost/#/signin`.

**No default credentials** — the initial admin is created during setup at first access.

---

## Discovery

* Footer: "Powered by Ghost"
* Admin: `http://TARGET/ghost/#/signin`
* Nuclei: `nuclei -u http://TARGET -rl 13 -c 12 -as` can detect ghost-panel, metatag-cms (version), and CVE-2022-41697.
* VHost enum: ffuf with `-H "Host: FUZZ.target.htb"` and `-fs SIZE` (baseline size) to find subdomains like `dev`.

---

## CVE-2022-41697 (user enum / auth bypass)

Affects Ghost admin API session endpoint. Use **Content-Type: application/json** or the request may not be handled as expected.

* **Endpoint:** `POST /ghost/api/admin/session` with JSON body `{"username":"email@target","password":"..."}`.
* Nuclei template: `[CVE-2022-41697] [http] [medium] http://TARGET/ghost/api/admin/session`.
* Reference: https://talosintelligence.com/vulnerability_reports/TALOS-2022-1625

User enumeration (e.g. with ffuf) can be done by fuzzing the username/email and filtering on response (e.g. `-fr "Authorization failed"` or `-fc 403`). Using a request file is often easier: save the POST request from Burp with `FUZZ` in the email, then:

```bash
ffuf -request users.req --request-proto http -w /usr/share/seclists/Usernames/Names/names.txt -fc 403
```

---

## Authenticated file read (LFI)

With valid admin credentials, some exploits provide an interactive file-read shell (e.g. via Ghost API or theme/settings abuse):

```bash
python3 ghost_fileread.py -t http://TARGET -u 'admin@TARGET' -p 'PASSWORD'
# Then at file> prompt:
file> /etc/passwd
file> /var/lib/ghost/config.production.json
```

**Config path (production):** `/var/lib/ghost/config.production.json`. Contains `url`, `server.port`, `database`, and often **mail** with SMTP credentials (`auth.user`, `auth.pass`) that may be reused for SSH or other services.

---

## Exposed .git on subdomain

If a subdomain (e.g. `dev.TARGET`) serves the app from a directory with **exposed .git**, you can try to recover the repo:

* **feroxbuster:** `feroxbuster -u http://dev.TARGET -E -g -w common.txt` — look for `/.git` (301 → `/.git/`).
* **Dump .git:** [git-dumper](https://github.com/arthaud/git-dumper) (Python) often works when other tools fail:
  ```bash
  python3 git_dumper.py http://dev.TARGET/.git /tmp/out
  ```
* **Staged changes / secrets:** After cloning or extracting, check staged diff for hardcoded credentials:
  ```bash
  git diff --cached
  ```
  (Without `--cached`, only unstaged changes are shown.) Test files or config in the repo may contain passwords.

---

## Typical path to shell

1. Enumerate vhosts (ffuf `-fs`), find e.g. `dev`.
2. Find exposed `.git` on dev, dump with git-dumper, run `git diff --cached` for credentials.
3. Or exploit CVE-2022-41697 / brute force Ghost admin.
4. Log in to Ghost, use file-read (e.g. ghost_fileread.py) to read `config.production.json` and obtain mail or other creds.
5. Reuse creds for SSH or next service.
