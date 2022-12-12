# netcat

### Netcat Relays on Windows

* Start by entering a temp dir where we can create files

```
cd C:\temp
```

#### Listener to Client Relay&#x20;

* This creates a relay that sends packets from the local port to a netcat client connected to the target ip address on the target port

```
echo nc [TargetIPAddr] [port] > relay.bat
nc -l -p [LocalPort] -e relay.bat
```

### Listener to Listener Relay

```
echo nc -l -p [Local_Port_2] > relay.bat
nc -l -p [Local_Port_1] -e relay.bat
```

* This creates a relay that will send packets from any connection on `Local_Port_1` to any connection on `Local_Port_2`

### Client to Client Relay

```
echo nc [NextHopIPAddr] [port2] > relay.bat
nc [PreviousHopIPAddr] [port] -e relay.bat
```

* This creates a relay that will send packets from the connection to `PreviousHopIPAddr` on `port` to a netcat client connected to `NextHopIPAddr` on `port2`

### Netcat Command Flags

* `-l` Listen mode&#x20;
* `-L` Listen harder, only supported on windows versions of netcat. This option makes netcat persistently listen which will listen again after client disconnect.
* `-u` UDP mode&#x20;
* `-p` Local Port. In listen mode this is the port listened on, in client mode this is the source port for all packets sent
* `-e` Program the execute after connection occurs, connecting STDIN and STDOUT of the program&#x20;
* `-n` Dont perform DNS look up on names of machines on the other side
* `-z` Zero I/O mode.  Dont send any data, just emit a packet with out a payload&#x20;
* `-wN` Timeout of connections.  Wait N seconds after closure of STDIN. If connection doesnt happen after N seconds netcat will stop listening
* `-v` `-vv` Be verbose, be very verbose respectively

### TCP Banner Grabs

```
echo "" | nc -v -n -w1 [TargetIP] [start_port]-[end_port]
```

* Grab the banner of any TCP service running on an IP from a linux machine&#x20;
* `-r` Add this flag to randomize destination ports within the range&#x20;
* `-p` add this flag to specify a source port for the connection

### Netcat Relays on Linux

* Move to tmp dir and create a FIFO

```
cd /tmp
mknod backpipe p
```

#### Listener to Client Relay

```
nc -l -p [Local_Port] 0<backpipe | nc [Target_IP_Addr] [port] | tee backpipe
```

* Create a relay that sends packets from the `Local_Port` to a netcat client connected to `Target_IP_Addr` on `port`

#### Listener to Listener Relay&#x20;

```
nc -l -p [Local_Port_1] 0<backpipe | nc -l -p [Local_Port_2] | tee backpipe
```

* Create a relay that sends packets from any connection on `Local_Port_1` to any connection on `Local_Port_2`

#### Client to Client Relay&#x20;

```
nc [PreviousHopIPAddr] [port] 0<backpipe | nc [NextHopIPAddr] [port2] | tee backpipe
```

* Create a relay that sends packets from the connection to `PreviousHopIPAddr` on `port` to a netcat client connected to `NextHopIPAddr` on `port2`
