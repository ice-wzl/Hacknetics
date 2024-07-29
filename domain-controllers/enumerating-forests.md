# Enumerating Forests

* See if your domain is in a forest

```
get-adforest

ApplicationPartitions : {DC=DomainDnsZones,DC=DANTE,DC=local, 
                        DC=ForestDnsZones,DC=DANTE,DC=local}
CrossForestReferences : {}
DomainNamingMaster    : DANTE-DC01.DANTE.local
Domains               : {DANTE.local}
ForestMode            : Windows2012R2Forest
GlobalCatalogs        : {DANTE-DC01.DANTE.local}
Name                  : DANTE.local
PartitionsContainer   : CN=Partitions,CN=Configuration,DC=DANTE,DC=local
RootDomain            : DANTE.local
SchemaMaster          : DANTE-DC01.DANTE.local
Sites                 : {Default-First-Site-Name}
SPNSuffixes           : {}
UPNSuffixes           : {}
```

* Look for the "Name" property in the output. If it returns a value, it means your domain controller is part of a forest

```
Get-ADDomainController -Filter *


ComputerObjectDN           : CN=DANTE-DC01,OU=Domain 
                             Controllers,DC=DANTE,DC=local
DefaultPartition           : DC=DANTE,DC=local
Domain                     : DANTE.local
Enabled                    : True
Forest                     : DANTE.local
HostName                   : DANTE-DC01.DANTE.local
InvocationId               : ba7c8279-7a1a-4caf-932b-e6b33907b70d
IPv4Address                : 172.16.1.20
IPv6Address                : 
IsGlobalCatalog            : True
IsReadOnly                 : False
LdapPort                   : 389
Name                       : DANTE-DC01
NTDSSettingsObjectDN       : CN=NTDS Settings,CN=DANTE-DC01,CN=Servers,CN=Defau
                             lt-First-Site-Name,CN=Sites,CN=Configuration,DC=DA
                             NTE,DC=local
OperatingSystem            : Windows Server 2012 R2 Standard
OperatingSystemHotfix      : 
OperatingSystemServicePack : 
OperatingSystemVersion     : 6.3 (9600)
OperationMasterRoles       : {SchemaMaster, DomainNamingMaster, PDCEmulator, 
                             RIDMaster...}
Partitions                 : {DC=ForestDnsZones,DC=DANTE,DC=local, 
                             DC=DomainDnsZones,DC=DANTE,DC=local, 
                             CN=Schema,CN=Configuration,DC=DANTE,DC=local, 
                             CN=Configuration,DC=DANTE,DC=local...}
ServerObjectDN             : CN=DANTE-DC01,CN=Servers,CN=Default-First-Site-Nam
                             e,CN=Sites,CN=Configuration,DC=DANTE,DC=local
ServerObjectGuid           : e6a5e077-f303-4cad-83fc-1d711dc6fbbc
Site                       : Default-First-Site-Name
SslPort                    : 636

```

```
Get-ADDomainController -Filter * | ForEach-Object { Resolve-DnsName -Name $_.HostName | Select-Object -ExpandProperty IPAddress }
fe80::9086:e8f3:3115:6b43
172.16.1.20
```
