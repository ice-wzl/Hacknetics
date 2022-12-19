# tcpdump

* Capture traffic on an interface or all&#x20;

```
tcpdump -i eth0
tcpdump -i any 
```

* Capture and write to a file&#x20;

```
tcpdump -i eth0 -w file_name.pcapng
```

* Read packets from a file, do not resolve hosts/ports

```
tcpdump -r file_name.pcapng -n 
```

* Read packets from a file, dont resolve, show as ASCII

```
tcpdump -r file_name.pcapng -n -A
```

### Useful BPF Examples

* Traffic going to or from a host&#x20;

```
tcpdump -r file_name.pcapng 'host 192.168.1.34'
```

* Traffic coming from host

```
tcpdump -r file_name.pcapng 'src host 192.168.1.34'
```

* Traffic where the source is not a specific host&#x20;

```
tcpdump -r file_name.pcapng 'not src host 192.168.1.34'
```

* Only ICMP traffic from a sepecifc host&#x20;

```
tcpdump -r file_name.pcapng 'icmp and (src host 19.168.1.34)
```
