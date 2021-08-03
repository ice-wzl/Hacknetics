##### Whois
- Whois lookup is used to get general information about the domain such as the registrar, domain owner, contact info, and DNS Server used 
````
whois [domain]
whois cisco.com
````
##### Nslookup
- Stands for name server lookup used for querying the dns in order to obtain records
````
nslookup [domain]
nslookup cisco.com
````
- May have to install the dnsutils package
````
sudo apt-get install dnsutils -y
````
##### Query the DNS records
````
nslookup -type=[record type] [domain]
nslookup -type=any cisco.com
````
##### Host
- Another application to perform DNS lookups.  
````
host [domain]
````
##### Zone Transfers 
- DNS servers need to be highly available, when one goes down another steps in.  In order to have this setup function properly we have to make sure that both DNS servers have the same data, they need to synchronize data with each other on a regular basis. A mechanism to replicate DNS databases is called a zone transfer, and the replicated database is called a DNS zone. Zone transfer is when one DNS server -> transfers information to another DNS server
-Contains potentially a complete list of all hosts for a given zone
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




























