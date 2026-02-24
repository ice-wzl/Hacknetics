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

* **Target from file:** `-iL hosts.lst` — read target IPs/hosts from file (one per line).
* **IP range in one octet:** `10.129.2.18-20` — same as 10.129.2.18, 10.129.2.19, 10.129.2.20.

### Option Purpose

* `-n` no DNS lookup
* `-R` reverse-DNS lookup for all hosts
* `-sn` host discovery only
* `-Pn` skip host discovery (treat all hosts as up; use when target blocks ping or for reliable HTB/VPN scans)
* `--disable-arp-ping` use ICMP (or other) instead of ARP for host discovery when on same L2
* `--packet-trace` show all packets sent and received (useful for understanding scan behavior)
* `--reason` show why a port/host is in a given state (e.g. syn-ack, arp-response)

## Port Scan Type Example Command

* TCP Connect Scan `nmap -sT MACHINE_IP`
  * Completes the full TCP 3-way handshake (SYN → SYN-ACK → ACK). Most accurate — gives definitive open/closed/filtered. Creates connection logs on the target so less stealthy, but behaves like a normal client so it is less likely to crash services. Used when Nmap does not have raw packet privileges (non-root).
* TCP SYN Scan `sudo nmap -sS MACHINE_IP`
  * Sends SYN, never completes the handshake. SYN-ACK back = **open**, RST back = **closed**, no response = **filtered**. Default scan when running as root. Stealthier than `-sT` because no full connection is established, minimizing log entries — though modern IDS can still detect it.
* UDP Scan `sudo nmap -sU MACHINE_IP`
  * Stateless — no handshake. Nmap sends empty datagrams; no response = **open|filtered**, ICMP port unreachable = **closed**, application response = **open**. Much slower than TCP scans due to longer timeouts.

### Option Purpose

* `-p-` all ports
* `-p1-1023` scan ports 1 to 1023
* `-p 22,25,80,139,445` comma-separated specific ports
* `--top-ports=10` scan the N most common ports from Nmap's database (default scans top 1000)
* `-F` 100 most common ports
* `-r` scan ports in consecutive order
* `-T<0-5>` timing templates:
  * `-T0` paranoid / `-T1` sneaky / `-T2` polite / `-T3` normal (default) / `-T4` aggressive / `-T5` insane
  * Too aggressive (`-T5`) can miss ports on congested networks or trigger IPS blocks
* `--max-rate 50` rate <= 50 packets/sec
* `--min-rate 15` rate >= 15 packets/sec
* `--min-parallelism 100` at least 100 probes in parallel
* `--max-retries 0` fewer retries = faster scan, may miss ports (default 10).
* `--initial-rtt-timeout 50ms --max-rtt-timeout 100ms` speed up by lowering RTT timeouts; too low can miss hosts/ports.
* `--stats-every=5s` print scan progress every 5s (or `5m`). During a scan, press **Space** to show current status.

### Nmap Results

* `Open`: indicates that a service is listening on the specified port.
* `Closed`: indicates that no service is listening on the specified port, although the port is accessible. By accessible, we mean that it is reachable and is not blocked by a firewall or other security appliances/programs.
* `Filtered`: Nmap cannot determine open or closed. **Dropped** = no response (retries up to `--max-retries`). **Rejected** = target sends e.g. ICMP type 3 code 3 (port unreachable).
* `Unfiltered`: port accessible but open/closed unknown; occurs with ACK scan (`-sA`). ACK scan often bypasses firewalls that block SYN/Connect.
* `Open|Filtered`: no response (common for UDP).
* `Closed|Filtered`: only in IP ID idle scan.
* **UDP:** Closed = ICMP port unreachable (type 3/code 3). No response = open|filtered. Application response = open.

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

### Advanced Options

* `--source-port PORT_NUM` specify source port number
* `--data-length NUM` append random data to reach given length
* `-v` verbose (shows open ports as discovered)
* `-vv` very verbose
* `-d` debugging
* `-dd` more details for debugging
* Null, FIN, and Xmas scans provoke a response from closed ports. Maimon, ACK, and Window scans provoke a response from open and closed ports.

### Subnet enumeration&#x20;

