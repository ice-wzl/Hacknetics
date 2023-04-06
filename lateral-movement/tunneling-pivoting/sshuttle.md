# SShuttle

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
