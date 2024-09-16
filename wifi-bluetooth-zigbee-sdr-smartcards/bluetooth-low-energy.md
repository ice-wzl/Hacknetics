# Bluetooth Low Energy

* In order to interact with bluetooth low energy ensure you configure your dongle to be in low energy mode

```
# verify dongle is detected and in up state
hciconfig
# set to low energy mode
sudo btmgmt le on 
hci0 Set Low Energy complete, settings: powered ssp br/edr le secure-conn 
```

* if you have to unplug the adapter for any reason you will need to set le mode again and ensure device is in an up state&#x20;

```
sudo hciconfig hci0 up
sudo btmgmt le on
```

### Scanning for BLE devices&#x20;

* when the scan occurs we will be flooded with information as it will scan on all three channels and advertisements happen frequently.&#x20;
* Look for unique addresses, easy to bash script

```
sudo hcitool -i hci0 lescan
4C:CE:83:6B:73:1D (unknown)
D8:3A:DD:95:26:78 (unknown)
D8:3A:DD:95:26:78 tens
30:C6:F7:9D:09:BA 51c7928b
```

* you can also capture to a file and then `uniq -c`

```
sudo hcitool -i hci0 lescan > lescan.txt
cat lescan.txt | sort | uniq -c
```

### GATT Tool to Connect to Devices

```
gatttool lecc -t public -i hci0 -b D8:3A:DD:95:26:78 -I
```

| `lecc`    |            | Perform a BLE, instead of Classic, connection.                                                 |
| --------- | ---------- | ---------------------------------------------------------------------------------------------- |
| `-t`      | `public`   | Use the BLE adapter's publicly assigned manufacturer assigned BLE address.                     |
| `-i`      | `hci0`     | The BLE adapter device descriptor.                                                             |
| `-b`      | `*BDADDR*` | The BDADDR of the victim BLE device, D8:3A:DD:95:26:78 for the purposes of this demonstration. |
| `-I`      |            | Enter gatttool in interactive mode.                                                            |
| `connect` |            | Connect to the specified device from the interactive session.                                  |
| `primary` |            | Get the primary UUID's ("services") on the device.                                             |

```
[D8:3A:DD:95:26:78][LE]> connect
Attempting to connect to D8:3A:DD:95:26:78
Connection successful
[D8:3A:DD:95:26:78][LE]> primary
attr handle: 0x0001, end grp handle: 0x0005 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x0006, end grp handle: 0x0009 uuid: 00001801-0000-1000-8000-00805f9b34fb
attr handle: 0x000a, end grp handle: 0x001a uuid: f000aa65-0451-4000-b000-000000000000
[D8:3A:DD:95:26:78][LE]> characteristics
handle: 0x0002, char properties: 0x02, char value handle: 0x0003, uuid: 00002a00-0000-1000-8000-00805f9b34fb
handle: 0x0004, char properties: 0x02, char value handle: 0x0005, uuid: 00002a01-0000-1000-8000-00805f9b34fb
handle: 0x0007, char properties: 0x20, char value handle: 0x0008, uuid: 00002a05-0000-1000-8000-00805f9b34fb
handle: 0x000b, char properties: 0x1a, char value handle: 0x000c, uuid: 00000054-0000-1000-8000-00805f9b34fb
handle: 0x000f, char properties: 0x1a, char value handle: 0x0010, uuid: 00000055-0000-1000-8000-00805f9b34fb
handle: 0x0013, char properties: 0x1a, char value handle: 0x0014, uuid: 00000056-0000-1000-8000-00805f9b34fb
handle: 0x0017, char properties: 0x1a, char value handle: 0x0018, uuid: 00000057-0000-1000-8000-00805f9b34fb
```

* you can see `0x0001` for the first attr handle and the individual values for the service end at address `0x0005` meaning there are 5 values for that service
* for the second attr handle: `0x06` through `0x09` represents 4 service values.

### Documentation for GATT Services

{% embed url="https://btprodspecificationrefs.blob.core.windows.net/assigned-numbers/Assigned%20Number%20Types/Assigned_Numbers.pdf" %}

* Good reference page&#x20;

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

### Interacting with Services

