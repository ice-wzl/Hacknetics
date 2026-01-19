# Pentesting DNS

### **Whois**

* Whois lookup is used to get general information about the domain such as the registrar, domain owner, contact info, and DNS Server used

```
whois [domain]
whois cisco.com
```

### **Nslookup**

* Stands for name server lookup used for querying the dns in order to obtain records

```
nslookup [domain]
nslookup cisco.com
```

* May have to install the dnsutils package

```
sudo apt-get install dnsutils -y
```

#### **Query the DNS records**

```
nslookup -type=[record type] [domain]
nslookup -type=any cisco.com
```

### nslookup information leakage&#x20;

* You can often get a computer with dns open to disclose its hostname to you by getting it to query itself.

```
nslookup
> server <ip of target>
> 127.0.0.1
> 127.0.0.2
> <ip of target>
```

### **Host**

* Another application to perform DNS lookups.

```
host [domain]
```

### **Zone Transfers**

* DNS servers need to be highly available, when one goes down another steps in. In order to have this setup function properly we have to make sure that both DNS servers have the same data, they need to synchronize data with each other on a regular basis.
* A mechanism to replicate DNS databases is called a zone transfer, and the replicated database is called a DNS zone.
* Zone transfer is when one DNS server -> transfers information to another DNS server
* Contains potentially a complete list of all hosts for a given zone
* Testing for Zone Transfers
* First you need to retrieve name servers for this domain with the Host tool. Then we will use Host again to test for zone transfers on the name server
* To retrieve the name servers for cisco.com domain name we use:

```
host -t ns cisco.com
```

* Output:

```
Cisco.com name server ns1.cisco.com
```

* Now that we know the name server we can supply it as an argument in the following command

```
host -t axfr -l cisco.com ns1.cisco.com
```

### **Dig**

-Short for Domain Information Groper, is another tool for DNS servers.

* To query a specific record type you can use the -t option (just like with Host). The following command retrieves the mx records for the google.com domain:

```
dig -t mx google.com
```

* Or you can request all records

```
dig -t any google.com
```

* Can also test for zone transfers:

```
dig axfr @nsztm1.digi.ninja zonetransfer.me [@name server domain]
```

* Using dig to subdomain bruteforce

```
for sub in $(cat /usr/share/seclists/Discovery/DNS/fierce-hostlist.txt);do dig $sub.trilocor.local @10.129.204.10 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains-dig.txt;done
```

### **Fierce**

* Fierce is a recon tool written in perl to locate non contiguous IP space and hostnames using DNS.
* This tool helps locate targets inside and out of the corporate network.

```
fierce -h  
fierce -dns google.com
```

* Fierce will first list DNS Servers, attempt a zone transfer on every name server, checks for wildcard DNS record and attempts to brute force subdomains using an internal wordlist.
* By default fierce has its own wordlist but you can also use your own word list:

```
fierce -dns google.com -wordlist [path to wordlist]
```

### **DNSenum**

* DNSenum is a perl script that can be used to enumerate the DNS information of a domain and to discover non contiguous IP blocks. This tool will also attempt zone transfers.

```
dnsenum [domain name]
```

* subdomain bruteforce
* https://github.com/fwaeytens/dnsenum&#x20;

```
dnsenum --dnsserver 10.129.33.40 --enum -p 0 -s 0 -o subdomains.txt -f /usr/share/seclists/Discovery/DNS/fierce-hostlist.txt inlanefreight.htb --threads 64
```

### **DNSrecon**

* DNSrecon is another automated tool that can be used to query DNS records, check for zone transfers and other tasks.

```
dnsrecon -d google.com
```

<pre><code><strong>user@slingshot:~$ dnsrecon -n 8.8.8.8 -d clifbar.com  -w
</strong>[*] Performing General Enumeration of Domain: clifbar.com
[-] DNSSEC is not configured for clifbar.com
[*]      SOA ns-1288.awsdns-33.org 205.251.197.8
...trimmed for brevity...
[*]      SRV _sip._tls.clifbar.com pulsip.clifbar.com 87.246.98.42 443 0
[+] 9 Records Found
[*] Performing Whois lookup against records found.
[*] The following IP Ranges where found:
[*]      0) 205.251.192.0-205.251.255.255 Amazon.com, Inc.
[*]      1) 205.251.192.0-205.251.199.255 Amazon Data Services NoVa
[*]      2) 67.231.144.0-67.231.159.255 Proofpoint, Inc.
[*]      3) 13.200.0.0-13.239.255.255 Amazon Technologies Inc.
[*]      4) 13.224.0.0-13.227.255.255 Amazon.com, Inc.
[*]      5) 213.128.224.0-213.128.255.255 UK-SOL-20020703
[*]      6) 87.246.76.32-87.246.76.63 pulsant15311
[*]      7) 87.246.98.0-87.246.98.127 pulsant1880
[*] What Range do you wish to do a Revers Lookup for?
[*] number, comma separated list, a for all or n for none
</code></pre>

