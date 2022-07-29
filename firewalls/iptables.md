# iptables

* Check the status of the current firewall rules&#x20;

```
sudo iptables -L -v
```

### Appending Rules to the Chain&#x20;

\-A stands for append and it is how you will add rules to the bottom of the chain.

```
sudo iptables -A
```

* **-i** (**interface**) — the network interface whose traffic you want to filter, such as eth0, lo, ppp0, etc.
* **-p** (**protocol**) — the network protocol where your filtering process takes place. It can be either **tcp**, **udp**, **udplite**, **icmp**, **sctp**, **icmpv6**, and so on. Alternatively, you can type **all** to choose every protocol.
* **-s** (**source**) — the address from which traffic comes from. You can add a hostname or IP address.
* **–dport** (**destination port**) — the destination port number of a protocol, such as **22** (**SSH**), **443** (**https**), etc.
* **-j** (**target**) — the target name (**ACCEPT**, **DROP**, **RETURN**). You need to insert this every time you make a new rule.

If you want to use all of them, you must write the command in this order:

```
sudo iptables -A <chain> -i <interface> -p <protocol (tcp/udp) > -s <source> --dport <port no.>  -j <target>
```

### **Enabling Traffic on Localhost**

To allow traffic on localhost, type this command:

```
sudo iptables -A INPUT -i lo -j ACCEPT
```

The command above will make sure that the connections between a database and a web application on the same machine are working properly.

### **Enabling Connections on HTTP, SSH, and SSL Port**

Next, we want **http** (port **80**), **https** (port **443**), and **ssh** (port **22**) connections to work as usual. To do this, we need to specify the protocol (**-p**) and the corresponding port (**–dport**). You can execute these commands one by one:

```
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### **Filtering Packets Based on Source**

You need to specify it after the **-s** option. For example, to accept packets from **192.168.1.3**, the command would be:

```
sudo iptables -A INPUT -s 192.168.1.3 -j DROP
```

You can also reject packets from a specific IP address by replacing the **ACCEPT** target with **DROP**.

```
sudo iptables -A INPUT -s 192.168.1.3 -j ACCEPT
```

If you want to drop packets from a range of IP addresses, you have to use the **-m** option and **iprange** module. Then, specify the IP address range with **–src-range**. Remember, a hyphen should separate the range of ip addresses without space, like this:

```
sudo iptables -A INPUT -m iprange --src-range 192.168.1.100-192.168.1.200 -j DROP
```



\
