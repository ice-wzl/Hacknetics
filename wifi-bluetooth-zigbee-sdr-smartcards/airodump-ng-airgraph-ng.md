# Airodump-ng Airgraph-ng

* with a packet capture you can map client probe requests.
* this can be useful if conducting an Evil-Twin attack
* Before using Airgraph-ng you need to process your libpcap file into a compatible format

```
airodump-ng -r client-probe.pcap -w CUST
```

* you will have a file called `CUST-01.csv`
* feel that into Airgraph-ng&#x20;

```
airgraph-ng -i CUST-01.csv -o cpb.png -g CPG
```

* open the resulting .png with firefox&#x20;

```
firefox cpb.png
```

#### If you are using Kismet

Ensure you add a `--old-pcap` switch to convert the kismetdb to old school pcap, not pcap-ng, which is not supported by airodump-ng.

```
sudo kismetdb_to_pcap --old-pcap -i Kismet-20240829-01-41-41-1.kismet -o out.pcap
Done...
```