* `-w` is for a more in depth enumeration.

### **Sublist3r**

* Sublist3r is a DNS meta-query spider that uses an extensive wordlist to enumerate DNS records and subdomains.
* In attempting large numbers of entries Subbrute uses open resolvers to circumvent rate limiting issues
* To install:

```
apt update && apt -y install sublist3r
```

* Default scan without subbrute:

```
sublist3r -d google.com
```

* To apply brute forcing with subbrute we add the -b option to the command and can specify the number of threads to use with the -t option

```
sublist3r -d google.com -b -t 100
```

### SUBBRUTE

* https://github.com/TheRook/subbrute&#x20;

```
git clone https://github.com/TheRook/subbrute.git >> /dev/null 2>&1 
cd subbrute 
echo "ns1.inlanefreight.htb" > ./resolvers.txt 
./subbrute.py inlanefreight.htb -s ./names.txt -r ./resolvers.txt ./subbrute.py inlanefreight.htb -s ./newnames.txt -r ./resolvers.txt -c 16 -p
```

### SUBFINDER

https://github.com/projectdiscovery/subfinder&#x20;

```
./subfinder -d inlanefreight.com -v
```

### **The Harvester**

* Example: we want to find any email address for the cisco.com domain using Yahoo.
* We will specify the domain to search for with -d, the data source with -b and limit the results to 100 by adding -l 100:

```
theharvester -d cisco.com -b yahoo -l 100
```

### crt.sh (Certificate Transparency)

* Certificate Transparency site can reveal subdomains via SSL certificates
* https://crt.sh

```bash
# Find all subdomains via crt.sh API
curl -s "https://crt.sh/?q=TARGET.com&output=json" | jq -r '.[].name_value' | sort -u

# Filter for specific subdomain pattern (e.g., "dev")
curl -s "https://crt.sh/?q=TARGET.com&output=json" | jq -r '.[] | select(.name_value | contains("dev")) | .name_value' | sort -u
```

### DNSCAN

* https://github.com/rbsec/dnscan

```
./dnscan.py -d cyberbotic.io -w subdomains-100.txt
```

### PUREDNS

* https://github.com/d3mondev/puredns#getting-started&#x20;
* https://sidxparab.gitbook.io/subdomain-enumeration-guide/active-enumeration/dns-bruteforcing&#x20;

```
puredns bruteforce best-dns-wordlist.txt trilocor.local -r resolvers.txt -w stuff/subdomains-out.txt
```

## GOTATOR - WORD LIST GENERATOR TOOL

* https://sidxparab.gitbook.io/subdomain-enumeration-guide/active-enumeration/permutation-alterations&#x20;
* ```
  gotator -sub subdomains.txt -perm permutations_list.txt -depth 1 -numbers 10 -mindup -adv -md > gotator1.txt puredns resolve permutations.txt -r resolvers.txt
  ```

## Subdomain Takeover

* [https://0xpatrik.com/takeover-proofs/](https://0xpatrik.com/takeover-proofs/)
* Validate with&#x20;
  * [https://punksecurity.co.uk/dnsreaper/](https://punksecurity.co.uk/dnsreaper/)
  * [https://github.com/EdOverflow/can-i-take-over-xyz](https://github.com/EdOverflow/can-i-take-over-xyz)

## Domain Spoofing

### Ettercap

* https://www.ettercap-project.org/
* EDIT /etc/ettercap/etter.dns TO MAP TARGET DOMAIN

```
cat /etc/ettercap/etter.dns inlanefreight.com A 192.168.225.110 *.inlanefreight.com A 192.168.225.110
```

* Start ettercap and scan for live hosts

```
Hosts > Scan for Hosts
```

* Add ips to targets, activate DNS\_SPOOF

```
Plugins > Manage Plugins
```

### Spoofy

* https://github.com/MattKeeley/Spoofy.git

```
python3 -m venv venv / source venv/bin/activate / pip3 install -r requirements
```

* Tool use

```
python3 spoofy.py -d cyberbotic.io -o stdout
```

#### Example output

```
[*] Domain: cyberbotic.io
[*] Is subdomain: False
[*] DNS Server: 1.1.1.1
[?] No SPF record found.
[?] No DMARC record found.
[+] Spoofing possible for fakedomain.io.
```