```
gatttool lecc -t public -i hci0 -b D8:3A:DD:95:26:78 -I
[D8:3A:DD:95:26:78][LE]> connect
Attempting to connect to D8:3A:DD:95:26:78
Connection successful
[D8:3A:DD:95:26:78][LE]> primary
attr handle: 0x0001, end grp handle: 0x0005 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x0006, end grp handle: 0x0009 uuid: 00001801-0000-1000-8000-00805f9b34fb
attr handle: 0x000a, end grp handle: 0x001a uuid: f000aa65-0451-4000-b000-000000000000
[D8:3A:DD:95:26:78][LE]> characteristics
handle: 0x0002, char properties: 0x02, char value handle: 0x0003, uuid: 00002a00-0000-1000-8000-00805f9b34fb
handle: 0x0004, char properties: 0x02, char value handle: 0x0005, uuid: 00002a01-0000-1000-8000-00805f9b34fb
handle: 0x0007, char properties: 0x20, char value handle: 0x0008, uuid: 00002a05-0000-1000-8000-00805f9b34fb
handle: 0x000b, char properties: 0x1a, char value handle: 0x000c, uuid: 00000054-0000-1000-8000-00805f9b34fb
handle: 0x000f, char properties: 0x1a, char value handle: 0x0010, uuid: 00000055-0000-1000-8000-00805f9b34fb
handle: 0x0013, char properties: 0x1a, char value handle: 0x0014, uuid: 00000056-0000-1000-8000-00805f9b34fb
handle: 0x0017, char properties: 0x1a, char value handle: 0x0018, uuid: 00000057-0000-1000-8000-00805f9b34fb
[D8:3A:DD:95:26:78][LE]> char-read-uuid 2a00
handle: 0x0003 	 value: 70 69 70 6f 69 6e 74 
```

* convert the response from hex to ascii

```
echo '72 69 70 6f 69 6b 72' | xxd -p -r
```

### Enumerate Range of Service handles

```
[D8:3A:DD:95:26:78][LE]> primary
attr handle: 0x0001, end grp handle: 0x0005 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x0006, end grp handle: 0x0009 uuid: 00001801-0000-1000-8000-00805f9b34fb
attr handle: 0x000a, end grp handle: 0x001a uuid: f000aa65-0451-4000-b000-000000000000
[D8:3A:DD:95:26:78][LE]> char-read-hnd 0x00a
Characteristic value/descriptor: 00 00 00 00 00 00 00 b0 00 40 51 04 65 aa 00 f0 
[D8:3A:DD:95:26:78][LE]> char-read-hnd 0x00b
Characteristic value/descriptor: 1a 0c 00 54 00 
```

* we can iterate through this enumeration command from `0x000a to 0x001a`

```
char-read-hnd 0x00e
Characteristic value/descriptor: 54 75 72 6e 73 20 74 68 65 20 75 6e 69 74 20 6f 6e 2f 6f 66 66
echo 54 75 72 6e 73 20 74 68 65 20 75 6e 69 74 20 6f 6e 2f 6f 66 666' | xxd -p -r
Turns the unit on/off
```

### Writing to a Device

* after enumerating the handles and getting the values with `char-read-hnd` we can write values altering the settings of the device

```
characteristics
handle: 0x0002, char properties: 0x02, char value handle: 0x0003, uuid: 00002a00-0000-1000-8000-00805f9b34fb
handle: 0x0004, char properties: 0x02, char value handle: 0x0005, uuid: 00002a01-0000-1000-8000-00805f9b34fb
handle: 0x0007, char properties: 0x20, char value handle: 0x0008, uuid: 00002a05-0000-1000-8000-00805f9b34fb
handle: 0x000b, char properties: 0x1a, char value handle: 0x000c, uuid: 00000054-0000-1000-8000-00805f9b34fb
handle: 0x000f, char properties: 0x1a, char value handle: 0x0010, uuid: 00000055-0000-1000-8000-00805f9b34fb
handle: 0x0013, char properties: 0x1a, char value handle: 0x0014, uuid: 00000056-0000-1000-8000-00805f9b34fb
handle: 0x0017, char properties: 0x1a, char value handle: 0x0018, uuid: 00000057-0000-1000-8000-00805f9b34fb

[D8:3A:DD:95:26:78][LE]> char-read-hnd 0x000c
Characteristic value/descriptor: 00 
[D8:3A:DD:95:26:78][LE]> char-write-req 000c 01
Characteristic value was written successfully
[D8:3A:DD:95:26:78][LE]> char-read-hnd 0x000c
Characteristic value/descriptor: 01 
```

