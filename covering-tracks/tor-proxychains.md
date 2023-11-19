# Tor

## Setup

```
apt-get install tor 
service tor start
service tor status 
service tor stop 
OR
systemctl start tor 
systemctl status tor
systemctl stop tor
```

## Proxychains

![rvVo73x](https://user-images.githubusercontent.com/75596877/172404948-52726fce-aa5e-4104-b8b6-b2bc9c04fa1b.png)

* Tool that forces any TCP connection made by any given application to follow through proxy like TOR SOCKS4 SOCKS5 HTTP(S) proxy

### Install

```
sudo apt install proxychains
```

### Configure

```
vim /etc/proxychains.conf
```

* Uncomment `dynamic_chain` and comment the other options
* Uncomment `proxy_dns` in order to prevent DNS leakage

#### Start Firefox with proxychains

```
tor #start the tor service 
proxychains firefox & #start firefox in the background with proxychains 
```

## Test

* Browse to `http://ifconfig.co` and or `http://ipinfo.io` to check that your IP is properly being obsfucated
* Browse to `http://dnsleaktest.com` and see that your DNS address has changed
* if using firefox instead of just the tor browser and have firefox configured to use `127.0.0.1` `9050` as a proxy and have the tor service running open firefox and browse to `about:config`
* Change `privacy.resist.Fingerprinting` from `false` to `true`
* IMPORTANT: All other web browser windows should be closed before opening firefox through `proxychains`

## Tor Browser

* Recommend changing saftey `Level to 2 (Safer)`

### Exclude Exit Nodes&#x20;

```
echo 'ExcludeNodes {us},{au},{ca},{ru} StrictNodes 1' >> /etc/tor/torrc 
```

### Use specific country exit node&#x20;

```
echo "ExitNodes {us} StrictNodes 1" >> /etc/tor/torrc 
```

### Prevent server to be used as exit node&#x20;

```
echo "ExitPolicy reject *:*" >>/etc/tor/torrc
```

### Running a Tor Relay

* This content below is assuming Centos8, but it can be adapted to almost any operating system (linux wise)
* To see more information:
* [https://community.torproject.org/relay/setup/](https://community.torproject.org/relay/setup/)

```
yum update
#OR
dnf update
-----------------------
yum install epel-release
#OR
dnf install epel-release
-----------------------
```

* create the file `/etc/yum.repos.d/Tor.repo`
* insert the below content into the file&#x20;

```
[tor]
name=Tor for Enterprise Linux $releasever - $basearch
baseurl=https://rpm.torproject.org/centos/$releasever/$basearch
enabled=1
gpgcheck=1
gpgkey=https://rpm.torproject.org/centos/public_gpg.key
cost=100
```

* now update for the changes to be included&#x20;

```
yum update
#OR 
dnf update
```

* install tor&#x20;

```
yum install tor
#OR
dnf install tor
```

* edit your `/etc/tor/torrc`
* insert the lines below, change the options to your need (top two lines)

```
Nickname    myNiceRelay  # Change "myNiceRelay" to something you like
ContactInfo your@e-mail  # Write your e-mail and be aware it will be published
ORPort      443          # You might use a different port, should you want to
ExitRelay   0
SocksPort   0
```

* enable and start tor&#x20;

```
systemctl enable --now tor
systemctl enable tor
systemctl start tor
```

#### Optional Monitor Tor useage&#x20;

* to see the stats for your relay live you can install `nyx`

```
yum install nyx
#OR
dnf install nyx
```

* start a `screen` or `tmux` sessions and run the program&#x20;

```
tmux
nyx
-----------
#detatch tmux 
Crtl+B + Shfit + D
#it will keep running 
#reattatch tmux to see stats after logging back in 
tmux attach -t 0
```
