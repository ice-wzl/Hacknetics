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

## SShuttle

* It doesn't perform a port forward, and the proxy it creates is nothing like the ones we have already seen.
* Instead it uses an SSH connection to create a tunnelled proxy that acts like a new interface.
* It simulates a VPN, allowing us to route our traffic through the proxy without the use of proxychains (or an equivalent).
* We can just directly connect to devices in the target network as we would normally connect to networked devices. As it creates a tunnel through SSH (the secure shell), anything we send through the tunnel is also encrypted.

### Limitations

* sshuttle only works on Linux targets.
* It also requires access to the compromised server via SSH, and Python also needs to be installed on the server.
* That said, with SSH access, it could theoretically be possible to upload a static copy of Python and work with that.

```
sudo apt install sshuttle
```

* The base command for connecting to a server with sshuttle is as follows:

```
sshuttle -r username@address subnet 
```

* For example, in our fictional `172.16.0.x` network with a compromised server at `172.16.0.5`, the command may look something like this:

```
sshuttle -r user@172.16.0.5 172.16.0.0/24
```

* We would then be asked for the user's password, and the proxy would be established.
* The tool will then just sit passively in the background and forward relevant traffic into the target network.
* Rather than specifying subnets, we could also use the `-N` option which attempts to determine them automatically based on the compromised server's own routing table:

```
sshuttle -r username@address -N
```

* If this has worked, you should see the following line:

```
c : Connected to server.
```

* sshuttle doesn't currently seem to have a shorthand for specifying a private key to authenticate to the server with. That said, we can easily bypass this limitation using

```
--ssh-cmd 
```

* With the `--ssh-cmd switch`, we can pick a different command to execute for authentication: say, `ssh -i keyfile`

#### Final Command

* So, when using key-based authentication, the final command looks something like this:

```
sshuttle -r user@address --ssh-cmd "ssh -i KEYFILE" SUBNET
```

* To use our example from before, the command would be:

```
sshuttle -r user@172.16.0.5 --ssh-cmd "ssh -i private_key" 172.16.0.0/24
```

#### Errors

* Please Note: When using sshuttle, you may encounter an error that looks like this:

```
client: Connected.
client_loop: send disconnect: Broken pipe
client: fatal: server died with error code 255
```

* This can occur when the compromised machine you're connecting to is part of the subnet you're attempting to gain access to.
* For instance, if we were connecting to `172.16.0.5` and trying to forward `172.16.0.0/24`, then we would be including the compromised server inside the newly forwarded subnet, thus disrupting the connection and causing the tool to die.
* To get around this, we tell sshuttle to exclude the compromised server from the subnet range using the `-x` switch.
* To use our earlier example:

```
sshuttle -r user@172.16.0.5 172.16.0.0/24 -x 172.16.0.5
```

#### Sources

* All credit for this guide goes to:
* https://tryhackme.com/room/wreath
* The THM Room was created by MuirlandOracle, who puts out amazing content. The contents of this .md come from that room. Check it out!