### BLE Fuzzing&#x20;

* we can use `blefuzz` to fuzz ble
* script does not accept cmdline args, all manual data input

```
./blefuzzV21.sh
Enter Bluetooth Address (eg. 00:00:00:00:00:00) : D8:3A:DD:95:26:78
Is the Address is Random? Enter '-t random' : 
Characteristics Read
handle = 0x0002, char properties = 0x02, char value handle = 0x0003, uuid = 00002a00-0000-1000-8000-00805f9b34fb
handle = 0x0004, char properties = 0x02, char value handle = 0x0005, uuid = 00002a01-0000-1000-8000-00805f9b34fb
handle = 0x0007, char properties = 0x20, char value handle = 0x0008, uuid = 00002a05-0000-1000-8000-00805f9b34fb
handle = 0x000b, char properties = 0x1a, char value handle = 0x000c, uuid = 00000054-0000-1000-8000-00805f9b34fb
handle = 0x000f, char properties = 0x1a, char value handle = 0x0010, uuid = 00000055-0000-1000-8000-00805f9b34fb
handle = 0x0013, char properties = 0x1a, char value handle = 0x0014, uuid = 00000056-0000-1000-8000-00805f9b34fb
handle = 0x0017, char properties = 0x1a, char value handle = 0x0018, uuid = 00000057-0000-1000-8000-00805f9b34fb
Profile Read
attr handle = 0x0001, end grp handle = 0x0005 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle = 0x0006, end grp handle = 0x0009 uuid: 00001801-0000-1000-8000-00805f9b34fb
attr handle = 0x000a, end grp handle = 0x001a uuid: f000aa65-0451-4000-b000-000000000000
sleep 5
Start Basic Device Configuration Read
Client Configuration Characteristic
handle: 0x0009 	 value: 00 00 
Server Configuration Characteristic
Basic Device Configuration Read Completed
--snip--
```

* modify this script to perform write operations

<pre><code><strong>cp blefuzzV21.sh blefuzz-write.sh
</strong>vim blefuzz-write.sh
</code></pre>

* at the bottom you will see a large amount of read commands, you can modify to `--char-write` and `--char-write-req` using `-a` to specify the handle and `-n` to specify the value to write.
* you can now automate any testing you want to perform.

### Reverse Engineering BLE

* many bluetooth le devices have an android and ios application which is utilized to control the device.
* we should use the target application (android apps are better as they can be downloaded from APK Monk)

{% embed url="https://www.apkmonk.com/" %}

* we can use JadX to reconstruct the Java source code.

{% embed url="https://github.com/skylot/jadx" %}

* with the source code up search for strings&#x20;
  * `BluetoothGattCallback`
  * `BluetoothGattDescriptor`
  * `Bluetooth`

### Reverse Engineering BLE with PCAP

* Android devices can dump all hci commands to a log file and the traffic can be captured in Wireshark
* Turn on the `HCI capture feature in Android`
  * It is under the developer options, can exfil the file with ADB or just email it to yourself.
* after opening pcap, filter on `btatt`
  * `this will show us the bluetooth attribute protocol`&#x20;
* it is all the data send and recieved between the ble device and the app&#x20;
* filter on the read request opcode `btatt.opcode == 0x0a`
* filter on the write request opcode `btatt.opcode == 0x12`
* it is simple to derive the valid handles this way&#x20;
* can also use tshark&#x20;

```
tshark -r app-hci.log -Y "btatt.opcode == 0x12"
tshark -r app-hci.log -Y "btatt.opcode == 0x12" -z proto,colinfo,btatt.value,btatt.value
   4   1.118400 localhost () → remote ()    ATT 13 Sent Write Request, Handle: 0x004d (Unknown)  btatt.value == 08
   14   5.834189 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:ff:02:00
   17   6.056926 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0031 (Unknown)  btatt.value == 41:87:20:20
   20   6.303084 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 41:87:20:20
# you can now awk on the column you want and count them 
# count the write requests
tshark -r app-hci.log -Y "btatt.opcode == 0x12" -z proto,colinfo,btatt.value,btatt.value | awk '{print $14}' | sort | uniq -c
     23 0x002a
     46 0x002e
     23 0x0031
     23 0x0034
      1 0x004d
# filter on a specific handle 
tshark -r app-hci.log -Y "btatt.opcode == 0x12 and btatt.handle == 0x002a" -z proto,colinfo,btatt.value,btatt.value
   23   6.557132 localhost () → remote ()    ATT 13 Sent Write Request, Handle: 0x002a (Unknown)  btatt.value == 06
  110  11.042753 localhost () → remote ()    ATT 13 Sent Write Request, Handle: 0x002a (Unknown)  btatt.value == 06
  125  17.661276 localhost () → remote ()    ATT 13 Sent Write Request, Handle: 0x002a (Unknown)  btatt.value == 06
  140  24.145688 localhost () → remote ()    ATT 13 Sent Write Request, Handle: 0x002a (Unknown)  btatt.value == 06
  155  29.658901 localhost () → remote ()    ATT 13 Sent Write Request, Handle: 0x002a (Unknown)  btatt.value == 06
  170  34.281215 localhost () → remote ()    ATT 13 Sent Write Request, Handle: 0x002a (Unknown)  btatt.value == 06
  
```

