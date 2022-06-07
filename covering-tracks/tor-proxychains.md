# Tor 
## Setup 
````
apt-get install tor 
service tor start
service tor status 
service tor stop 
OR
systemctl start tor 
systemctl status tor
systemctl stop tor
````
## Proxychains 
![rvVo73x](https://user-images.githubusercontent.com/75596877/172404948-52726fce-aa5e-4104-b8b6-b2bc9c04fa1b.png)
- Tool that forces any TCP connection made by any given application to follow through proxy like TOR SOCKS4 SOCKS5 HTTP(S) proxy
### Install
````
sudo apt install proxychains
````
### Configure 
````
vim /etc/proxychains.conf
````
- Uncomment `dynamic_chain` and comment the other options
- Uncomment `proxy_dns` in order to prevent DNS leakage 
#### Start Firefox with proxychains
````
tor #start the tor service 
proxychains firefox & #start firefox in the background with proxychains 
````
## Test
- Browse to `http://ifconfig.co` and or `http://ipinfo.io` to check that your IP is properly being obsfucated
- Browse to `http://dnsleaktest.com` and see that your DNS address has changed 
- IMPORTANT: All other web browser windows should be closed before opening firefox through `proxychains`

## Tor Browser 
- Recommend changing saftey `Level to 2 (Safer)`
