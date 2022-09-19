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



##

##

## Stuck

* https://book.hacktricks.xyz/
* https://guide.offsecnewbie.com/
