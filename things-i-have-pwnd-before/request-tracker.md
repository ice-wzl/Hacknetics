# Request Tracker (RT)

Open-source ticketing system by Best Practical Solutions.

**Common Path:** `/rt/`

---

## Discovery

```bash
# Look for RT paths
/rt/
/rt/login
/rt/NoAuth/Login.html

# Version in footer
»|« RT 4.4.4+dfsg-2ubuntu1 (Debian)
```

---

## Default Credentials

| Username | Password |
|----------|----------|
| `root` | `password` |
| `admin` | `admin` |

---

## Post-Authentication Enumeration

### Users

```
Admin → Users → Select
```

Look for:
- Additional usernames
- User comments (often contain temp passwords like "Initial password set to Welcome2023!")
- Email addresses

### Tickets

Browse tickets for:
- Sensitive attachments
- Passwords in ticket body
- Internal hostnames/IPs
- Application names/versions

---

## Interesting Endpoints

| Path | Description |
|------|-------------|
| `/rt/Admin/Users/Modify.html?id=X` | User details (may contain passwords in comments) |
| `/rt/Ticket/Display.html?id=X` | View ticket |
| `/rt/Search/Results.html` | Search all tickets |
| `/rt/Admin/` | Admin panel |

---

## Known Vulnerabilities

### CVE-2022-25802 - XSS

Stored XSS in ticket subject/body.

### CVE-2021-38562 - Information Disclosure

Unauthenticated user enumeration via timing attack.

---

## Config Files

```
/opt/rt4/etc/RT_SiteConfig.pm
/etc/request-tracker4/RT_SiteConfig.d/
```

May contain database credentials:
```perl
Set($DatabaseType, 'mysql');
Set($DatabaseUser, 'rt_user');
Set($DatabasePassword, 'password');
```
