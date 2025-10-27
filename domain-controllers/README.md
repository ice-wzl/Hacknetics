# Active Directory AD Attacks

{% embed url="https://casvancooten.com/posts/2020/11/windows-active-directory-exploitation-cheat-sheet-and-command-reference/" %}

* Some great tools to help you pillage Windows environments&#x20;

### AD Enumeration

#### SharpView - .NET port of PowerView.ps1

* https://github.com/dmchell/SharpView

#### Get-ADGroupMemberDate - Retireves date a user was added

* https://raw.githubusercontent.com/proxb/PowerShell\_Scripts/master/Get-ADGroupMemberDate.ps1

#### Windapsearch - LDAP Enumeration

* https://github.com/ropnop/windapsearch

#### ldapsearch-ad - LDAP Enumeration

* https://github.com/yaap7/ldapsearch-ad

### Active Directory GPO

#### SharpGPOAbuse

* .NET application written in C# that can be used to take advantage of a user's edit rights on a Group Policy Object (GPO)
* https://github.com/FSecureLABS/SharpGPOAbuse

#### Group3r

* Enumerate relevant settings in AD Group Policy, and to identify exploitable misconfigurations
* https://github.com/Group3r/Group3r

#### GPOwned

* https://github.com/X-C3LL/GPOwned

#### pyGPOAbuse

* Python partial implementation of SharpGPOAbuse
* https://github.com/Hackndo/pyGPOAbuse

### AD Misc

#### GoldenGMSA

* C# tool for abusing Group Managed Service Accounts (gMSA) in Active Directory
* https://github.com/Semperis/GoldenGMSA

### AD Lateral Movement

#### SharpRDP

* .NET tool allows for non-graphical RCE via RDP
* https://github.com/0xthirteen/SharpRDP

### SharpNoPSExec

* Leverages existing services on a target system without creating new ones or writing to disk
* https://github.com/juliourena/SharpNoPSExec

### NimExec

* Fileless remote command execution tool. Operates by exploiting the Service Control Manager Remote Protocol (MS-SCMR)
* https://github.com/frkngksl/NimExec

#### EvilWinRM

* https://github.com/Hackplayers/evil-winrm

#### SharpWSUS

* CSharp tool for lateral movement through WSUS
* https://github.com/nettitude/SharpWSUS

### AD Lateral Movement

#### KrbRelayUp

* Simple wrapper around some of the features of Rubeus and KrbRelay in order to streamline
* https://github.com/Dec0ne/KrbRelayUp

#### KrbRelay

* Kerberos Relaying
* https://github.com/cube0x0/KrbRelay

#### SharpSystemTriggers

* Collection of remote authentication triggers coded in C#
* https://github.com/cube0x0/SharpSystemTriggers

#### SpoolSample

* PrinterBug Attack (Unconstrained Delegation)
* https://github.com/leechristensen/SpoolSample

### Windows Attack Boxes

#### Commando VM

* Mandiant - Comprehensive and customizable, Windows-based security distribution for penetration testing and red teaming
* https://github.com/mandiant/commando-vm

#### Flare VM

* Mandiant - Reverse engineering environment on a virtual machine
* https://github.com/mandiant/flare-vm
