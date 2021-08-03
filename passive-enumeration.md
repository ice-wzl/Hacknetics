#### Whois
- Whois lookup is used to get general information about the domain such as the registrar, domain owner, contact info, and DNS Server used 
````
whois [domain]
whois cisco.com
````
#### Nslookup
- Stands for name server lookup used for querying the dns in order to obtain records
````
nslookup [domain]
nslookup cisco.com
````
- May have to install the dnsutils package
````
sudo apt-get install dnsutils -y
````
#### Query the DNS records
````
nslookup -type=[record type] [domain]
nslookup -type=any cisco.com
````
#### Host
- Another application to perform DNS lookups.  
````
host [domain]
````
#### Zone Transfers 
- DNS servers need to be highly available, when one goes down another steps in.  In order to have this setup function properly we have to make sure that both DNS servers have the same data, they need to synchronize data with each other on a regular basis. 
- A mechanism to replicate DNS databases is called a zone transfer, and the replicated database is called a DNS zone. 
- Zone transfer is when one DNS server -> transfers information to another DNS server
- Contains potentially a complete list of all hosts for a given zone
- Testing for Zone Transfers
- First you need to retrieve name servers for this domain with the Host tool. Then we will use Host again to test for zone transfers on the name server
- To retrieve the name servers for cisco.com domain name we use:
````
host -t ns cisco.com
````
- Output:
````
Cisco.com name server ns1.cisco.com
````
- Now that we know the name server we can supply it as an argument in the following command 
````
host -t axfr -l cisco.com ns1.cisco.com
````
#### Dig 
-Short for Domain Information Groper, is another tool for DNS servers.  
- To query a specific record type you can use the -t option (just like with Host).  The following command retrieves the mx records for the google.com domain:
````
dig -t mx google.com
````
- Or you can request all records 
````
dig -t any google.com
````
- Can also test for zone transfers:
````
dig axfr @nsztm1.digi.ninja zonetransfer.me [@name server domain]
````
#### Fierce
- Fierce is a recon tool written in perl to locate non contiguous IP space and hostnames using DNS.
- This tool helps locate targets inside and out of the corporate network.
````
fierce -h  
fierce -dns google.com
````
- Fierce will first list DNS Servers, attempt a zone transfer on every name server, checks for wildcard DNS record and attempts to brute force subdomains using an internal wordlist.
- By default fierce has its own wordlist but you can also use your own word list:
````
fierce -dns google.com -wordlist [path to wordlist]
````
#### DNSenum
- DNSenum is a perl script that can be used to enumerate the DNS information of a domain and to discover non contiguous IP blocks.  This tool will also attempt zone transfers.
```` 
dnsenum [domain name]
````
#### DNSrecon
- DNSrecon is another automated tool that can be used to query DNS records, check for zone transfers and other tasks.  
````
dnsrecon -d google.com
````
#### Sublist3r
- Sublist3r is a DNS meta-query spider that uses an extensive wordlist to enumerate DNS records and subdomains.  
- In attempting large numbers of entries Subbrute uses open resolvers to circumvent rate limiting issues 
- To install:
````
apt update && apt -y install sublist3r
````
- Default scan without subbrute:
````
sublist3r -d google.com
````
- To apply brute forcing with subbrute we add the -b option to the command and can specify the number of threads to use with the -t option
````
sublist3r -d google.com -b -t 100
````
#### The Harvester
- Example: we want to find any email address for the cisco.com domain using Yahoo.  
- We will specify the domain to search for with -d, the data source with -b and limit the results to 100 by adding -l 100:
````
theharvester -d cisco.com -b yahoo -l 100
````























