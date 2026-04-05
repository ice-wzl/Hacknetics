# Ptunnel-ng (ICMP Tunneling)

Encapsulates traffic within ICMP echo request/response packets. Only works when ping (ICMP) is permitted through the firewall.

## Installation

```bash
git clone https://github.com/utoni/ptunnel-ng.git
```

Build:

```bash
sudo ./autogen.sh
```

### Static Binary Build

```bash
sudo apt install automake autoconf -y
cd ptunnel-ng/
sed -i '$s/.*/LDFLAGS=-static "${NEW_WD}\/configure" --enable-static $@ \&\& make clean \&\& make -j${BUILDJOBS:-4} all/' autogen.sh
./autogen.sh
```

## Transfer to Pivot Host

```bash
scp -r ptunnel-ng ubuntu@10.129.202.64:~/
```

## Usage

### Start Server on Pivot Host

```bash
sudo ./ptunnel-ng -r10.129.202.64 -R22
```

- `-r` — IP to accept connections on
- `-R22` — forward to SSH port 22

### Connect Client from Attack Host

```bash
sudo ./ptunnel-ng -p10.129.202.64 -l2222 -r10.129.202.64 -R22
```

- `-p` — ptunnel-ng server IP
- `-l2222` — local listening port
- `-r` — destination IP
- `-R22` — remote port

### SSH Through ICMP Tunnel

```bash
ssh -p2222 -lubuntu 127.0.0.1
```

### Dynamic Port Forwarding Over ICMP

```bash
ssh -D 9050 -p2222 -lubuntu 127.0.0.1
```

Then use proxychains as normal to route traffic through the ICMP tunnel.
