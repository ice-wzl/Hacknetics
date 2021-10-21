# Nmap
## Host Discovery
- Scan Type	Example Command
- ARP Scan	`sudo nmap -PR -sn MACHINE_IP/24`
- ICMP Echo Scan	`sudo nmap -PE -sn MACHINE_IP/24`
- ICMP Timestamp Scan	`sudo nmap -PP -sn MACHINE_IP/24`
- ICMP Address Mask Scan	`sudo nmap -PM -sn MACHINE_IP/24`
- TCP SYN Ping Scan	`sudo nmap -PS22,80,443 -sn MACHINE_IP/30`
- TCP ACK Ping Scan	`sudo nmap -PA22,80,443 -sn MACHINE_IP/30`
- UDP Ping Scan	`sudo nmap -PU53,161,162 -sn MACHINE_IP/30`
- Remember to add `-sn` if you are only interested in host discovery without port-scanning. Omitting `-sn` will let Nmap default to port-scanning the live hosts.

### Option	Purpose
- `-n`	no DNS lookup
- `-R`	reverse-DNS lookup for all hosts
- `-sn`	host discovery only

## Port Scan Type	Example Command
- TCP Connect Scan	`nmap -sT MACHINE_IP`
- TCP SYN Scan	`sudo nmap -sS MACHINE_IP`
- UDP Scan	`sudo nmap -sU MACHINE_IP`
- These scan types should get you started discovering running TCP and UDP services on a target host.

### Option	Purpose
- `-p-`	all ports
- `-p1-1023`	scan ports 1 to 1023
- `-F`	100 most common ports
- `-r`	scan ports in consecutive order
- `-T<0-5>`	`-T0` being the slowest and `T5` the fastest
- `--max-rate 50`	rate <= 50 packets/sec
- `--min-rate 15`	rate >= 15 packets/sec
- `--min-parallelism 100`	at least 100 probes in parallel
