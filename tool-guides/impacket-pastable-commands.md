# Impacket Pastable Commands

### impacket-mssqlclient

```
#set env vars
domain=RLAB
user=epugh_adm
pass=Password!
ip=10.10.122.15
proxychains -q impacket-mssqlclient $domain/$user:$pass@$ip -windows-auth
```

### Windows Auth issues&#x20;

* If you recieve this error below

```
python3 mssqlclient.py $user:$pass@$ip -windows-auth 
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Encryption required, switching to TLS
[-] ERROR(DANTE-SQL01\SQLEXPRESS): Line 1: Login failed. The login is from an untrusted domain and cannot be used with Integrated authentication.
```

* Drop the `-windows-auth` and run the same command :)&#x20;

```
python3 mssqlclient.py $user:$pass@$ip              
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DANTE-SQL01\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(DANTE-SQL01\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands
SQL (administrator dbo@master)> 
```