* in the last above command we can see the value `btatt.value` always is 06. so we can rule that out as a handle that controls a device setting. find the values that are different as those are likely the setting changes
* to find these values see which wireshark `btatt.value` changes per packet
  * if handle `0x0031` has the same `btatt.value` each time, rule it out. look for ones where the data value in `btatt.value` changes each time or frequently
* awk for your handles and then iterate through the last tshark command seeing the values and if they seem to be different alot

### Reverse Engineering TSHARK HCI Summary&#x20;

* awk for the handles, iterate through them see the changing values
* `head` was used to save space, dont do this in real life, you might miss stuff...

```
tshark -r app-hci.log -Y "btatt.opcode == 0x12" -z proto,colinfo,btatt.value,btatt.value | awk '{print $14}' | sort | uniq -c
     23 0x002a
     46 0x002e
     23 0x0031
     23 0x0034
      1 0x004d
tshark -r app-hci.log -Y "btatt.opcode == 0x12 and btatt.handle == 0x002e" -z proto,colinfo,btatt.value,btatt.value | head
   20   6.303084 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 41:87:20:20
   26   6.647561 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 82:c3:0f:0f
  107  10.767957 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 41:87:20:20
  113  11.119934 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 82:c3:0f:0f
  122  17.397355 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 41:87:20:20
  128  17.773057 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 82:c3:0f:0f
  137  23.879547 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 41:87:20:20
  143  24.240349 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 82:c3:0f:0f
  152  29.416673 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 41:87:20:20
  158  29.771678 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x002e (Unknown)  btatt.value == 82:c3:0f:0f
tshark -r app-hci.log -Y "btatt.opcode == 0x12 and btatt.handle == 0x0034" -z proto,colinfo,btatt.value,btatt.value | head
   14   5.834189 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:ff:02:00
  101  10.299287 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:0a:02:00
  116  16.936518 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:20:02:00
  131  23.402051 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:40:02:00
  146  28.941775 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:55:02:00
  161  33.497028 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:70:02:00
  176  44.376252 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:80:02:00
  191  48.216134 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:90:02:00
  206  52.516285 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:a0:02:00
  221  56.205962 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:b0:02:00
tshark -r app-hci.log -Y "btatt.opcode == 0x12 and btatt.handle == 0x0034" -z proto,colinfo,btatt.value,btatt.value
   14   5.834189 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:ff:02:00
  101  10.299287 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:0a:02:00
  116  16.936518 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:20:02:00
  131  23.402051 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:40:02:00
  146  28.941775 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:55:02:00
  161  33.497028 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:70:02:00
  176  44.376252 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:80:02:00
  191  48.216134 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:90:02:00
  206  52.516285 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:a0:02:00
  221  56.205962 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:b0:02:00
  236  59.983711 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:c0:02:00
  251  62.987032 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:ff:02:00
  266  68.260189 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:0a:01:00
  281  72.793182 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:20:01:00
  296  77.914534 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:40:01:00
  311  81.261032 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:55:01:00
  326  89.449411 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:70:01:00
  341  95.427576 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:80:01:00
  356  98.125358 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:90:01:00
  371 103.532286 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:a0:01:00
  386 107.267313 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:b0:01:00
  401 110.924918 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:c0:01:00
  416 114.065336 localhost () → remote ()    ATT 16 Sent Write Request, Handle: 0x0034 (Unknown)  btatt.value == 41:ff:01:00
```

* `0x0034` is the handle we want!
