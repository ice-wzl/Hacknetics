# AD Enumeration Commands (Living Off the Land)

## Host & Network Recon

| Command | Description |
|---|---|
| `hostname` | PC's Name |
| `[System.Environment]::OSVersion.Version` | OS version and revision |
| `wmic qfe get Caption,Description,HotFixID,InstalledOn` | Patches and hotfixes |
| `ipconfig /all` | Network adapter state |
| `set` | Environment variables (CMD) |
| `echo %USERDOMAIN%` | Domain name (CMD) |
| `echo %logonserver%` | Domain Controller name (CMD) |
| `systeminfo` | Comprehensive host summary |

## PowerShell Enumeration

| Cmdlet | Description |
|---|---|
| `Get-Module` | List available modules |
| `Get-ExecutionPolicy -List` | Execution policy settings |
| `Set-ExecutionPolicy Bypass -Scope Process` | Bypass for current process only |
| `Get-ChildItem Env: \| ft Key,Value` | Environment variables |
| `Get-Content $env:APPDATA\Microsoft\Windows\Powershell\PSReadline\ConsoleHost_history.txt` | PowerShell command history |

### PowerShell Downgrade (Evasion)
```powershell
# Check current version
Get-host

# Downgrade to v2 (no Script Block Logging)
powershell.exe -version 2
```

## Active Directory PowerShell Module

```powershell
Import-Module ActiveDirectory

# Domain info
Get-ADDomain

# Users with SPNs (Kerberoastable)
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName

# Trust relationships
Get-ADTrust -Filter *

# Group enumeration
Get-ADGroup -Filter * | select name

# Group membership
Get-ADGroupMember -Identity "Backup Operators"
```

## Security Controls Checks

### Windows Defender
```powershell
Get-MpComputerStatus
```

### AppLocker
```powershell
Get-AppLockerPolicy -Effective | select -ExpandProperty RuleCollections
```

### Constrained Language Mode
```powershell
$ExecutionContext.SessionState.LanguageMode
```

### LAPS Enumeration
```powershell
# Find delegated groups
Find-LAPSDelegatedGroups

# Check extended rights
Find-AdmPwdExtendedRights

# Get LAPS passwords (if you have access)
Get-LAPSComputers
```

### Firewall
```powershell
netsh advfirewall show allprofiles
```

### Windows Defender Service
```cmd
sc query windefend
```

## Network Commands

| Command | Description |
|---|---|
| `arp -a` | Known hosts in ARP table |
| `ipconfig /all` | Adapter settings |
| `route print` | Routing table (IPv4 & IPv6) |
| `netsh advfirewall show allprofiles` | Firewall status |

## WMI Commands

| Command | Description |
|---|---|
| `wmic computersystem get Name,Domain,Manufacturer,Model,Username,Roles /format:List` | Host info |
| `wmic process list /format:list` | All processes |
| `wmic ntdomain list /format:list` | Domain and DC info |
| `wmic useraccount list /format:list` | All local and domain accounts |
| `wmic group list /format:list` | Local groups |
| `wmic sysaccount list /format:list` | System/service accounts |

## Net Commands

| Command | Description |
|---|---|
| `net accounts` | Password requirements |
| `net accounts /domain` | Domain password and lockout policy |
| `net group /domain` | Domain groups |
| `net group "Domain Admins" /domain` | Domain admin members |
| `net group "domain computers" /domain` | Domain-joined PCs |
| `net group "Domain Controllers" /domain` | Domain Controllers |
| `net localgroup` | All local groups |
| `net localgroup administrators` | Local admins |
| `net share` | Current shares |
| `net user <ACCOUNT_NAME> /domain` | User info |
| `net user /domain` | All domain users |
| `net view` | List computers |
| `net view /domain` | PCs in the domain |

- **Tip:** Use `net1` instead of `net` to potentially avoid detection

## Dsquery (on DCs or hosts with AD DS role)

```powershell
# User search
dsquery user

# Computer search
dsquery computer

# Wildcard search in OU
dsquery * "CN=Users,DC=INLANEFREIGHT,DC=LOCAL"

# Users with PASSWD_NOTREQD
dsquery * -filter "(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=32))" -attr distinguishedName userAccountControl

# Domain Controllers
dsquery * -filter "(userAccountControl:1.2.840.113556.1.4.803:=8192)" -limit 5 -attr sAMAccountName
```

### LDAP Filter OID Match Strings
- `1.2.840.113556.1.4.803` - Bit value must match completely (AND)
- `1.2.840.113556.1.4.804` - Any bit match (OR)
- `1.2.840.113556.1.4.1941` - Match Distinguished Name (recursive membership)

## Check Who Else is Logged In
```powershell
qwinsta
```
