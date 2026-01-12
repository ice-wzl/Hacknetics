# IpTables bending traffic

### iptables

```
iptables -A INPUT
```

```
sudo iptables -t nat -A PREROUTING -i ens192 -s 10.10.14.221 -d 10.129.64.133 -j DNAT --to-destination 172.16.5.5
sudo iptables -t nat -A PREROUTING -i ens224 -s 172.16.5.5 -d 172.16.5.225 -j DNAT --to-destination 10.10.14.221
sudo iptables -A FORWARD -s 172.16.5.5 -d 10.10.14.221 -j ACCEPT
sudo iptables -A FORWARD -d 172.16.5.5 -s 10.10.14.221 -j ACCEPT
sudo iptables -t nat -A POSTROUTING -d 10.10.14.221 -j SNAT --to-source 10.129.64.133
sudo iptables -t nat -A POSTROUTING -d 172.16.5.5 -j SNAT --to-source 172.16.5.225
```

```
sudo iptables -t nat -A PREROUTING -p tcp --dport 1234 -i tun0 -d 192.168.49.125 -j DNAT --to-destination 192.168.23.134
sudo iptables -t nat -A PREROUTING -i ens224 -s 172.16.5.5 -d 172.16.5.225 -j DNAT --to-destination 10.10.14.221
sudo iptables -A FORWARD -s 172.16.5.5 -d 10.10.14.221 -j ACCEPT
sudo iptables -A FORWARD -d 172.16.5.5 -s 10.10.14.221 -j ACCEPT
sudo iptables -t nat -A POSTROUTING -d 10.10.14.221 -j SNAT --to-source 10.129.64.133
sudo iptables -t nat -A POSTROUTING -d 172.16.5.5 -j SNAT --to-source 172.16.5.225
```

```
iptables -t nat -A PREROUTING -p tcp --dport 1234 -i tun0 -d 192.168.49.125 -j DNAT --to-destination 192.168.23.134
iptables -t nat -A PREROUTING -p tcp -i eth1 -d 192.168.23.138 -j DNAT --to-destination 10.10.110.10
iptables -A FORWARD -s 10.10.110.10 -d 192.168.23.134 -j ACCEPT
iptables -A FORWARD -d 10.10.110.10 -s 192.168.23.134 -j ACCEPT
iptables -A FORWARD -i eth1 -o tun0 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A POSTROUTING -d 192.168.23.134 -j SNAT --to-source 192.168.49.125
iptables -t nat -A POSTROUTING -d 10.10.110.10 -j SNAT --to-source 192.168.49.125
```
