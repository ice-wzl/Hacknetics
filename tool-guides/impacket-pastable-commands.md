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
