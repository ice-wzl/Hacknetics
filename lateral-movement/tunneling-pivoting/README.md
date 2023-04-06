# Pivoting

![alt text](https://assets.tryhackme.com/additional/wreath-network/6904b85a9b93.png)

## Manual Techniques

* There are two main methods encompassed in this area of pentesting:
* **Tunnelling/Proxying:** Creating a proxy type connection through a compromised machine in order to route all desired traffic into the targeted network. This could potentially also be tunneled inside another protocol (e.g. SSH tunneling), which can be useful for evading a basic Intrusion Detection System (IDS) or firewall
* Port Forwarding: Creating a connection between a local port and a single port on a target, via a compromised host

### Pros and cons

* A proxy is good if we want to redirect lots of different kinds of traffic into our target network -- for example, with an nmap scan, or to access multiple ports on multiple different machines.
* Port Forwarding tends to be faster and more reliable, but only allows us to access a single port (or a small range) on a target device.
* It would be sensible at this point to also start to draw up a layout of the network as you see it
* As a general rule, if you have multiple possible entry-points, try to use a Linux/Unix target where possible, as these tend to be easier to pivot from. An outward facing Linux webserver is absolutely ideal.

### Enumeration

* There are five possible ways to enumerate a network through a compromised host:
* Using material found on the machine. The hosts file or ARP cache, for example
* Using pre-installed tools
* Using statically compiled tools
* Using scripting techniques
* Using local tools through a proxy

## Basic Checks

* Win and Lin see the arp cache

```
arp -a 
```

* Static mapping Lin/Win

```
/etc/hosts 
C:\Windows\System32\drivers\etc\hosts 
```

* Local DNS server (zone transfer?)

```
/etc/resolv.conf 
```

* Lin/Win ip address, interfaces, gateway etc

```
ipconfig /all 
ip addr 
```

* Alternative to reading /etc/resolv.conf

```
nmcli dev show 
```

#### Proxy Note:

* Finally, the dreaded scanning through a proxy. This should be an absolute last resort, as scanning through something like proxychains is very slow, and often limited (you cannot scan UDP ports through a TCP proxy, for example).
* The one exception to this rule is when using the Nmap Scripting Engine (NSE), as the scripts library does not come with the statically compiled version of the tool.
* As such, you can use a static copy of Nmap to sweep the network and find hosts with open ports, then use your local copy of Nmap through a proxy specifically against the found ports.

## LOL Techniques

* The following Bash one-liner would perform a full ping sweep of the `192.168.1.x` network:

```
for i in {1..255}; do (ping -c 1 192.168.1.${i} | grep "bytes from" &); done
```

* The equivalent of this command in Powershell is unbearably slow, so it's better to find an alternative option where possible.
* If you suspect that a host is active but is blocking ICMP ping requests, you could also check some common ports using a tool like netcat.

### Port scanning in bash can be done:

```
for i in {1..65535}; do (echo > /dev/tcp/192.168.1.1/$i) >/dev/null 2>&1 && echo $i is open; done
```

#### Sources

* All credit for this guide goes to:
* https://tryhackme.com/room/wreath
* The THM Room was created by MuirlandOracle, who puts out amazing content. The contents of this .md come from that room. Check it out!
