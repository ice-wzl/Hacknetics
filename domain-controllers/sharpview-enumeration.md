# SharpView PowerView

Great for domain enumeration and replacement of `net` commands / other windows built-ins.

SharpView is a replacement for powerview due to alot of increased awareness and logging that occurs in modern power shell versions.

Cannot use `| select` with SharpView due to it returning strings instead of power shell objects&#x20;

Getting help with `SharpView.exe`  is easy

```
.\SharpView.exe Get-DomainUser -Help
```

### PowerView and Opsec

PowerView can leverage token impersonation. Instead of creating a new process, you can run commands as another user by using the `-Credential` flag. This will generate a logon event on the host.

### Sid Name Conversion

```
ConvertTo-SID -name m.jones
Convert-ADName -ObjectName S-1-5-21-2974783224-3764228556-2640795941-1724
.\SharpView.exe ConvertTo-SID -name m.jones
.\SharpView.exe Convert-ADName -ObjectName S-1-5-21-2974783224-3764228556-2640795941-1724
```

## Domain Policy

Get general domain information&#x20;

```
Get-DomainPolicy
Get-Domain
.\SharpView.exe Get-DomainPolicy
.\SharpView.exe Get-Domain
```

Get all the Organizational Units, helps to map the domain structure

```

Get-DomainOU | select name 
.\SharpView.exe Get-DomainOU | findstr /b "name"
```

## GPO Enumeration

```
.\SharpView.exe Get-DomainGPO | findstr displayname
Get-DomainGPO | select displayname
```

Its helpful to figure out which GPO applies to which host&#x20;

```
.\SharpView.exe Get-DomainGPO -ComputerIdentity WS01 | findstr /b "displayname"
Get-DomainGPO -ComputerIdentity WS01 | select displayname
```

## Enumerate Users

```
(Get-DomainUser).count
# all users
Get-DomainUser
.\SharpView.exe Get-DomainUser
# single user
Get-DomainUser harry.jones
.\SharpView.exe Get-DomainUser harry.jones

Get-DomainUser -Identity harry.jones -Domain inlanefreight.local | Select-Object -Property name,samaccountname,description,memberof,whencreated,pwdlastset,lastlogontimestamp,accountexpires,admincount,userprincipalname,serviceprincipalname,mail,useraccountcontrol
.\SharpView.exe Get-DomainUser -Identity harry.jones -Domain inlanefreight.local | findstr /b "cn"
```

Get important values for all users, export to csv for offline processing

```
Get-DomainUser * -Domain inlanefreight.local | Select-Object -Property name,samaccountname,description,memberof,whencreated,pwdlastset,lastlogontimestamp,accountexpires,admincount,userprincipalname,serviceprincipalname,mail,useraccountcontrol | Export-Csv .\inlanefreight_users.csv -NoTypeInformation
```

When enumerating UAC values, they are displayed as non human-readable. Convert them with powerview, ones that apply to the user have `+` after them&#x20;

```
Get-DomainUser m.jones | ConvertFrom-UACValue -showall
--snip--
SCRIPT                         1
ACCOUNTDISABLE                 2
HOMEDIR_REQUIRED               8
LOCKOUT                        16
PASSWD_NOTREQD                 32+
--snip--
```

### Kerberoasting

```
.\SharpView.exe Get-DomainUser -SPN -Properties samaccountname,memberof,serviceprincipalname
Get-DomainUser -SPN -Properties samaccountname,memberof,serviceprincipalname
```

Check for users with SPNs in another domain allowing kerberoasting across trusts

```
Get-DomainUser -SPN -Domain freightlogistics.local | select samaccountname,memberof,serviceprincipalname | fl
```

### AS-REPRoast

```
.\SharpView.exe Get-DomainUser -KerberosPreauthNotRequired -Properties samaccountname,useraccountcontrol,memberof
Get-DomainUser -KerberosPreauthNotRequired -Properties samaccountname,useraccountcontrol,memberof
```

### Constrained Delegation

```
.\SharpView.exe Get-DomainUser -TrustedToAuth -Properties samaccountname,useraccountcontrol,memberof
Get-DomainUser -TrustedToAuth -Properties samaccountname,useraccountcontrol,memberof
```

