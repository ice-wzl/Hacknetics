# SharpView PowerView

Great for domain enumeration and replacement of `net` commands / other windows built-ins.

SharpView is a replacement for powerview due to alot of increased awareness and logging that occurs in modern power shell versions.

Cannot use `| select` with SharpView due to it returning strings instead of power shell objects&#x20;

### PowerView and Opsec

PowerView can leverage token impersonation. Instead of creating a new process, you can run commands as another user by using the `-Credential` flag. This will generate a logon event on the host.

### Sid Name Conversion

```
ConvertTo-SID -name m.jones
Convert-ADName -ObjectName S-1-5-21-2974783224-3764228556-2640795941-1724
.\SharpView.exe ConvertTo-SID -name m.jones
.\SharpView.exe Convert-ADName -ObjectName S-1-5-21-2974783224-3764228556-2640795941-1724
```

### Domain Policy

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

### GPO Enumeration

```
.\SharpView.exe Get-DomainGPO | findstr displayname
Get-DomainGPO | select displayname
```

Its helpful to figure out which GPO applies to which host&#x20;

```
.\SharpView.exe Get-DomainGPO -ComputerIdentity WS01 | findstr /b "displayname"
Get-DomainGPO -ComputerIdentity WS01 | select displayname
```

### Enumerate Users

```
# all users
Get-DomainUser
.\SharpView.exe Get-DomainUser
# single user
Get-DomainUser harry.jones
.\SharpView.exe Get-DomainUser harry.jones

Get-DomainUser | select cn
.\SharpView.exe Get-DomainUser | findstr /b "cn"
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

#### AS-REPRoast

```
Get-DomainUser -KerberosPreauthNotRequired
.\SharpView.exe Get-DomainUser -KerberosPreauthNotRequired
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

### Enumerate Computers

```
Get-DomainComputer | select dnshostname,useraccountcontrol
.\SharpView.exe Get-DomainComputer | findstr /b /c:"dnshostname" /c:"useraccountcontrol"
```

#### Test Local Admin Access

```
Test-AdminAccess -ComputerName WS01
Find-LocalAdminAccess
.\SharpView.exe Test-AdminAccess -ComputerName WS01
.\SharpView.exe Find-LocalAdminAccess
```

#### Enumerate Shares

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
