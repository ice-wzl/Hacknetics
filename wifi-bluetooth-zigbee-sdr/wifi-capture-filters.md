# Wifi Capture Filters

### WEP Networks

* Per Wigle.net as of 2024, WEP networks make up less than 5% of all wireless networks, however they can still be found!
* In every WEP packet is an:
  * initialization vector
  * key index number
  * integrity check value.
* Display only WEP encrypted data packets

```
wlan.wep.iv
```

### BSSID

* Filtering on BSSIDs

```
!wlan.bssid eq 58:6d:8f:07:4e:8d
wlan.bssid eq 58:6d:8f:07:4e:8d
```

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

### Probe Requests

* Find clients looking for SSID names. Useful if you are looking to stand up an Evil Twin and would like a specific client to connect to you.
* Probe requests can have privacy implications. If you capture SSID names and they are unique, you are able to query https://wigle.net to potentially find home locations/work locations

```
(wlan.fc.subtype == 4) && (wlan.fc.type == 0)
# filter out probe requests
!(wlan.fc.subtype == 4) && !(wlan.fc.type == 0)
```

### WPA3 PSK networks&#x20;

* We can identify these networks in a wireshark pcap by filtering off the Auth Key Management suite in use&#x20;

```
wlan.fc.type_subtype == 0x0008 && wlan.rsn.akms == 0x00FAC08
```

* above AKMS identifies the most common key type in use GCMP-128

### Find Data packets with no Frame Body Encryption

* Encryption can still be used at the application layer i.e. TLS
* Can catch protocols that are not encrypted&#x20;

```
wlan.fc.protected == 0 && wlan.fc.type == 2
```

### WPA3 Transition networks

* wireshark filter for WPA3 transition networks. They will have to broadcast two cipher suites at once&#x20;

```
wlan.fc.type_subtype == 0x0008 && wlan.rsn.akms ==  0x000FAC02 && wlan.rsn.akms == 0x000FAc08
```

* `0x000FAC02` == WPA2
* `0x000FAC08` == WPA3

### Tcpdump no Beacons / Control frames

```
tcpdump -i wlan0mon -s 0 -n -w out.pcap 'not type mgt subtype beacon and not type ctl'
```

* capture the whole packet with `-s 0`
* capture everything that are not beacon frames + control frames (loud)
  * generally 10 beacon frames a second from each AP. If you are in range of 20 APs that can get rough quickly on pcap size&#x20;
* Great assessment tcpdump filter for assessments on smaller devices like a Pi
