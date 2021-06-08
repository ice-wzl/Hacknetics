# OSCP-Prep
### Nmap
#### Basic Usage
##### Aggressive scan (-A), as fast as possible (-T5), port (-p), range (1-10000)
```
nmap -A -T5 172.16.6.1 -p 1-100000
```
##### Other Scan Flags
##### TCP Syn Scan 
```
nmap -sS -T3 172.16.6.1
```
- Default and most popular.  Fast, never completes the TCP connections. Clear and reliable, half open scanning.
##### TCP Connect Scan
```
nmap -sT -T2 172.16.6.1
```
- Default TCP scan when Syn Scan is not an option. When a user does not have raw packet privlages. Completes the connection, target machine is more likely to log the connection.
##### UDP Scan 
```
nmap -sU 172.16.6.1 -T1
```
- UDP Scan, DNS, SNMP, DHCP 53, 161/162, 67/68 most common UDP ports. Sends a UDP packet to every targeted host, for common ports a protocol specific payload is sent to increase response rate. -sV can be added to help differentiate the truly open from filtered ports. Full scan of a host and all ports can take 18 hours, scan the popular ports, scan from behind the firewall, and use `--host-timeout` to skip slow hosts.
##### Null Scan, Fin Scan, Xmas Scan
```
-sN
```
- Null Scan 
```
-sF
```
- Fin Scan
```
-sX
```
- Xmas Scan
- Can sneak through certain non-stateful firewalls and packet filtering routers.  More stealthy than even the SYN scan. Non RFC 793 complient system and will send a RST back whether the port is closed or open, this will cause all ports to be labeled closed. Cannot distinguish between `open` versus `filtered` leaving the label `open | filtered`
##### TCP ACK Scan
```
nmap -sA 172.16.6.1
```
- Never determines `open` or even `open | filtered` Used to map out firewall rulesets, determining wether they are stateful or not and which ports are filtered. The ACK scan probe only has the ACK flag set unless you use `--scanflags` Unfiltered systems, `open` and `closed` ports will both return a RST packet. Nmap then labels them as `unfiltered` meaning they are reachable by the ACK, whether they are `open` or `closed` is undetermined.
##### Custom TCP Scan
```
--scanflags
```
- Allows you to design your own scan specifying TCP flags. Add the options URG, ACK, PSH, RST, SYN, FIN together.  
```
nmap --scanflags URGACKPSHRSTSYNFIN
```
- This would set all the options together, not useful for scanning.
##### Idle or Zombie Scan
```
nmap -sI <zombie host>[:<probeport>] (idle scan)
```
- Truly blind TCP port scan of the target. No packets are sent to the target from your real IP address. Unique side channel attack exploits predictable IP fragmentation ID sequence generation on the zombie host to glean infomation about the open ports on the target. IDS will display the scan coming from the zombie host. Zombie must be up.
- Extremely stealthy, maps out IP-based trust relationships between machines. Port listing shows open ports *from the perspective of the zombie host*. 
- Can add a colon followed by a port number `[:<probeport>]` to the zombie host if you want to probe a particular port on the zombie for IP ID changes. Otherwise nmap will default to 80 TCP pings.
##### FTP Bounce Scan
```
-b <FTP relay host>
<username>:<password>@<server>:<port>
```
- `<Server>` is the name or IP address of a vulberable FTP server. You may omit `<username>:<password>` in which anonymous login creds are used.  Use `<anonymous>:-wwwuser>` The port number and preceeding colon may be omitted as well when the default FTP port (21) are used on `<server>`.
- Using the `--script ftp-bounce` will tell you whether the host is vulnerable or not.
- Causes the FTP server to scan other hosts. "Sends a file to each interesting port of the target host."  Good way to bypass firewalls because FTP servers in organizations typically have more access than a standard host.
##### Scan Options
```
--exclude-ports <port ranges>
```
- Specifies which ports you do not want scanned
##### Service and Version Detection
- Note `-A` option includes version detection
- Version Detection
```
-sV
```
- Enables version detection. `-sR` is an alias for `-sV`.
```
--allports
```
- Dont exclude any ports from version detection.  By default nmap version detection skips TCP port 9100 because some printers simply print anything sent to that port, leading to dozens of pages of HTTP GET requests, binary SSL session requests etc.
`--allports` supercedes any `-exclude-ports` flag range.
##### Sets Version Scan Intensity 
```
--version-intensity <intensity>
```
- Numbers 1-9, assigns a rarity value to a series of probes. Larger the number the more likely the services will be correct, however it takes longer. Default is 7.
##### OS Detection
```
-O
```
- Enable OS detection `-A` also does this inaddition to other things.
###### Limit OS Detection to promising targets
```
--osscan-limit
```
- OS Detection needs at least one open and one closed port to be accurate-ish.  `--osscan-limit` Does not even attempt OS detection without meeting the criteria of one open one closed.
###### Guess OS Detection results
```
--osscan-guess; --fuzzy
```
- When nmap cannot perfectly detect the OS it sometimes offers near matches as possibilities. For it to do this by default it has to be very close. This option makes nmap guess more aggressively. Will give % certainty.
###### Set the maximum number of OS detection tries against a target
```
--max-os-tries
```
- When nmap fails to find a perfect match it usually repeats the attempt. Default tries 5 attempts if conditions are favorable, and twice when conditions are not good. `--max-os-tries` speeds nmap up, but miss the retry capabilitiy. Can be set to a higher number to tell nmap to keep trying. *Rarely done, except to generate better fingerprints for submission and intergration into the nmap os database*.
### Nmap Scripting Engine
- Location of nmap scripts
```
/usr/share/nmap/scripts
```
- Script categories: auth, broadcast, default, discovery, dos, exploit, external, fuzzer, intrusive, malwarer, safe, version, vuln
##### NSE 
- NSE is controlled with the `-sC` option
- `-sC` performs a script scan using the default set of scripts.  Same as `--script=default`. 
```
--script <filename>|<category>|<directory>/|<expression>[,...]
```
- Above syntax runs a script scan using the comma-separated list of filesname, script categories, and directories. 
##### Special Features
`+`
- Prefix the script name and expression with the `+` symbol to force them to run even if they normally wouldnt i.e. the relevant service wasnt detected on the target port.
`all`
- Used to specify every script in the nmap databse. Be carful with this the nse contains bruteforce and exploit scripts
#### Running NSE Scripts
- When refering to scripts from `script.db` by name use a shell-style wildcard.
```
nmap --script "http-*"
```
  - Loads all scripts whose name starts with `http-` such as `http-auth` and `http-open-proxy`.  The argument to `--script` has to be in quotes to protect the wildcard to the shell.
```
nmap --script "not intrusive"
```
  - Loads all scripts except those in the intrusive category.
```
namp --script "default or safe
```
  - Equivalent to `nmap --script "default,safe"`. It loads all scripts that are in the `default` category or the `safe` category.
```
nmap --script "(default or safe or intrusive) and not http-*"
```
  - Loads scripts in the `default`, `safe`, or `intrusive` categories except for whose names start with `http-`.
```
--script-args <n1>=<v1>,<n2>={<n3>=<v3>},<n4>={<v4>,<v5>}
```
- Lets you provide arguments to NSE scripts. Arguments are a comma-separated list of `name=value` pairs. To include one of these characters in a string, enclose the string in single or double quotes. Within a quoted string '\' escapes a quote. All other cases a \ is interpreted literally.
- Example
```
--script-args 'user=foo,pass=",{}=bar".whois={whodb=nofollow+ripe},xmpp-info.server_name=localhost'
--script-args-file <filename>
```
- Lets you load arguments to NSE scripts from a file.
