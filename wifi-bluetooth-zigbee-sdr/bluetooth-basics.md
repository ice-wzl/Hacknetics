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

### Change the name of Adapter&#x20;

```
hciconfig hci0 name 
sudo hciconfig hci0 name SECRET
hciconfig hci0 name
```

* Names cannot be blank and names cannot be in excess of 248 bytes in length
* **BlueZ stack limits devices to 247 byte name length**

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

### Enable Discoverable Mode&#x20;

* configure device to be in discoverable mode and allow connections to the interface&#x20;

```
sudo hciconfig hci0 piscan
hciconfig hci0 
hci0:	Type: Primary  Bus: USB
	BD Address: 00:01:95:79:EF:89  ACL MTU: 310:10  SCO MTU: 64:8
	UP RUNNING PSCAN ISCAN 
	RX bytes:1278 acl:0 sco:0 events:79 errors:0
	TX bytes:2904 acl:0 sco:0 commands:78 errors:0
```

* If successful you will see `PSCAN ISCAN`

### Disable Discoverable Mode

```
sudo hciconfig hci0 noscan 
hciconfig 
hci0:	Type: Primary  Bus: USB
	BD Address: 00:01:95:79:EF:89  ACL MTU: 310:10  SCO MTU: 64:8
	UP RUNNING 
	RX bytes:1290 acl:0 sco:0 events:81 errors:0
	TX bytes:2943 acl:0 sco:0 commands:80 errors:0
```

### PSCAN V ISCAN

* PSCAN enabled allows connections to the interface&#x20;
* ISCAN places the device in discoverable mode&#x20;

#### Place device in discoverable mode but dont accept new connections&#x20;

```
sudo hciconfig hci0 noscan 
sudo hciconfig hci0 pscan 
hciconfig hci0 
sudo hciconfig hci0 noscan 
sudo hciconfig hci0 iscan 
hciconfig hci0
```

* Should see `UP RUNNING ISCAN` in the output of the second `hciconfig hci0` command

#### Restore ability to accept new connections&#x20;

```
sudo hciconfig hci0 piscan
hciconfig hci0
```

* should see `UP RUNNING PSCAN ISCAN`

### Spoofing Device Class

* There are three types of Bluetooth device classes 1-3.&#x20;
* It is important to have the ability to spoof a device in a different class
* Some devices might simply ignore your device if it is of the wrong class.
  * i.e. a headset for phone calls might ignore your device if you are not a phone
  * case by case basis per manufacturer&#x20;
* change the class for a device
* useful site for attaining the codes to act like other devices&#x20;
* [https://bluetooth-pentest.narod.ru/software/bluetooth\_class\_of\_device-service\_generator.html](https://bluetooth-pentest.narod.ru/software/bluetooth\_class\_of\_device-service\_generator.html)

```
hciconfig hci0 class
sudo hciconfig hci0 class 0x3e0100
hciconfig hci0 class
sudo hciconfig hci0 class 0x84010c
hciconfig hci0 class
sudo hciconfig hci0 class 0x050204
hciconfig hci0 class
```

### Scanning for Devices&#x20;

* Basic Scan

```
hcitool -i hci0 scan
Scanning ...
	98:2C:BC:0E:06:8B	BALTIMORE
```

* Detailed Scan&#x20;

```
hcitool -i hci0 scan --info --class
Scanning ...
BD Address:	98:2C:BC:0E:06:8B [mode 1, clkoffset 0x717b]
Device name:	BALTIMORE
Device class:	Computer, Laptop (0x2a410c)
```
