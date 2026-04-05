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

---

### Multi-Hop RDP

After Proxifier is configured, use `mstsc.exe` to RDP to deeper internal targets through the SOCKS tunnel chain.

### Performance Tip

Set mstsc.exe Experience tab Performance to **Modem** for slow tunneled connections to reduce bandwidth overhead.
