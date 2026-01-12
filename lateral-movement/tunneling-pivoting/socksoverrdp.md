# SocksOverRDP

#### Binaries

* https://github.com/nccgroup/SocksOverRDP/releases
* https://www.proxifier.com/download/#win-tab

#### Setup

* Copy SocksOverRDP.zip to target and unzip
* Loading SocksOverRDP.dll using regsvr32.exe
* As Admin & Disable Realtime Protection

```
Set-MpPreference -DisableRealtimeMonitoring $true
regsvr32.exe SocksOverRDP-Plugin.dll
```

#### Run RDP and Enter Target IP

```
mstsc.exe
```

* Will get prompt - enter creds
* Transfer SocksOverRDP-Server.exe to target

#### Confirming the SOCKS Listener is Started on Pivot

```
netstat -antb | findstr 1080
```

#### Transfer Proxifier to Pivot Host

* Configure Proxifier

```
Profile > Proxy Server > Add
127.0.0.1 1080 Socks5
```
