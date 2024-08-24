# Aircrack-ng

### Aircrack-ng WEP Attack

* understand your pcap&#x20;

```
capinfos wep.pcap
aircrack-ng wep.pcap
```

* it will prompt you to select the network, and then it will try to recover the key
* if your attack is successful the key will look something like this&#x20;

```
E1:26:9E:0F:19:4A:A7:2A:9D:32:53:53:52
```

### WEP Key Decrypt Wireshark Capture

* with key in hand go to: **Edit | Preferences**
* **Expand Protocols tree**, and then scroll and select the **IEEE 802.11**

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

* Make sure the Wireshark **Ignore the Protection bit** option is set to No.
* Make sure **Enable decryption** is selected
* To specify a key to use in decryption, click the **Edit...** button to open the WEP and WPA Decryption Keys dialog

<figure><img src="../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

* add your key by pressing the `+` button
* Hit Ok twice and your packets will be decrypted&#x20;