```
user@slingshot:~$ nmap -n -sn 10.130.10.0/24 --packet-trace

Starting Nmap 7.60 ( https://nmap.org )
SENT (0.0509s) ICMP [10.254.252.2 > 10.130.10.1 Echo request (type=8/code=0) id=65308 seq=0] IP [ttl=44 id=3373 iplen=28 ]
SENT (0.0513s) ICMP [10.254.252.2 > 10.130.10.2 Echo request (type=8/code=0) id=27237 seq=0] IP [ttl=37 id=41108 iplen=28 ]
SENT (0.0517s) ICMP [10.254.252.2 > 10.130.10.3 Echo request (type=8/code=0) id=64932 seq=0] IP [ttl=37 id=40840 iplen=28 ]
SENT (0.0520s) ICMP [10.254.252.2 > 10.130.10.4 Echo request (type=8/code=0) id=45780 seq=0] IP [ttl=59 id=29404 iplen=28 ]

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
sudo nmap 10.129.2.28 -p 25 --script banner,smtp-commands
sudo nmap 10.129.2.28 -p 80 -sV --script vuln
```

* `--script banner,smtp-commands` grabs the service banner and enumerates SMTP commands — useful for identifying OS/distro from the SMTP greeting.
* `--script vuln` runs all vuln-category scripts against the target; combine with `-sV` so scripts have version info to match against CVE databases.

## NSE + Output

* Option Meaning
* `-sV` determine service/version info on open ports
* `-sV --version-light` try the most likely probes (2)
* `-sV --version-all` try all available probes (9)
* If `-sV` truncates the banner, use manual `nc` + `tcpdump` to capture the full banner (see [Banner Grabbing](../recon-enumeration/banner-grabbing.md)).
* `-O` detect OS
* `--traceroute` run traceroute to target
* `--script=SCRIPTS` Nmap scripts to run
* `-sC` or `--script=default` run default scripts
* `-A` equivalent to -sV -O -sC --traceroute
* `-oN` save output in normal format
* `-oG` save output in grepable format
* `-oX` save output in XML format
* `-oA` save output in normal, XML and Grepable formats
* **HTML report:** `xsltproc target.xml -o target.html` — convert XML to readable HTML for reporting.

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

## Firewall and IDS/IPS Evasion

### ACK Scan for Firewall Detection

* `-sA` sends only the ACK flag. Firewalls often allow ACK packets through because they cannot tell whether the connection was initiated internally or externally — ACK looks like part of an established session.
* Result: **unfiltered** (RST received — port is accessible through the firewall) or **filtered** (no response / ICMP error — firewall is blocking).
* ACK scan does **not** distinguish open from closed — it only reveals firewall rules.

```
# SYN scan shows filtered (firewall blocks SYN)
sudo nmap 10.129.2.28 -p 21,22,25 -sS -Pn -n --disable-arp-ping --packet-trace

# ACK scan on same ports — may show unfiltered where SYN was blocked
sudo nmap 10.129.2.28 -p 21,22,25 -sA -Pn -n --disable-arp-ping --packet-trace
```

### Decoy Scan

* `-D RND:5` generates 5 random source IPs and mixes your real IP among them, making it harder to identify the true scanner in logs.
* Decoy IPs must be alive hosts; otherwise SYN-flood protections may drop all traffic.

```
sudo nmap 10.129.2.28 -p 80 -sS -Pn -n --disable-arp-ping --packet-trace -D RND:5
```

### Source IP and Interface Spoofing

* `-S 10.129.2.200` sets the source IP — useful for testing whether a different subnet bypasses firewall rules.
* `-e tun0` forces Nmap to send through a specific network interface (required when spoofing source IP).

```
sudo nmap 10.129.2.28 -n -Pn -p 445 -O -S 10.129.2.200 -e tun0
```

### DNS Source Port Evasion

* Firewalls often trust traffic from `TCP/UDP port 53` (DNS). Using `--source-port 53` can bypass poorly configured firewalls.
* `--dns-server <ns>,<ns>` lets you specify custom DNS servers — useful in a DMZ where the company's internal DNS is more trusted.

```
# Port appears filtered with normal source port
sudo nmap 10.129.2.28 -p50000 -sS -Pn -n --disable-arp-ping --packet-trace

# Same port now open when scanning from source port 53
sudo nmap 10.129.2.28 -p50000 -sS -Pn -n --disable-arp-ping --packet-trace --source-port 53
```

* Once you confirm source port 53 bypasses the firewall, connect directly with ncat:

```
ncat -nv --source-port 53 10.129.2.28 50000
```
