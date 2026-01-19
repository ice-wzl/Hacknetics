# osTicket

## Overview

- Open-source support ticketing system
- Written in PHP with MySQL backend
- Often exposes company email domains

---

## Discovery

- Cookie: `OSTSESSID`
- Footer: "powered by osTicket"
- Default path: `/support/`

---

## Email Domain Exposure

### Attack Flow

1. Create support ticket on osTicket portal
2. osTicket assigns temporary email: `940288@company.local`
3. Use this email to register on other services (Slack, GitLab, etc.)
4. Verification emails appear in osTicket ticket thread

### Exploitation

1. Submit new ticket
2. Note assigned email (e.g., `940288@inlanefreight.local`)
3. Use email to register on:
   - Slack workspace
   - GitLab instance
   - Mattermost
   - Internal wikis

4. Check ticket for verification email
5. Complete registration on target service

---

## CVE-2020-24881 (SSRF)

**Affects:** osTicket 1.14.1

SSRF vulnerability to access internal resources:

```bash
# May allow internal port scanning
# May expose internal services
```

---

## Credential Reuse

If you obtain leaked credentials (via Dehashed, breaches):

1. Try credentials on osTicket admin panel
2. Admin panel typically at `/scp/`
3. Look for API keys, integrations, email configs

---

## Important Paths

| Path | Description |
|------|-------------|
| `/scp/` | Staff Control Panel (admin) |
| `/api/` | API endpoint |
| `/kb/` | Knowledge base |
| `/tickets.php` | Ticket submission |

---

## Post-Access

If admin access obtained:
- Check `Admin Panel → Emails` for SMTP credentials
- Check `Admin Panel → API Keys` for API tokens
- Review `Admin Panel → Plugins` for integrations
