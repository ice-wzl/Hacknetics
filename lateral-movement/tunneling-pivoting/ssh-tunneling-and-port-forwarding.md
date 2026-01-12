# SSH Tunneling and Port Forwarding

### SSH -D

#### SOCKS Proxy Tunneling

**Enable Dynamic Port Forwarding with SSH**

```
ssh -D 9050 ubuntu@10.129.202.64
```

**Edit /etc/proxychains.conf with Port to Use**

```
socks4 127.0.0.1 9050
```

**Scan Remote Network from Target Machine Over SSH Tunnel**

```
proxychains nmap -v -sn 172.16.5.1-200
```

* Only a full TCP connect scan works over proxychains
* Windows may not respond to a normal ping as well so use -Pn

```
proxychains nmap -v -Pn -sT 172.16.5.19
```

#### Metasploit with Proxychains

```
proxychains msfconsole
set LHOST eth0
search rdp_scanner
use 0
set rhosts 172.16.5.19
run
```

#### xfreerdp with Proxychains

```
proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123
```

### Forward Connections

* Creating a forward (or "local") SSH tunnel can be done from our attacking box when we have SSH access to the target.
* There are two ways to create a forward SSH tunnel using the SSH client -- port forwarding, and creating a proxy.
* Port forwarding is accomplished with the `-L` switch, which creates a link to a Local port. For example, if we had SSH access to `172.16.0.5` and there's a webserver running on `172.16.0.10`, we could use this command to create a link to the server on `172.16.0.10`:

```
ssh -L user@172.16.0.5 8000:172.16.0.10:80 -fN
```

* We could then access the website on `172.16.0.10` (through `172.16.0.5`) by navigating to port `8000` on our own attacking machine.
* For example, by entering `localhost:8000` into a web browser.
* Using this technique we have effectively created a tunnel between port `80` on the target server, and port `8000` on our own box. Note that it's good practice to use a high port, out of the way, for the local connection.
* This also means that we do not need to use `sudo` to create the connection. The `-fN` combined switch does two things: `-f` backgrounds the shell immediately so that we have our own terminal back. `-N` tells SSH that it doesn't need to execute any commands -- only set up the connection.&#x20;

### Proxies

* These are made using the `-D` switch, for example: `-D 1337`. This will open up port `1337` on your attacking box as a proxy to send data through into the protected network. This is useful when combined with a tool such as `proxychains`.
* An example of this command would be:

```
ssh -D 1337 user@172.16.0.5 -fN
```

This again uses the `-fN` switches to background the shell. The choice of port `1337` is completely arbitrary -- all that matters is that the port is available and correctly set up in your proxychains (or equivalent) configuration file. Having this proxy set up would allow us to route all of our traffic through into the target network.

### Reverse Connections

* Reverse connections are very possible with the SSH client (and indeed may be preferable if you have a shell on the compromised server, but not SSH access).
* They are, however, riskier as you inherently must access your attacking machine from the target

#### Make it safe

* First, generate a new set of SSH keys and store them somewhere safe `ssh-keygen`
* Copy the contents of the public key (the file ending with .pub), then edit the \~/.ssh/authorized\_keys file on your own attacking machine. You may need to create the \~/.ssh directory and authorized\_keys file first.
* On a new line, type the following line, then paste in the public key:

```
command="echo 'This account can only be used for port forwarding'",no-agent-forwarding,no-x11-forwarding,no-pty
```

* This makes sure that the key can only be used for port forwarding, disallowing the ability to gain a shell on your attacking machine.
* The final entry in the authorized\_keys file should look something like this:
*

    <figure><img src="https://assets.tryhackme.com/additional/wreath-network/055753470a05.png" alt=""><figcaption></figcaption></figure>
* Next. check if the SSH server on your attacking machine is running:

```
sudo systemctl status ssh
```

* The only thing left is to do the unthinkable: transfer the private key to the target box.
* With the key transferred, we can then connect back with a reverse port forward using the following command:

```
ssh -R LOCAL_PORT:TARGET_IP:TARGET_PORT USERNAME@ATTACKING_IP -i KEYFILE -fN
```

* To put that into the context of our fictitious IPs: `172.16.0.10` and `172.16.0.5`, if we have a shell on `172.16.0.5` and want to give our attacking box (`172.16.0.20`) access to the webserver on `172.16.0.10`, we could use this command on the `172.16.0.5` machine:

```
ssh -R 8000:172.16.0.10:80 kali@172.16.0.20 -i KEYFILE -fN
```

* This would open up a port forward to our Kali box, allowing us to access the `172.16.0.10` webserver, in exactly the same way as with the forward connection we made before!

### Examples

* If you wanted to set up a reverse portforward from port `22` of a remote machine (`172.16.0.100`) to port `2222` of your local machine (`172.16.0.200`), using a keyfile called `id_rsa` and backgrounding the shell, what command would you use? (Assume your username is "kali")

```
ssh -R 2222:172.16.0.100:22 kali@172.16.0.200 -i id_rsa -fN
```

* What command would you use to set up a forward proxy on port `8000` to `user@target.thm`, backgrounding the shell?

```
ssh -D 8000 user@target.thm -fN
```

* If you had SSH access to a server (`172.16.0.50`) with a webserver running internally on port `80` (i.e. only accessible to the server itself on `127.0.0.1:80`), how would you forward it to port `8000` on your attacking machine? Assume the username is `user`, and background the shell.

```
ssh -L 8000:127.0.0.1:80 user@172.16.0.50 -fN
```

### Fixing SSH tunnels that only listen on loopback&#x20;

* if you run into a situation where you are attempting to tunnel and instead of `0.0.0.0` the device only listens on `127.0.0.1` you have two choices&#x20;
* if root&#x20;

```
echo 'GatewayPorts yes' >> /etc/ssh/sshd_config
```

* or utilize socat&#x20;

```
./.socat tcp-listen:80 tcp-connect:127.0.0.1:8080 &
```

* above command listens on `0.0.0.0:80` and will port bend the connection to `127.0.0.1:8080` when it is assumed you have your reverse tunnel set up back to kali station
