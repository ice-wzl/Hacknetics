### T-Shark User Guide
#### Installation
- See if tshark is installed.
````
tshark
apt list tshark
````
- If it is not installed.
````
sudo apt install tshark
````
- Help menu
````
tshark -h
````
#### Capture Packets with Tshark
````
tshark -i wlan0 -w capture-output.pcap
````
#### Reading a File
````
tshark -r [file-name.cap]
````
- When used with `wc -l` we cann see how mnay packets are in a capture
````
tshark -r [file-name.cap | wc -l]
````
#### Filters 
- Tshark filters are different than bpf syntax.
- If we are interested in DNS A records only we can use:
````
dns.qry.type==1
````
- Display filters are added with the `-Y` switch.
- View all DNS A records:
````
tshark -r [file-name.cap] -Y "dns.qry.type == 1"
````
- DNS requests only in a file:
````
tshark -r [file-name.pcap] -Y "dns.flags.response == 0" | wc -l
````
#### Extracted data
- One way to extract data is using `-T` and `-e [field name]` switches.
- Extract the A records in the pcap, we would use `-T fields -e dns.query.name`.
````
tshark -r dns.cap -Y "dns.qry.type == 1" -T fields -e dns.qry.name
````
- An easy way to identify field names in Wireshark is to navigate to the Packet Details in the capture, highlight the interesting field, then view the bottom left corner.
#### Queries
- See who queried for a particular domain:
````
tshark -r [file-name.pcap] -T fields -e ip.src -e
````
- List all queries
````
tshark -r [file-name.pcap] -T fields -e ip.src -e
````

















