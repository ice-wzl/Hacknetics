# Nmap

## Host Discovery

* Scan Type Example Command
* ARP Scan `sudo nmap -PR -sn MACHINE_IP/24`
* ICMP Echo Scan `sudo nmap -PE -sn MACHINE_IP/24`
* ICMP Timestamp Scan `sudo nmap -PP -sn MACHINE_IP/24`
* ICMP Address Mask Scan `sudo nmap -PM -sn MACHINE_IP/24`
* TCP SYN Ping Scan `sudo nmap -PS22,80,443 -sn MACHINE_IP/30`
* TCP ACK Ping Scan `sudo nmap -PA22,80,443 -sn MACHINE_IP/30`
* UDP Ping Scan `sudo nmap -PU53,161,162 -sn MACHINE_IP/30`
* Remember to add `-sn` if you are only interested in host discovery without port-scanning. Omitting `-sn` will let Nmap default to port-scanning the live hosts.

### Option Purpose

* `-n` no DNS lookup
* `-R` reverse-DNS lookup for all hosts
* `-sn` host discovery only
* `-Pn` skip host discovery (treat all hosts as up; use when target blocks ping or for reliable HTB/VPN scans)

## Port Scan Type Example Command

* TCP Connect Scan `nmap -sT MACHINE_IP`
* TCP SYN Scan `sudo nmap -sS MACHINE_IP`
* UDP Scan `sudo nmap -sU MACHINE_IP`
* These scan types should get you started discovering running TCP and UDP services on a target host.

### Option Purpose

* `-p-` all ports
* `-p1-1023` scan ports 1 to 1023
* `-F` 100 most common ports
* `-r` scan ports in consecutive order
* `-T<0-5>` `-T0` being the slowest and `T5` the fastest
* `--max-rate 50` rate <= 50 packets/sec
* `--min-rate 15` rate >= 15 packets/sec
* `--min-parallelism 100` at least 100 probes in parallel

### Nmap Results

* `Open`: indicates that a service is listening on the specified port.
* `Closed`: indicates that no service is listening on the specified port, although the port is accessible. By accessible, we mean that it is reachable and is not blocked by a firewall or other security appliances/programs.
* `Filtered`: means that Nmap cannot determine if the port is open or closed because the port is not accessible. This state is usually due to a firewall preventing Nmap from reaching that port. Nmap’s packets may be blocked from reaching the port; alternatively, the responses are blocked from reaching Nmap’s host.
* `Unfiltered`: means that Nmap cannot determine if the port is open or closed, although the port is accessible. This state is encountered when using an ACK scan -sA.
* `Open|Filtered`: This means that Nmap cannot determine whether the port is open or filtered.
* `Closed|Filtered`: This means that Nmap cannot decide whether a port is closed or filtered.

## Nmap Advanced Scanning

### Port Scan Type Example Command

* TCP Null Scan `sudo nmap -sN MACHINE_IP`
* TCP FIN Scan `sudo nmap -sF MACHINE_IP`
* TCP Xmas Scan `sudo nmap -sX MACHINE_IP`
* Three above scan types can be efficient when scanning a target behind a stateless (non-stateful) firewall. A stateless firewall will check if the incoming packet has the SYN flag set to detect a connection attempt. Using a flag combination that does not match the SYN packet makes it possible to deceive the firewall and reach the system behind it.
* TCP Maimon Scan `sudo nmap -sM MACHINE_IP`
* TCP ACK Scan `sudo nmap -sA MACHINE_IP`
* TCP Window Scan `sudo nmap -sW MACHINE_IP`
* Custom TCP Scan `sudo nmap --scanflags URGACKPSHRSTSYNFIN MACHINE_IP`
* Spoofed Source IP `sudo nmap -S SPOOFED_IP MACHINE_IP`
* Spoofed MAC Address `--spoof-mac SPOOFED_MAC`
* Decoy Scan `nmap -D DECOY_IP,ME MACHINE_IP`
* Idle (Zombie) Scan `sudo nmap -sI ZOMBIE_IP MACHINE_IP`
* Fragment IP data into 8 bytes `-f`
* Fragment IP data into 16 bytes `-ff`

### Option Purpose

