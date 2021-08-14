# Pivoting 
![alt text](https://assets.tryhackme.com/additional/wreath-network/6904b85a9b93.png)
## Manual Techniques 
- There are two main methods encompassed in this area of pentesting:
- Tunnelling/Proxying: Creating a proxy type connection through a compromised machine in order to route all desired traffic into the targeted network. This could potentially also be tunnelled inside another protocol (e.g. SSH tunnelling), which can be useful for evading a basic Intrusion Detection System (IDS) or firewall
- Port Forwarding: Creating a connection between a local port and a single port on a target, via a compromised host
### Pros and cons
- A proxy is good if we want to redirect lots of different kinds of traffic into our target network -- for example, with an nmap scan, or to access multiple ports on multiple different machines.
- Port Forwarding tends to be faster and more reliable, but only allows us to access a single port (or a small range) on a target device.
- It would be sensible at this point to also start to draw up a layout of the network as you see it
- As a general rule, if you have multiple possible entry-points, try to use a Linux/Unix target where possible, as these tend to be easier to pivot from. An outward facing Linux webserver is absolutely ideal.
### Enumeration
- There are five possible ways to enumerate a network through a compromised host:
- Using material found on the machine. The hosts file or ARP cache, for example
- Using pre-installed tools
- Using statically compiled tools
- Using scripting techniques
- Using local tools through a proxy
## Basic Checks
- Win and Lin see the arp cache
````
arp -a 
````
- Static mapping Lin/Win
````
/etc/hosts 
C:\Windows\System32\drivers\etc\hosts 
````
- Local DNS server (zone transfer?)
````
/etc/resolv.conf 
````
- Lin/Win ip address, interfaces, gateway etc
````
ipconfig /all 
ip addr 
````
- Alternative to reading /etc/resolv.conf
````
nmcli dev show 
````
#### Proxy Note:
- Finally, the dreaded scanning through a proxy. This should be an absolute last resort, as scanning through something like proxychains is very slow, and often limited (you cannot scan UDP ports through a TCP proxy, for example). 
- The one exception to this rule is when using the Nmap Scripting Engine (NSE), as the scripts library does not come with the statically compiled version of the tool. 
- As such, you can use a static copy of Nmap to sweep the network and find hosts with open ports, then use your local copy of Nmap through a proxy specifically against the found ports.
## LOL Techniques
- The following Bash one-liner would perform a full ping sweep of the `192.168.1.x` network:
````
for i in {1..255}; do (ping -c 1 192.168.1.${i} | grep "bytes from" &); done
````
- The equivalent of this command in Powershell is unbearably slow, so it's better to find an alternative option where possible.
- If you suspect that a host is active but is blocking ICMP ping requests, you could also check some common ports using a tool like netcat.
### Port scanning in bash can be done:
````
for i in {1..65535}; do (echo > /dev/tcp/192.168.1.1/$i) >/dev/null 2>&1 && echo $i is open; done
````
## Proxychains and FoxyProxy
- Think of this as being something like a tunnel created between a port on our attacking box that comes out inside the target network
### Proxychains
- Proxychains can often slow down a connection: performing an nmap scan through it is especially hellish.
- Ideally you should try to use static tools where possible
- For example, to proxy netcat  through a proxy, you could use the command:
````
proxychains nc 172.16.0.10 23
````
- `proxychains` reads its options from a config file. The master config file is located at `/etc/proxychains.conf`. 
- This is where proxychains will look by default; however, it's actually the last location where proxychains will look. The locations (in order) are:
The current directory (i.e. `./proxychains.conf`)
````
~/.proxychains/proxychains.conf
/etc/proxychains.conf
````
-  It's extremely easy to configure proxychains for a specific assignment, without altering the master file. 
-  Simply execute: `cp /etc/proxychains.conf .`, then make any changes to the config file in a copy stored in your current directory. 
-  If you're likely to move directories a lot then you could instead place it in a `.proxychains` directory under your home directory
- If you mess up the master copy, redownload: 
- https://raw.githubusercontent.com/haad/proxychains/master/src/proxychains.conf
- The only section we care about right now is:
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/443c865e3ff3.png)
- By default there is one proxy set to localhost port 9050 -- this is the default port for a Tor entrypoint, should you choose to run one on your attacking machine. 
- That said, it is not hugely useful to us. This should be changed to whichever (arbitrary) port is being used for the proxies
- There is one other line in the Proxychains configuration that is worth paying attention to, specifically related to the Proxy DNS settings:
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/3af17f6ddafc.png)
- If performing an Nmap scan through proxychains, this option can cause the scan to hang and ultimately crash. Comment out the `proxy_dns` line
#### Other things to note when scanning through proxychains:
- You can only use TCP scans -- so no UDP or SYN scans. ICMP Echo packets (Ping requests) will also not work through the proxy, so use the  -Pn  switch to prevent Nmap from trying it.
- It will be extremely slow. Try to only use Nmap through a proxy when using the NSE (i.e. use a static binary to see where the open ports/hosts are before proxying a local copy of nmap to use the scripts library).
#### Examples
- Line addition to `proxychains.conf` to redirect through sock4 proxy
````
socks4 127.0.0.1 4242
````
- Telnet through a proxy to target
````
proxychains telnet 172.16.0.100 23
````
### FoxyProxy
- Proxychains is an acceptable option when working with CLI tools, but if working in a web browser to access a webapp through a proxy, there is a better option available
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/c22f2ef3d6fc.png)
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/92e3cabe22e8.png)
- Fill in the IP and Port on the right hand side of the page that appears, then give it a name. Set the proxy type to the kind of proxy you will be using. SOCKS4 is usually a good bet, although Chisel requires SOCKS5. An example config is given here:
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/19436164d15e.png)
- Press Save, then click on the icon in the task bar again to bring up the proxy menu. You can switch between any of your saved proxies by clicking on them:
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/1d91c2b6a625.png)
- Once activated, all of your browser traffic will be redirected through the chosen port (so make sure the proxy is active!). 
- Be aware that if the target network doesn't have internet access then you will not be able to access the outside internet when the proxy is activated. 
- Even in a real engagement, routing your general internet searches through a client's network is unwise
## SSH Tunnelling and Port Forwarding
### Forward Connections
- Creating a forward (or "local") SSH tunnel can be done from our attacking box when we have SSH access to the target.
- There are two ways to create a forward SSH tunnel using the SSH client -- port forwarding, and creating a proxy.
- Port forwarding is accomplished with the `-L` switch, which creates a link to a Local port. For example, if we had SSH access to `172.16.0.5` and there's a webserver running on `172.16.0.10`, we could use this command to create a link to the server on `172.16.0.10`:
````
ssh -L 8000:172.16.0.10:80 user@172.16.0.5 -fN
````
- We could then access the website on `172.16.0.10` (through `172.16.0.5`) by navigating to port `8000` on our own attacking machine. 
- For example, by entering `localhost:8000` into a web browser. 
- Using this technique we have effectively created a tunnel between port `80` on the target server, and port `8000` on our own box. Note that it's good practice to use a high port, out of the way, for the local connection.
- This also means that we do not need to use `sudo` to create the connection. The `-fN` combined switch does two things: `-f` backgrounds the shell immediately so that we have our own terminal back. `-N` tells SSH that it doesn't need to execute any commands -- only set up the connection.
###Proxies 
- These are made using the `-D` switch, for example: `-D 1337`. This will open up port `1337` on your attacking box as a proxy to send data through into the protected network. This is useful when combined with a tool such as `proxychains`. 
- An example of this command would be:
````
ssh -D 1337 user@172.16.0.5 -fN
````
This again uses the `-fN` switches to background the shell. The choice of port `1337` is completely arbitrary -- all that matters is that the port is available and correctly set up in your proxychains (or equivalent) configuration file. Having this proxy set up would allow us to route all of our traffic through into the target network.
### Reverse Connections
















































































- All credit for this guide goes to:
- https://tryhackme.com/room/wreath

