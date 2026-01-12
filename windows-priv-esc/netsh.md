# netsh

#### Capture

```cmd
netsh trace start capture=yes tracefile=C:\Users\Administrator\Documents\cap.etl
```

#### Stop

```cmd
netsh trace stop
```

#### Convert to PCAP

* https://github.com/microsoft/etl2pcapng

```cmd
etl2pcapng.exe in.etl out.pcapng
```
