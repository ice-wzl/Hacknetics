# tun2socks

### tun2socks

* https://github.com/xjasonlyu/tun2socks/wiki/Examples

#### Run tun2socks

```
sudo tun2socks --device tun://tun1 --proxy socks5://127.0.0.1:1080
```

#### Configure Tunnel Interface

```
sudo ip link set tun1 up
sudo ip a a 10.9.9.9/24 dev tun1
sudo ip r a 192.168.110.0/24 via 10.9.9.9 dev tun1
```
