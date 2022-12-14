# ufw

### Verify Status&#x20;

```
sudo ufw status
#output
Status: inactive
--OR--
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), deny (routed)
New profiles: skip
```

### Enable the FW

```
sudo ufw enable
#output
Firewall is active and enabled on system startup
```

### Disable the FW

```
sudo ufw disable
```

### See FW Rules

```
sudo ufw status
#output
Status: active

To                         Action      From
--                         ------      ----
Anywhere                   DENY        10.10.10.10  
```

### Block an IP Address/Subnet <a href="#block-an-ip-address" id="block-an-ip-address"></a>

```
sudo ufw deny from 10.10.10.10
sudo ufw deny from 10.10.10.10/24
```

### Block Incoming Connections to a Network Interface&#x20;

```
sudo ufw deny in on eth0 from 10.10.10.10
```

### Allow Incoming Connections to a Network Interface <a href="#allow-incoming-connections-to-a-network-interface" id="allow-incoming-connections-to-a-network-interface"></a>

```
sudo ufw allow in on eth0 from 10.10.10.10
```

### Allow an IP in&#x20;

```
sudo ufw allow from 10.10.10.10
```

### Deleting Rules

```
sudo ufw status numbered
#output
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] Anywhere                   DENY IN     10.10.10.10             
[ 2] Anywhere on eth0           ALLOW IN    10.10.10.11 

#now delete the rule
sudo ufw delete 1    
```
