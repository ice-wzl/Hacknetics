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

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

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