* `--source-port PORT_NUM` specify source port number
* `--data-length NUM` append random data to reach given length
* These scan types rely on setting TCP flags in unexpected ways to prompt ports for a reply. Null, FIN, and Xmas scan provoke a response from closed ports, while Maimon, ACK, and Window scans provoke a response from open and closed ports.

### Option Purpose

* `--reason` explains how Nmap made its conclusion
* `-v` verbose
* `-vv` very verbose
* `-d` debugging
* `-dd` more details for debugging

### Subnet enumeration&#x20;

```
user@slingshot:~$ nmap -n -sn 10.130.10.0/24 --packet-trace

Starting Nmap 7.60 ( https://nmap.org )
SENT (0.0509s) ICMP [10.254.252.2 > 10.130.10.1 Echo request (type=8/code=0) id=65308 seq=0] IP [ttl=44 id=3373 iplen=28 ]
SENT (0.0513s) ICMP [10.254.252.2 > 10.130.10.2 Echo request (type=8/code=0) id=27237 seq=0] IP [ttl=37 id=41108 iplen=28 ]
SENT (0.0517s) ICMP [10.254.252.2 > 10.130.10.3 Echo request (type=8/code=0) id=64932 seq=0] IP [ttl=37 id=40840 iplen=28 ]
SENT (0.0520s) ICMP [10.254.252.2 > 10.130.10.4 Echo request (type=8/code=0) id=45780 seq=0] IP [ttl=59 id=29404 iplen=28 ]

```

* `--packet-trace` will show you the enumeration packets sent out&#x20;

### Top 3000 Packets

* By default nmap will scan the top 1000 ports, if you dont want to scan all 65536 ports but want to scan more than just 1000 you can scan 3000 like seen below&#x20;

```
sudo nmap -n -sT 10.130.10.33 --top-ports 3000
```

### TCP Header

![tcp-header](https://user-images.githubusercontent.com/75596877/138295680-a20a687e-6898-4b7a-8c6b-d3e496ff6c07.png)

## NSE

### Script Category Description

* `auth` Authentication related scripts
* `broadcast` Discover hosts by sending broadcast messages
* `brute` Performs brute-force password auditing against logins
* `default` Default scripts, same as -sC
* `discovery` Retrieve accessible information, such as database tables and DNS names
* `dos` Detects servers vulnerable to Denial of Service (DoS)
* `exploit` Attempts to exploit various vulnerable services
* `external` Checks using a third-party service, such as Geoplugin and Virustotal
* `fuzzer` Launch fuzzing attacks
* `intrusive` Intrusive scripts such as brute-force attacks and exploitation
* `malware` Scans for backdoors
* `safe` Safe scripts that won’t crash the target
* `version` Retrieve service versions
* `vuln` Checks for vulnerabilities or exploit vulnerable services

### Run Scripts

```
nmap --script "http*" 10.10.10.10
nmap --script "ssh2-enum-algos" 10.10.220.56
```

## NSE + Output

* Option Meaning
* `-sV` determine service/version info on open ports
* `-sV --version-light` try the most likely probes (2)
* `-sV --version-all` try all available probes (9)
* `-O` detect OS
* `--traceroute` run traceroute to target
* `--script=SCRIPTS` Nmap scripts to run
* `-sC` or `--script=default` run default scripts
* `-A` equivalent to -sV -O -sC --traceroute
* `-oN` save output in normal format
* `-oG` save output in grepable format
* `-oX` save output in XML format
* `-oA` save output in normal, XML and Grepable formats

### Quick / full scan pattern

```bash
# Quick: default ports, scripts, version
nmap -sC -sV -Pn TARGET_IP -oA nmap/nmap.quick

# Full: all ports
nmap -sC -sV -Pn TARGET_IP -p- -oA nmap/nmap.full
```

### Searching Through Output&#x20;

* Looking for open port 445 in nmap output and returning ips&#x20;

```
grep ' 445/open/' /tmp/scan.gnmap | cut -d ' ' -f 2
10.130.10.4
10.130.10.5
10.130.10.6
10.130.10.21
10.130.10.25
10.130.10.33
10.130.10.44
10.130.10.45
```
