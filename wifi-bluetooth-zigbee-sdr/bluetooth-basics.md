# Bluetooth Basics

* Class 1 External Bluetooth adapter. Provides \~100 yard range.
* [https://www.antaira.com/PARANI-UD100-G03](https://www.antaira.com/PARANI-UD100-G03)

### Basics of Interaction&#x20;

* `hciconfig` command is to bluetooth adapters as `ifconfig` is to linux networking interfaces.
* View your device

```
hciconfig
hci0:	Type: Primary  Bus: USB
	BD Address: 00:01:95:79:EF:89  ACL MTU: 310:10  SCO MTU: 64:8
	UP RUNNING 
	RX bytes:1252 acl:0 sco:0 events:76 errors:0
	TX bytes:2862 acl:0 sco:0 commands:75 errors:0
```

* Can see `Bus: USB`
* Interface name `hci0`
* BD Address (our address) `00:01:95:79:EF:89`
* Status of our adapter `UP RUNNING`
* `ACL MTU: 310:10`
  * The MTU size for ACL connections. 310 bytes. An ACL buffer size uses 10 packets.
* `SCO MTU: 64:8`
  * The MTU size for SCO connection. 64 bytes. An SCO buffer size uses 8 packets.
* UP - The interface is in the UP state.
* RUNNING - The interface is currently operational.
* PSCAN - The interface will respond to page scan messages.

### Bring Adapter Up/Down

```
hciconfig 
hci0:	Type: Primary  Bus: USB
	BD Address: 00:01:95:79:EF:89  ACL MTU: 310:10  SCO MTU: 64:8
	UP RUNNING 
	RX bytes:1252 acl:0 sco:0 events:76 errors:0
	TX bytes:2862 acl:0 sco:0 commands:75 errors:0
```

```
hciconfig hci0 down
hciconfig hci0 up 
```

### Central v Peripheral Mode

* See if your adapter is running in central or peripheral mode&#x20;

```
hciconfig hci0 lm
hci0:	Type: Primary  Bus: USB
	BD Address: 00:01:95:79:EF:89  ACL MTU: 310:10  SCO MTU: 64:8
	Link mode: PERIPHERAL ACCEPT 
```

* Can see we are in peripheral mode
* ACCEPT means that the interface will accept new baseband connections from a central device

### View Version&#x20;

```
hciconfig hci0 version
hci0:	Type: Primary  Bus: USB
	BD Address: 00:01:95:79:EF:89  ACL MTU: 310:10  SCO MTU: 64:8
	HCI Version: 4.0 (0x6)  Revision: 0x2031
	LMP Version: 4.0 (0x6)  Subversion: 0x2031
	Manufacturer: Cambridge Silicon Radio (10)
```
