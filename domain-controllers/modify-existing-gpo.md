# Modify Existing GPO

* Identify GPOs in the domain, check the ACL of each
* Filter for principal with modify privileges

```
powershell Get-DomainGPO | Get-DomainObjectAcl -ResolveGUIDs | ? { $_.ActiveDirectoryRights -match "CreateChild|WriteProperty" -and $_.SecurityIdentifier -match "S-1-5-21-1304128723-2758812735-1929980917-[\d]{4,10}" }

`AceType               : AccessAllowed
ObjectDN              : CN={5059FAC1-5E94-4361-95D3-3BB235A23928},CN=Policies,CN=System,DC=dev,DC=cyberbotic,DC=io
ActiveDirectoryRights : CreateChild, DeleteChild, ReadProperty, WriteProperty, GenericExecute
OpaqueLength          : 0
ObjectSID             : 
InheritanceFlags      : ContainerInherit
BinaryLength          : 36
IsInherited           : False
IsCallback            : False
PropagationFlags      : None
SecurityIdentifier    : S-1-5-21-569305411-121244042-2357301523-1107
AccessMask            : 131127
AuditFlags            : None
AceFlags              : ContainerInherit
AceQualifier          : AccessAllowed`    

```

* Resolve the GUID for  the GPO

```
powershell Get-DomainGPO -Identity "CN={827D319E-6EAC-11D2-A4EA-00C04F79F83A},CN=Policies,CN=System,DC=dev,DC=cyberbotic,DC=io" | select displayName, gpcFileSysPath
displayname    gpcfilesyspath                                                                              
-----------    --------------                                                                              
Vulnerable GPO \\dev.cyberbotic.io\SysVol\dev.cyberbotic.io\Policies\{5059FAC1-5E94-4361-95D3-3BB235A23928}
```

* Convert the SID

```
powershell ConvertFrom-SID S-1-5-21-569305411-121244042-2357301523-1107
DEV\Developers
```

* This shows us that members of the "Developers" group can modify "Vulnerable GPO".
* Determine which OU this GPO applies to

```
powershell Get-DomainOU -GPLink "{5059FAC1-5E94-4361-95D3-3BB235A23928}" | select distinguishedName
distinguishedname                         
-----------------                         
OU=Workstations,DC=dev,DC=cyberbotic,DC=io
```

* Get computers that are a part of that OU

```
powershell Get-DomainComputer -SearchBase "OU=Workstations,DC=dev,DC=cyberbotic,DC=io" | select dnsHostName
dnshostname              
-----------              
wkstn-1.dev.cyberbotic.io
wkstn-2.dev.cyberbotic.io
```

* Without GPMC (Group Policy Management Console)
* Manual method - Modify files in SYSVOL

```
ls \\dev.cyberbotic.io\SysVol\dev.cyberbotic.io\Policies\{5059FAC1-5E94-4361-95D3-3BB235A23928}

Size     Type    Last Modified         Name
 ----     ----    -------------         ----
          dir     09/07/2022 12:40:22   Machine
          dir     09/07/2022 12:40:22   User
 59b      fil     09/07/2022 12:40:22   GPT.INI
```
