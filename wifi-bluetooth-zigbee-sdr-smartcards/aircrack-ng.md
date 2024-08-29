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

### Four way Handshake Cracking

* Easy to filter on handshake traffic with `eapol` Wireshark filter
* If you have the 4 way handshake it can be cracked with&#x20;

```
aircrack-ng -w word-list capture_handshake.pcap
```

* if that is failing due to the password not being in the wordlist you can easily add permutation to it&#x20;

```
john -wordlist:word-list -rules -stdout > morewords
```

### hcxpcapngtool for Hashcat

* before being utilizing hashcat to crack to crack a handshake we need to conver it with hcxpcapngtool

```
hcxpcapngtool -o wifi.crackme wifi.pcap
```

* examining the file&#x20;

```
cat wifi.crackme
WPA*01*2f28a275f277d17904ec948e51012bef*586d8f074e8f*a088b4583fa0*4d6f62696c65576946692034453846***
WPA*02*4acfe35de7bc8c44b19ba7bfcf2ce152*586d8f074e8f*a088b4583fa0*4d6f62696c65576946692034453846*
6148801ead3ac326e653a8e5417998245ff5819acd16aee63f0621081325378b*0103007702010a0000000000000000000
288fe22a134055f845914ffa8573f82db7d34f1dd65a12cae4790738a72c3f8ca000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000001830160100000fac040100000fac04010
0000fac023c000000*02
```

* there was only one handshake captured, however we can see two hashes.
* the first one is the PMKID and the second is the the four way handshake hash
* Note: The PMKID hash is outputted to the file even if that AP DOES NOT support PMKID. That means hashcat will never crack the hash if the AP does not support PMKID.
* the PMKID hash can be filtered out&#x20;

```
hcxhashtool -i wifi.crackme --type=2 -o eapolhashonly
```

### Hashcat Mask Attack

* Many AP companies will have passwords with only partial variations, save yourself the time with a mask attack&#x20;

```
hashcat -m 22000 -a 3 mobilewifi.crackme Wifi3E9F-?d?d?d?d?d?d --force
```

* `-m 22000 is for WPA2-PSK`
