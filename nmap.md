# OSCP-Prep
###Nmap
####Basic Usage
#####Aggressive scan (-A), as fast as possible (-T5), port (-p), range (1-10000)
`nmap -A -T5 172.16.6.1 -p 1-100000`
#####Other Scan Flags
#####TCP Syn Scan 
Default and most popular.  Fast, never completes the TCP connections. Clear and reliable, half open scanning.
`nmap -sS -T3 172.16.6.1`
#####TCP Connect Scan
`nmap -sT -T2 172.16.6.1`
Default TCP scan when Syn Scan is not an option. When a user does not have raw packet privlages. Completes the connection, target machine is more likely to log the connection.
#####UDP Scan 
`nmap -sU 172.16.6.1 -T1`
UDP Scan, DNS, SNMP, DHCP 53, 161/162, 67/68 most common UDP ports. Sends a UDP packet to every targeted host, for common ports a protocol specific payload is sent to increase response rate. -sV can be added to help differentiate the truly open from filtered ports. Full scan of a host and all ports can take 18 hours, scan the popular ports, scan from behind the firewall, and use `--host-timeout` to skip slow hosts.
#####Null Scan, Fin Scan, Xmas Scan
`-sN` Null Scan 
`-sF` Fin Scan
`-sX` Xmas Scan
Can sneak through certain non-stateful firewalls and packet filtering routers.  More stealthy than even the SYN scan. Non RFC 793 complient system and will send a RST back whether the port is closed or open, this will cause all ports to be labeled closed. Cannot distinguish between `open` versus `filtered` leaving the label `open | filtered`
#####TCP ACK Scan
`nmap -sA 172.16.6.1` 
Never determines `open` or even `open | filtered` Used to map out firewall rulesets, determining wether they are stateful or not and which ports are filtered. The ACK scan probe only has the ACK flag set unless you use `--scanflags` Unfiltered systems, `open` and `closed` ports will both return a RST packet. Nmap then labels them as `unfiltered` meaning they are reachable by the ACK, whether they are `open` or `closed` is undetermined.
