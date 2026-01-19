# Bug Bounty Hunting Process

## Program Types

| Type | Description |
|------|-------------|
| **Private** | Invite only, based on track record |
| **Public** | Open to all hackers |
| **VDP** | Vulnerability Disclosure Program - no rewards, just guidelines |
| **BBP** | Bug Bounty Program - rewards for valid findings |

---

## Finding Programs

- [HackerOne Directory](https://hackerone.com/directory/programs)
- [Bugcrowd Programs](https://bugcrowd.com/programs)
- [Intigriti Programs](https://www.intigriti.com/programs)
- [YesWeHack](https://yeswehack.com/programs)

---

## Program Structure Checklist

| Element | Check |
|---------|-------|
| **Scope** | In-scope domains, IPs, apps |
| **Out of Scope** | Excluded targets, vuln types |
| **Rules of Engagement** | Testing limitations |
| **Rewards** | Bounty amounts by severity |
| **Response SLAs** | Expected response times |
| **Safe Harbor** | Legal protection |
| **Reporting Format** | Required info in reports |

---

## Bug Report Structure

| Section | Content |
|---------|---------|
| **Title** | `[VulnType] in [Component] - [Impact]` |
| **CWE** | Common Weakness Enumeration ID |
| **CVSS** | Severity score (use calculator) |
| **Description** | What the vuln is, where it exists |
| **POC** | Step-by-step reproduction |
| **Impact** | Business impact, what attacker can achieve |
| **Remediation** | Fix suggestion (optional) |

---

## CVSS 3.1 Calculator

https://www.first.org/cvss/calculator/3.1

### Attack Vector (AV)

| Value | Meaning |
|-------|---------|
| **N** (Network) | Remotely exploitable |
| **A** (Adjacent) | Same network required |
| **L** (Local) | Local access required |
| **P** (Physical) | Physical access required |

### Attack Complexity (AC)

| Value | Meaning |
|-------|---------|
| **L** (Low) | No special conditions |
| **H** (High) | Special prep/info gathering needed |

### Privileges Required (PR)

| Value | Meaning |
|-------|---------|
| **N** (None) | Unauth exploitation |
| **L** (Low) | Standard user privs |
| **H** (High) | Admin privs needed |

### User Interaction (UI)

| Value | Meaning |
|-------|---------|
| **N** (None) | No user action needed |
| **R** (Required) | User must click/visit |

### Scope (S)

| Value | Meaning |
|-------|---------|
| **U** (Unchanged) | Only affects vuln component |
| **C** (Changed) | Affects other components |

### CIA Impact

| Value | C/I/A Impact |
|-------|--------------|
| **N** (None) | No impact |
| **L** (Low) | Limited impact |
| **H** (High) | Total/serious impact |

---

## CVSS Score Examples

### Critical (9.8) - RCE Unauth

```
AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
```

### High (8.8) - SQLi Auth Required

```
AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H
```

### Medium (5.4) - CSRF

```
AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N
```

### Medium (5.5) - Stored XSS (Admin Panel)

```
AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:N
```

### Low (3.5) - Reflected XSS

```
AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N
```

---

## Common CWEs

| CWE | Vulnerability |
|-----|--------------|
| CWE-79 | XSS |
| CWE-89 | SQL Injection |
| CWE-352 | CSRF |
| CWE-502 | Deserialization |
| CWE-918 | SSRF |
| CWE-22 | Path Traversal |
| CWE-78 | OS Command Injection |
| CWE-287 | Improper Authentication |
| CWE-639 | IDOR |
| CWE-611 | XXE |

---

## Report Title Examples

```
Stored XSS in Profile Bio leads to Account Takeover
SQLi in Search Parameter allows Database Dump  
SSRF in PDF Generator exposes Internal Services
IDOR in /api/users/{id} exposes PII of all users
CSRF in Password Change lacks Token Validation
```

---

## Good Report Examples (HackerOne)

- [SSRF in Exchange → ROOT access](https://hackerone.com/reports/341876)
- [RCE in Slack Desktop](https://hackerone.com/reports/783877)
- [API Explorer exposes names](https://hackerone.com/reports/520518)
- [XSS via Google Login](https://hackerone.com/reports/691611)

---

## Communication Rules

| Do | Don't |
|----|-------|
| Wait for response | Spam triage team |
| Tag same team member | Use unofficial channels |
| Stay professional | Argue over severity |
| Reference program policy | Demand specific bounty |
| Use mediation if stuck | Disclose before resolution |

---

## Disagreement Process

1. Explain CVSS metric rationale
2. Reference program policy/scope
3. Request mediation (platform service)

---

## Quick POC Templates

### XSS POC

```markdown
1. Navigate to http://target.com/profile
2. In "Bio" field, enter: `"><script>alert(document.cookie)</script>`
3. Save profile
4. View profile → alert fires
```

### SQLi POC

```markdown
1. Navigate to http://target.com/search
2. In search field, enter: `' OR 1=1--`
3. All records returned (expected: none)
4. Enter: `' UNION SELECT username,password FROM users--`
5. Credentials dumped
```

### CSRF POC

```html
<html>
<body onload="document.forms[0].submit()">
<form action="http://target.com/change-email" method="POST">
  <input name="email" value="attacker@evil.com">
</form>
</body>
</html>
```

### SSRF POC

```markdown
1. Navigate to http://target.com/fetch-url
2. Enter URL: `http://169.254.169.254/latest/meta-data/`
3. AWS metadata returned
```
