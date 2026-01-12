# netsh bending traffic

#### Local Port Forwarding - Access Service Not Externally Exposed

```
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8888 connectaddress=127.0.0.1 connectport=80
```

#### Verify Port Forward

```
netsh.exe interface portproxy show v4tov4
```

#### Pivot - Local Port Forwarding with netsh

```
netsh.exe interface portproxy add v4tov4 listenport=88 listenaddress=0.0.0.0 connectport=88 connectaddress=10.11.1.120
netsh.exe interface portproxy add v4tov4 listenport=4444 listenaddress=0.0.0.0 connectport=21 connectaddress=10.1.1.27
netsh.exe interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=3389 connectaddress=172.16.197.5
netsh.exe interface portproxy add v4tov4 listenport=43389 listenaddress=0.0.0.0 connectport=22 connectaddress=172.16.9.25
```

#### Verify Port Forward

```
netsh.exe interface portproxy show v4tov4
```

#### Firewall Entry If Needed

```
netsh advfirewall firewall add rule name="forwarded_Port" protocol=TCP dir=in localip=0.0.0.0 localport=43389 action=allow
```

#### Cleanup

```
netsh interface portproxy reset
netsh advfirewall firewall del rule name="forwarded_RDPport_3340"
netsh interface portproxy delete v4tov4 listenport=4444 listenaddress=0.0.0.0 connectport=21 connectaddress=10.1.1.27
```

### Misc Usage

```
netsh.exe interface portproxy add v4tov4 listenport=443 listenaddress=172.16.118.3 connectport=8443 connectaddress=172.16.117.3
netsh advfirewall firewall add rule name="445" protocol=TCP dir=in localip=any localport=445 action=allow

netsh.exe interface portproxy add v4tov4 listenport=80 listenaddress=172.16.118.3 connectport=8080 connectaddress=172.16.117.3
netsh advfirewall firewall add rule name="80" protocol=TCP dir=in localip=any localport=80 action=allow

netsh.exe interface portproxy add v4tov4 listenport=8443 listenaddress=172.16.117.3 connectport=443 connectaddress=172.16.116.201
netsh advfirewall firewall add rule name="8443" protocol=TCP dir=in localip=any localport=8443 action=allow
```

#### Loop - Change Connect Address and Ports to Iterate

```
setlocal & for %i in (135,139,389,445,3389,5985) do (set /A x=%i+50000 & call netsh.exe interface portproxy add v4tov4 listenport=%x% listenaddress=0.0.0.0 connectport=%i connectaddress=172.16.210.5 & call netsh advfirewall firewall add rule name="forwarded_port_%x%" protocol=TCP dir=in localip=any localport=%x% action=allow) & set "x="
```

* For PSExec will need to SSH -L on Kali - only takes port 445 or 139

```
ssh -L 445:192.168.198.10:50445 kali@localhost
```

#### Loop - Cleanup

```
netsh interface portproxy reset & setlocal & for %i in (80,88,135,139,389,445,3389,5985) do (set /A x=%i+50000 & call netsh advfirewall firewall del rule name="forwarded_port_%x%") & set "x="
```

```
netsh.exe interface portproxy add v4tov4 listenport=8443 listenaddress=172.16.106.132 connectport=8443 connectaddress=192.168.50.74
netsh advfirewall firewall add rule name=8443 protocol=TCP dir=in localip=any localport=8443 action=allow
netsh.exe interface portproxy add v4tov4 listenport=80 listenaddress=172.16.106.132 connectport=80 connectaddress=192.168.50.74
netsh advfirewall firewall add rule name=80 protocol=TCP dir=in localip=any localport=80 action=allow
```
