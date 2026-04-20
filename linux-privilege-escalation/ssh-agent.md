# ssh agent

### Overview

* credit to the original author: [https://grahamhelton.com/blog/ssh\_agent/](https://grahamhelton.com/blog/ssh\_agent/)&#x20;
* ssh-agent is an interesting utility that is used to help ease the burden of managing private keys. It’s similar to the concept of single sign on but for SSH keys. The SSH agent allows you to add private keys/identities to the agent running on your local machine using `ssh-add <private_key_file>`
* After adding a key to the `ssh-agent` utility, you can then `ssh` to a server using the key without having to re-enter the password.
* when the `ssh` option is used in conjunction with the `-A` option. In fact, even the `ssh` manpage gives a hint that it can lead to “the ability to bypass file permissions on the remote host”.
* TLDR; SSH Agent forwarding keeps your private keys out of places you don’t have control over.

### POC

* running the `ssh-add -l` command on `vuln-server` allows us to identify if there are any loaded identities. Currently, there are no identities loaded which means no one is logged into this server as _root_ with an SSH session using ssh-agent. Fairly normal so far.
* When we run `lsof -U | grep agent`, we get a result back indicating that the user _admin_ is logged in to the machine and is utilizing SSH-Agent.

```
lsof -U | grep agent 
sshd    4145        admin    11u    unix    0x000000007f0fda18    0t0    46998936    /tmp/ssh-ZzrtT2ZwVr/agent.4145 type=STREAM
```

* lets attempt to take over the `SSH_AUTH_SOCK` socket. Doing so is is fairly trivial. All we need to do is set an environment variable of the root user using the `export` command. To do so, simply take the `/tmp/ssh-ZzrtT2ZwVr/agent.4145` path identified in the previous `lsof -U | grep agent` command, and assign it to the `SSH_AUTH_SOCK` environment variable by running `export SSH_AUTH_SOCK=/tmp/ssh-ZzrtT2ZwVr/agent4145`.
* Running the command `ssh-add -l` once again, we can see the fingerprint for the keys on the _admin_ user’s LOCAL machine. I ran `ssh-add -l` on my local machine (which is where I am logged in as admin from) and you can see that the fingerprints are the same because I have logged into the compromised machine using agent forwarding.
* the SSH-Agent does not allow you to export the actual private key in any way.

### Figure out the hosts you can connect to&#x20;

* There are a few ways we can do so. The first is by checking the `/home/admin/known_hosts` file. This file typically contains the IP addresses of previously connected to hosts. However, taking a look at our file (on an Ubuntu 20.04) system, you might notice that there are not any IP addresses… What gives?
* Well, you can thank the `/etc/ssh/ssh_config` file’s `HashKnownHosts` option for this. If this option is set, the hosts that _admin_ has been connecting to will be… well hashed.
* see: [https://grahamhelton.com/blog/ssh\_agent/](https://grahamhelton.com/blog/ssh\_agent/) for cracking methods.
