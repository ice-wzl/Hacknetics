# pktmon Packet Capture Windows

* pktmon is a native binary found on Windows 10 systems
* Can capture packets based on port number
* Binary found on all post Win 10 October 18 update
* Binary with pcap conversion ability found on all Win 10 2004 (May 2020 update)&#x20;
* Packet Capture will be saved in .etl format, convert it to a pcap --> [https://github.com/microsoft/etl2pcapng/](https://github.com/microsoft/etl2pcapng/)

### Capture Packet Process

* View the filters saved on the machine first (if any)

```
pktmon filter list
```

* Create your own filters

```
pktmon filter add -t TCP -p 8080 -i 10.10.120.1
pktmon filter add -t UDP -p 69 
```

* Capture Packets&#x20;

```
pktmon start --etw -po -f output.etl
pktmon stop 
```

* Convert if the system is post required updated

```
pktmon pcapng input.etl -o output.etl
```
