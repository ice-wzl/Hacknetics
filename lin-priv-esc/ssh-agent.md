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

