# Wifi Capture Filters

### Handshakes

* To filter for four-way handshake packets in Wireshark&#x20;

```
eapol
```

* To filter for four-way handshake packets in tcpdump or to set a capture filter to only grab four-way handshake packets.

```
ether proto 0x888e
```

### Beacons

* wireshark filter for beacon frames&#x20;

```
wlan.fc.type_subtype == 0x0008
```

### Management Frames&#x20;

* wireshark filter for management frames&#x20;

```
wlan.fc.type == 0
```

### WPA3 PSK networks&#x20;

* We can identify these networks in a wireshark pcap by filtering off the Auth Key Management suite in use&#x20;

```
wlan.fc.type_subtype == 0x0008 && wlan.rsn.akms == 0x00FAC08
```
