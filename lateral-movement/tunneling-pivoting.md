# Pivoting 
![alt text](https://assets.tryhackme.com/additional/wreath-network/6904b85a9b93.png)
## Manual Techniques 
- There are two main methods encompassed in this area of pentesting:
- Tunnelling/Proxying: Creating a proxy type connection through a compromised machine in order to route all desired traffic into the targeted network. This could potentially also be tunnelled inside another protocol (e.g. SSH tunnelling), which can be useful for evading a basic Intrusion Detection System (IDS) or firewall
- Port Forwarding: Creating a connection between a local port and a single port on a target, via a compromised host
#### Pros and cons
- A proxy is good if we want to redirect lots of different kinds of traffic into our target network -- for example, with an nmap scan, or to access multiple ports on multiple different machines.
- Port Forwarding tends to be faster and more reliable, but only allows us to access a single port (or a small range) on a target device.
- It would be sensible at this point to also start to draw up a layout of the network as you see it
- As a general rule, if you have multiple possible entry-points, try to use a Linux/Unix target where possible, as these tend to be easier to pivot from. An outward facing Linux webserver is absolutely ideal.
#### Enumeration
- There are five possible ways to enumerate a network through a compromised host:
- Using material found on the machine. The hosts file or ARP cache, for example
- Using pre-installed tools
- Using statically compiled tools
- Using scripting techniques
- Using local tools through a proxy
### Basic Checks
````
arp -a #Win and Lin see the arp cache
/etc/hosts #static mapping Lin
C:\Windows\System32\drivers\etc\hosts #Static mapping Win
/etc/resolv.conf #Local DNS server (zone transfer?)
ipconfig /all #Win ip address, interfaces, gateway etc
ip addr #Lin ip addresses, interfaces, gateway etc
nmcli dev show #Alternative to reading /etc/resolv.conf
````





































































































