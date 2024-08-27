# Airdecap-ng

**Decrypting Traffic with Airdecap-ng**

* Tool takes an input libpcap file of WEP-encrypted content and the WEP key, generating an output file of unencrypted content (`airdecap-ng` also supports WPA-PSK packet captures, with some caveats

```
airdecap-ng -w E1:26:9E:1D:19:2A:C7:1B:9F:33:53:55:54 wep.pcap
```

* output file will be the input file name with `-dec.pcap` at the end&#x20;
