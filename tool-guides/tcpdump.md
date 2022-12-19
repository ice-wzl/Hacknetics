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

### Dump Windows Memory&#x20;

```
winpmem_mini.exe 20221218-ircase#0100.mem
```

### Volatility

* Best to use a virtual enviroment&#x20;

```
python3 -m venv venv
source venv/bin/activate
```

#### General Usage&#x20;

```
./vol.py -f image_name --profile profile_name plugin_name
```

* Save off some enviromental variables that will help with command length and typos

```
export VOLATILITY_LOCATION=file:///path/image
export VOLATILITY_PROFILE=profile
```

#### Vol Plugins

* There are alot of created plugins, view plugins

```
python vol.py --info
```

#### Basic Image Information (Start Here)

* This provides basic information about the image, will suggest which volatility plugin to use&#x20;

```
./vol.py imageinfo
#OR on windows cmd
ver
#Output 
Microsoft Windows [Version 10.0.20348.1249]
#now search for the build version 
python vol.py --info | grep 20348
```

#### Listing Processes

```
vol.py pslist
```

#### Parent and Child Processes&#x20;

```
vol.py pstree
```

#### Network Connections

```
vol.py netscan
```

#### UserAssist&#x20;

* UserAssist registry keys track any program run from the GUI, create for creating IR timelines

```
vol.py userassist
```

#### Processs Command Line&#x20;

* See full command line used to start processes&#x20;

```
vol.py cmdline
```

#### Guidelines

* Suspicious process --> `pslist`, `pstree`
* Network Listener --> `netscan`, check processes&#x20;
* Suspicious program --> `userassist` , `cmdline` , processes
* Others --> `hivelist` `printkey` `svcscan` `dllist`
