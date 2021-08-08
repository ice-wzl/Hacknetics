## Recon
### Table of Contents
- [Recon](#recon)
  * [AutoRecon](#autorecon)
  * [NetDiscover](#netdiscover)
  * [Nmap](#nmap)
    + [Ping Scan -sn Option](#ping-scan--sn-option)
    + [TCP Connect Scan](#tcp-connect-scan)
    + [TCP SYN Scan](#tcp-syn-scan)
    + [UDP Port Scanning](#udp-port-scanning)
    + [Fingerprint Services](#fingerprint-services)
    + [Scanning port ranges with Nmap](#scanning-port-ranges-with-nmap)
  * [NSE](#nse)
  * [SNMP](#snmp)
  * [Onesixtyone](#onesixtyone)
  * [SNMPwalk](#snmpwalk)
  * [SMB Enumeration](#smb-enumeration)
  * [smbmap](#smbmap)
  * [smbclient](#smbclient)
  * [rpcclient](#rpcclient)
  * [Enum4linux](#enum4linux)
  * [Nmap SMB scripts](#nmap-smb-scripts)
  * [Web Servers](#web-servers)
  * [Nikto](#nikto)
  * [Sanity Check](#sanity-check)
  * [DIRB](#dirb)
  * [Dirbuster](#dirbuster)
  * [Netcat](#netcat)
  * [GoBuster](#gobuster)
  * [WpScan](#wpscan)

### AutoRecon
- Always start here, trust me.
```
autorecon -ct 2 -cs 2 -vv -o outputdir 192.168.1.100 192.168.1.1/30 localhost
autorecon 10.200.97.200
````
- `-ct` (concurrent targets)
- `-o` custom output directory location.
- `-cs` limits the number of concurent scans per target
- Auto recon will create and store the results in the `/results` directory.
### NetDiscover
- Netdiscover is an active/passive reconnaissance tool that uses ARP to find live hosts on a local network.
- Netdiscover actively searches for live hosts on the network by broadcasting ARP requests like a router.
- By default netdiscover operates in active mode, however you can use it in passive mode with `-p`.  With passive move it will not broadcast anything.
- Note: ARP is unable to cross network boundaries or over any VPN connection
``` 
netdiscover -r 10.11.1.0/24
````
### Nmap
- I have no time to read, just give me the nmap scanning meta.
````
nmap -sS x.x.x.x -p- --min-rate 10000
nmap -A -T5 x.x.x.x -p- -vv
nmap --script=scriptname.nse x.x.x.x -vv
````
#### Ping Scan -sn Option
- -sn tells nmap to perform host discovery only without any additional port scanning and prints out details of any hosts that responded.
````
nmap -sn 10.11.1.0/24
````
- nmap also has the -Pn option which will disable the host discovery stage altogether on a scan.  The -Pn option is best used in combination with other scans.
#### TCP Connect Scan
- The TCP connect scan in Nmap is the alternative TCP scan to use when a SYN scan is not an option.  
- TCP connect scan should be used when nmap does not have raw packet privileges which is required for a SYN scan.
- TCP complete performs the entire 3 way handshake.
- SLOW!
````
nmap -sT [target host]
````
#### TCP SYN Scan
- The TCP SYN scan is usually the best scan option in most cases and is known as the ‘stealthy port scan.’
- Does not complete the 3 way handshake
````
nmap -sS [target host]
````
#### UDP Port Scanning
- Always check for UDP ports will pick up DNS, NTP, SNMP 
- Check top 100 ports with the `-F` option.
- Generally much slower than TCP scanning 
````
nmap -sU [target host]
nmap -sU -F [target host]
````
#### Fingerprint Services
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
#### Scanning port ranges with Nmap
- By default nmap will only scan the most 1000 common ports. To override the default use the -p
````
nmap -p 1-100 [target host]
nmap -p 137-139,445 [target host]
````
### NSE
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
nmap --script=http-robots.txt.nse [target host]
````
### SNMP 
- Commands 
- Read, write, trap, traversal command
- SNMP community strings
- Community strings are like a username or password that allows access to the managed device. 
- There are three different community strings that allow a user to set 1 ready only commands, 2 read write commands and 3 traps.  
- SNMPv3 community string is replaced with a user and password authentication.  
- SNMPv1/v2 is factory default read only strings set to public and read write string set to private.
### Onesixtyone
- Onesixtyone is a fast tool to brute force SNMP community strings and take advantage of the connectionless protocol.
- Onesixtyone requires two arguments: a file that contains the list of community strings to try and the target host ip address.  
- You can also provide a list of host IP addresses to be scanned by onesixtyone using the -i option.
````
onesixtyone #access help menu
onesixtyone -c snmp_community_strings_wordlist_onesixtyone.txt -p 161 192.168.43.161
````
- Location of wordlists
````
/usr/share/wordlists/seclists/Discovery/SNMP
````
### SNMPwalk
- Snmpwalk queries MIB values to retrieve information about the managed devices, but as a minimum requires a valid SNMP read only community string.
- Run snmpwalk with the default community string ‘public’ on and SNMPv1 device use the following command:
````
snmpwalk -c public -v1 [target host]
````
- You can also request a single object ID value using the following command:
````
snmpwalk -c public -v1 [target host] [OID]
````
- Nmap SNMP scripts
````
ls -l /usr/share/nmap/scripts/snmp*
````
### SMB Enumeration
- The SMB is a network file sharing protocol that provides access to shared files and printers on a local network.
- When clients and servers use different operating systems and SMB versions, the highest supported version will be used for communication.
- SMB uses the following TCP and UDP ports:
````
Netbios-ns 137/tcp #NETBIOS Name Service
Netbios-ns 137/udp
netbios-dgm 138/tcp #NETBIOS Datagram Service
Netbios-dgm 138/udp
Netbios-ssn 139/tcp #NETBIOS session service
Netbios-ssn 139/udp
Microsoft-ds 445/tcp #if you are using active directory
````
### smbmap
- smbmap is one of the best ways to enumerate samba. smbmap allows pen-testers to run commands(given proper permissions), download and upload files, and overall is just incredibly useful for smb enumeration.
````
smbmap -u "admin" -p "password" -H 10.10.10.10 -x "ipconfig"
````
- `-s` -> specify the share to enumerate
- `-d` -> specify the domain to enumerate
- `--download` -> downloads a file
- `--upload` -> uploads a file
### smbclient
- smbclient allows you to do most of the things you can do with smbmap, and it also offers you and interactive prompt.
- `-w` -> specify the domain(workgroup) to use when connecting to the host
- `-I` -> specify the ip address of the host
- `-c "ipconfig"` -> would run the `ipconfig` command on the host
- `-U` -> specify the username to authenticate with 
- `-P` -> specifies the password to authenticate with
- `-N` -> tells smbclient to not use a password
- `get test` -> would download the file named `test`
- `put /etc/hosts` -> would put your `/etc/hosts` file on the target 
- Syntax: 
- To see which shares are available on a given host, run:
````
 /usr/bin/smbclient -L 10.10.10.10
````
- For example, if you are trying to reach a directory that has been shared as 'public' on a machine called 10.10.10.10, the service would be called \\10.10.10.10\public. - 
- However, due to shell restrictions, you will need to escape the backslashes, so you end up with something like this:
````
/usr/bin/smbclient \\\\10.10.10.10\\public mypasswd
````
### rpcclient
- A tool used for executing client-side MS-RPC functions. A null session in a connection with a samba or SMB server that does not require authentication with a password.
````
rpcclient -U “” [target ip address]
````
- The -U option defines a null username, you will be asked for a password but leave it blank (hit enter!!!!)
- The command line will change to the rpcclient context
````
rpcclient $>
````
- To retrieve some general information about the server like the domain and number of users:
````
querydominfo
````
- This command returns the domain, server, total users on the system and some other useful information.  
- Also shows the total number of user accounts and groups available on the target system.
- To retrieve a list of users present on the system 
````
enumdomusers
````
- The result is a list of user accounts available on the system with the RID in hex.  We can now use rpcclient to query the user info for more information:
````
queryuser [username]
username=pbx
queryuser pbx, queryuser 1000, queryuser 0x3e8
````
-This command will return information about the profile path on the server, the home drive, password related settings and a lot more.
- To see an overview of all enumeration objects just type enum+tabx2.
- If you get an error that says:
````
Cannot connect to server.  Error was NT_STATUS_CONNECTION_DISCONNECTED
````
- Occurs because the minimum protocol version for smbclient has been set to SMB2_02
- Fix with:
````
sudo vim /etc/samba/smb.conf
````
- Add the following line to the config under the `[global]` section
````
client min protocol = CORE
````
- Alternative method to enumdomusers is through RID cycling.
- To determine the full SID we can run the: ‘lookupnames’ command and search for the domain with the following command:
````
lookupnames pbx
````
- There are two sets of RIDS 500-1000 for system and 1000-10000 for Domain created users and groups. 
- If we append -500 to the SID and look it up using the lookupsids command we get the following output with the username:
````
rpcclient $> lookupsids S-1-5-21-532510730-1394270290-3802288464-500
S-1-5-21-532510730-1394270290-3802288464-500 *unknown*\*unknown* (8)
````
- Shows SID is unknown, increase by one
````
rpcclient $> lookupsids S-1-5-21-532510730-1394270290-3802288464-501
S-1-5-21-532510730-1394270290-3802288464-501 PBX\nobody (1)
````
- Find a valid user, increase the RID to 1000.
````
rpcclient $> lookupsids S-1-5-21-532510730-1394270290-3802288464-1000
S-1-5-21-532510730-1394270290-3802288464-1000 PBX\pbx (1)
````
- Have the full SID now
### Enum4linux
- Enum4linux is a linux alternative to enum.exe and it is used to enumerate data from windows or samba hosts.
```
enum4linux [target ip]
````
-Will auto RID cycle 
- Part of autorecon!
- Recommend to > output to a text file for reference (its alot)
### Nmap SMB scripts
````
ls -l /usr/share/nmap/scripts/smb*
nmap --script=[scriptname] [target ip]
````
- For smb-os-discovery:
````
nmap -p 139,445 --script=smb-os-discovery [target ip]
````
- First scans the target for all known SMB vulnerabilities 
- Second to see if target is vulnerable to EternalBlue

````
nmap -p 139,445 --script=smb-vuln* [target ip]
nmap -p 445 [target] --script=smb-vuln-ms17-010
````
- If nse is missing a script that is available:
````
wget https://svn.nmap.org/nmap/scripts/NAME_OF_SCRIPT.nse -O /usr/share/nmap/scripts/NAME_OF_SCRIPT.nse
````
- Then update the database:
````
nmap --script-updatedb
````
### Web Servers
- Two most common Apache, Microsoft IIS
### Nikto
```
nikto -h [target ip/hostname]
nikto -h [target ip/hostname] -p 80,88,443
nikto -h [target ip/hostname -p 80-88
```
- Run early, its slow but good
### Sanity Check
- Look at robots.txt
- Look in the webpage for comments
- Is the site not rendering right? (check dns /etc/hosts)
### DIRB
- Comes with a default word list 
````
Dirb [url target host]
````
- Custom wordlist:
````
Dirb [url target host] [wordlist]
````
- `-n` will stop the scan on current dir and move to the next 
- `-q` stops the running scan and saves the current state
- `-r` will return the remaining scan statistics 
### Dirbuster
````
dirbuster 
````
- Wordlist location: 
````
/usr/share/dirbuster/wordlists/
````
- To run, set the target to the target url, set the number of threads, select a word list and hit the start button.
- Much faster because its multi threaded
### Netcat
- We can grab the banner of the web service running on the target host:
````
nc [target ip] 80
````
- Enter this HTTP request on the next line
````
HEAD / HTTP/1.0
````
- To retrieve the top level page on the webserver we can use the following command:
````
nc [target ip] 80
````
- Run this HTTP request
````
GET / HTTP/1.0
````
### GoBuster
- Another good web application scanner.
````
gobuster dir -u http://magic.uploadvulns.thm -w /usr/share/wordlists/dirb/big.txt
````
- `dir` to run it in directory enumeration mode
- `-u` followed by the url 
- `-w` to specify a wordlist
#### Syntax
- `dir` -> Directory/File Brute force mode
- `dns` -> DNS brute forcing mode
- `-x` -> Flag for extentions to be tested against
- `-w` -> Sets a wordlist to be used
- `-U` -> Set username for basic authentication (if required by the directory)
- `-P` -> Set password for basic authentication 
- `-s` -> Set the status codes gobuster will recognize as valid
- `-k` -> Skip ssl certificate validation
- `-a` -> Set a user agent string
- `-H` -> Specify and HTTP header
- `-u` -> Set the url to brute force 
- `/usr/share/wordlists` -> Location of the wordlists
### Example full syntax
````
dirb http://10.10.10.10:80/secret/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -X .txt 
````
- This command tests the /secret/ directory 
- It specifies to use the wordlist `directory-list-2.3-medium.txt`
- With the `-x` flag it sets gobuster to test for `.txt` file extensions i.e. admin.txt, secret.txt
### WpScan
- Ideal for wordpress sites to find their vulnerable plugins, users, and themes.
- Default scan runs non intrusive checks which means no accounts will be brute forced and themes and plugins will be enumerated passively.
````
wpscan --update
wpscan --url [target url]
wpscan --url http://x.x.x.x --enumerate u,p,t
````
- Active enumeration 
- `p` ->scans popular plugins only
- `vt` ->scans vulnerable these only
- `at` ->scans all themes
- Full command:
````
wpscan --url [url] --enumerate [p/vp/ap/t/vt/at]
````
- The following command will test a target for all popular plugins:
````
wpscan --url [url] --enumerate p --plugins-detection aggressive
````
- To scan a wordpress installation only for vulnerable plugins we can run the following command:
````
wpscan --url [url] --enumerate vp --plugins-detection aggressive
````
- Scan for all plugins in the WPScan database run the enumerate option with ap:
````
wpscan --url [url] --enumerate ap --plugins-detection aggressive
````
- Enumerating WP users
````
wpscan --url [target url] --enumerate u 
````




