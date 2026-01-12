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
