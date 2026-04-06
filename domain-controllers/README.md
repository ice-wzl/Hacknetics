# Active Directory AD Attacks

{% embed url="https://casvancooten.com/posts/2020/11/windows-active-directory-exploitation-cheat-sheet-and-command-reference/" %}

## Attack Methodology

| Phase | Page |
|---|---|
| AD Fundamentals | [AD Overview](ad-overview.md) |
| Initial Enumeration (LotL) | [AD Enumeration Commands](ad-enumeration-commands.md) |
| LLMNR/NBT-NS Poisoning | [LLMNR/NBT-NS Poisoning](llmnr-nbt-ns-poisoning.md) |
| Password Spraying | [Password Spraying](password-spraying.md) |
| Credentialed Enumeration | [Credentialed AD Enumeration](credentialed-enumeration.md) |
| Kerberos Attacks | [Pentesting Kerberos](Kerberos.md) |
| ACL Abuse | [ACL Abuse](acl-abuse.md) |
| DCSync | [DCSync](dcsync.md) |
| Domain Trust Abuse | [Domain Trust Abuse](domain-trust-abuse.md) |
| Misc Misconfigurations | [Miscellaneous AD Misconfigurations](miscellaneous-ad-misconfigurations.md) |

## AD Enumeration Tools

- [SharpView](https://github.com/dmchell/SharpView) - .NET port of PowerView.ps1
- [Windapsearch](https://github.com/ropnop/windapsearch) - LDAP Enumeration
- [ldapsearch-ad](https://github.com/yaap7/ldapsearch-ad) - LDAP Enumeration
- [Get-ADGroupMemberDate](https://raw.githubusercontent.com/proxb/PowerShell_Scripts/master/Get-ADGroupMemberDate.ps1) - Retrieve date a user was added

## Active Directory GPO Tools

- [SharpGPOAbuse](https://github.com/FSecureLABS/SharpGPOAbuse) - Abuse GPO edit rights
- [Group3r](https://github.com/Group3r/Group3r) - Enumerate and identify exploitable GPO misconfigurations
- [GPOwned](https://github.com/X-C3LL/GPOwned)
- [pyGPOAbuse](https://github.com/Hackndo/pyGPOAbuse) - Python partial implementation of SharpGPOAbuse

## AD Misc Tools

- [GoldenGMSA](https://github.com/Semperis/GoldenGMSA) - C# tool for abusing Group Managed Service Accounts (gMSA)

## AD Lateral Movement Tools

- [SharpRDP](https://github.com/0xthirteen/SharpRDP) - .NET non-graphical RCE via RDP
- [SharpNoPSExec](https://github.com/juliourena/SharpNoPSExec) - Leverages existing services without creating new ones
- [NimExec](https://github.com/frkngksl/NimExec) - Fileless remote command execution via MS-SCMR
- [EvilWinRM](https://github.com/Hackplayers/evil-winrm)
- [SharpWSUS](https://github.com/nettitude/SharpWSUS) - Lateral movement through WSUS
- [KrbRelayUp](https://github.com/Dec0ne/KrbRelayUp) - Wrapper around Rubeus and KrbRelay
- [KrbRelay](https://github.com/cube0x0/KrbRelay) - Kerberos Relaying
- [SharpSystemTriggers](https://github.com/cube0x0/SharpSystemTriggers) - Remote authentication triggers
- [SpoolSample](https://github.com/leechristensen/SpoolSample) - PrinterBug Attack (Unconstrained Delegation)

## Windows Attack Boxes

- [Commando VM](https://github.com/mandiant/commando-vm) - Mandiant Windows security distribution
- [Flare VM](https://github.com/mandiant/flare-vm) - Mandiant reverse engineering environment
