# OSCP-Prep
## This repo is not complete yet, I am working on it daily.
## Methodology 
### Step 1 Recon
- Can you ping the target?
- Is your VPN still connected?
![alt text](https://github.com/DigitalAftermath/EnumerationVisualized/raw/master/enumeration-mind-map.png?raw=true)
## Path
### Start with recon-enumeration folder
- Start the scans: What is open?
- Use `autorecon 10.10.10.10 -v`
- Once completed, rescan all ports with service detection `nmap -sS -sV -sC 10.10.10.10 | tee nmap_output.txt`
- Consider running some targeted scripts against services running.
````
nmap --script "http*" 10.10.10.10 -p 8080 -vv | tee nmap_http_scripts.txt
````
- Identify the Ports and Services running.
#### Web Server Running?
- Go To: `/web/web-servers.md`
- Find out CMS type and version --> check `exploitdb`
- Look for usernames
- Run `nikto`, `gobuster` --> try and map out the website
- `robots.txt` file?
- Default Credentials
#### SSH/Telnet Running?
- Be on the look out for LFI on a web server --> Private keys
- Think about Hydra if you can find a username
#### Email Ports 25, 110, 143?
- `/recon-enumeration/recon-enumeration.md`
#### NFS port 2049
- `/recon-enumeration/recon-enumeration.md`
- Check for shares that are accessible 
