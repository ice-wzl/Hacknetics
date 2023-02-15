# Scanning

## AutoRecon

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

### Detecting Linux Version from nmap SSH output

* If ssh is running on the target, and it can fingerprint the service you have a good chance of detecting the operating system version:

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 29:dd:8e:d7:17:1e:8e:30:90:87:3c:c6:51:00:7c:75 (RSA)
|   256 80:a4:c5:2e:9a:b1:ec:da:27:64:39:a4:08:97:3b:ef (ECDSA)
|_  256 f5:90:ba:7d:ed:55:cb:70:07:f2:bb:c8:91:93:1b:f6 (ED25519)

```

* Take a look at the part `4ubuntu0.5`
* If you google that and select the `launchpad.net` link it will tell you the OS version&#x20;
* [https://launchpad.net/ubuntu/+source/openssh/1:7.6p1-4ubuntu0.5](https://launchpad.net/ubuntu/+source/openssh/1:7.6p1-4ubuntu0.5)

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

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