### Unconstrained Delegation

```
.\SharpView.exe Get-DomainUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=524288)"
Get-DomainUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=524288)"
```

### Passwords in the Description

```
Get-DomainUser -Properties samaccountname,description | Where {$_.description -ne $null}
.\SharpView.exe Get-DomainUser -Properties samaccountname,description
```

### Active Sessions

Find domain machines that users are logged into

```
Find-DomainUserLocation
.\SharpView.exe Find-DomainUserLocation
```

Find log on events for specified user

```
Find-DomainUserEvent
.\SharpView.exe
```

## Enumerate Computers

```
Get-DomainComputer | select dnshostname,useraccountcontrol
.\SharpView.exe Get-DomainComputer | findstr /b /c:"dnshostname" /c:"useraccountcontrol"
```

### Test Local Admin Access

```
Test-AdminAccess -ComputerName WS01
Find-LocalAdminAccess
.\SharpView.exe Test-AdminAccess -ComputerName WS01
.\SharpView.exe Find-LocalAdminAccess
```

### Enumerate Shares

```
# (S/P)
Get-NetShare -ComputerName DC01
Find-DomainShare
Find-InterestingDomainShareFile
.\SharpView.exe Get-NetShare -ComputerName DC01
.\SharpView.exe Find-DomainShare
.\SharpView.exe Find-InterestingDomainShareFile
```

### Domain Trusts

Returns all domain trusts for the current domain or specified domain

```
Get-DomainTrust
.\SharpView.exe Get-DomainTrust
```

Returns all forest trusts for the current forest or specified forest

```
Get-ForestTrust
.\SharpView.exe Get-ForestTrust
```

Enumerate users who are in groups outside of the users domain

```
Get-DomainForeignUser
.\SharpView.exe Get-DomainForeignUser
```

Enumerate groups with users outside of the groups domain and return each foreign member

```
Get-DomainForeignGroupMember
.\SharpView.exe Get-DomainForeignGroupMember
```

Enumerate all trusts for the current domain and then enumerate all trusts for each domain it finds

```
Get-DomainTrustMapping
.\SharpView.exe Get-DomainTrustMapping
```

Find any user from foreign domain with group membership with any groups in our current domain. You will get back `MemberName` use `Convert-SidToName` to turn it into username

```
Find-ForeignGroup
.\SharpView.exe Find-ForeignGroup
```

### Password Set Times

Likely to get caught if you spray across an entire domain. Get the password set time, look for clusters of passwords being reset close to eachother. They were likely reset by the help desk to the default password of the organization.

For the ones that are the same you can do selective guessing. i.e. for one account spray `Password2026` for another spray `Freight2024!` etc. This allows you to effectively try many more than just four passwords if the lockout policy is in effect.&#x20;

Pay attention to set times. If a password was set in August 2025, attempting `Winter2026` likely makes no sense.&#x20;

If you see old passwords set > 2 years ago, likely weak passwords. Try to guess those first.

Admins typically have sperate Admin accounts from their user accounts. If you see that their normal and admin account passwords were set at the same time, they are likely using the same password for both!

```
Get-DomainUser -Properties samaccountname,pwdlastset,lastlogon -Domain InlaneFreight.local | select samaccountname, pwdlastset, lastlogon | Sort-Object -Property pwdlastset
.\SharpView.exe Get-DomainUser -Properties samaccountname,pwdlastset,lastlogon -Domain InlaneFreight.local | select samaccountname, pwdlastset, lastlogon | Sort-Object -Property pwdlastset
```

Passwords set longer than 90 days ago&#x20;

```
Get-DomainUser -Properties samaccountname,pwdlastset,lastlogon -Domain InlaneFreight.local | select samaccountname, pwdlastset, lastlogon | where { $_.pwdlastset -lt (Get-Date).addDays(-90) }
.\SharpView.exe Get-DomainUser -Properties samaccountname,pwdlastset,lastlogon -Domain InlaneFreight.local | select samaccountname, pwdlastset, lastlogon | where { $_.pwdlastset -lt (Get-Date).addDays(-90) }
```
