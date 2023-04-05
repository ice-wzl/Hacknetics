# Proxychains and FoxyProxy

* Think of this as being something like a tunnel created between a port on our attacking box that comes out inside the target network

### Proxychains

* Proxychains can often slow down a connection: performing an nmap scan through it is especially hellish.
* Ideally you should try to use static tools where possible
* For example, to proxy netcat through a proxy, you could use the command:

```
proxychains nc 172.16.0.10 23
```

* `proxychains` reads its options from a config file. The master config file is located at `/etc/proxychains.conf`.
* This is where proxychains will look by default; however, it's actually the last location where proxychains will look. The locations (in order) are: The current directory (i.e. `./proxychains.conf`)

```
~/.proxychains/proxychains.conf
/etc/proxychains.conf
```

* It's extremely easy to configure proxychains for a specific assignment, without altering the master file.
* Simply execute: `cp /etc/proxychains.conf .`, then make any changes to the config file in a copy stored in your current directory.
* `proxychains` will use the config file in your local dir first before using the one in `/etc/`
* Can also use `-f` and specify a file&#x20;

```
proxychains -f proxy9051.conf #rest of command here
```

* If you're likely to move directories a lot then you could instead place it in a `.proxychains` directory under your home directory
* If you mess up the master copy, redownload:
* https://raw.githubusercontent.com/haad/proxychains/master/src/proxychains.conf
* The only section we care about right now is:
* ![alt text](https://assets.tryhackme.com/additional/wreath-network/443c865e3ff3.png)
* By default there is one proxy set to localhost port 9050 -- this is the default port for a Tor entrypoint, should you choose to run one on your attacking machine.
* That said, it is not hugely useful to us. This should be changed to whichever (arbitrary) port is being used for the proxies
* There is one other line in the Proxychains configuration that is worth paying attention to, specifically related to the Proxy DNS settings:
* ![alt text](https://assets.tryhackme.com/additional/wreath-network/3af17f6ddafc.png)
* If performing an Nmap scan through proxychains, this option can cause the scan to hang and ultimately crash. Comment out the `proxy_dns` line

#### Other things to note when scanning through proxychains:

* You can only use TCP scans -- so no UDP or SYN scans. ICMP Echo packets (Ping requests) will also not work through the proxy, so use the -Pn switch to prevent Nmap from trying it.
* It will be extremely slow. Try to only use Nmap through a proxy when using the NSE (i.e. use a static binary to see where the open ports/hosts are before proxying a local copy of nmap to use the scripts library).

#### Examples

* Line addition to `proxychains.conf` to redirect through sock4 proxy

```
socks4 127.0.0.1 4242
```

* Telnet through a proxy to target

```
proxychains telnet 172.16.0.100 23
```

### FoxyProxy

* Proxychains is an acceptable option when working with CLI tools, but if working in a web browser to access a webapp through a proxy, there is a better option available
* ![alt text](https://assets.tryhackme.com/additional/wreath-network/c22f2ef3d6fc.png)
* ![alt text](https://assets.tryhackme.com/additional/wreath-network/92e3cabe22e8.png)
* Fill in the IP and Port on the right hand side of the page that appears, then give it a name. Set the proxy type to the kind of proxy you will be using. SOCKS4 is usually a good bet, although Chisel requires SOCKS5. An example config is given here:
* ![alt text](https://assets.tryhackme.com/additional/wreath-network/19436164d15e.png)
* Press Save, then click on the icon in the task bar again to bring up the proxy menu. You can switch between any of your saved proxies by clicking on them:
* ![alt text](https://assets.tryhackme.com/additional/wreath-network/1d91c2b6a625.png)
* Once activated, all of your browser traffic will be redirected through the chosen port (so make sure the proxy is active!).
* Be aware that if the target network doesn't have internet access then you will not be able to access the outside internet when the proxy is activated.
* Even in a real engagement, routing your general internet searches through a client's network is unwise
