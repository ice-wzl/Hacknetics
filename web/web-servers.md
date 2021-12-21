# Web Servers
![alt text](https://gblobscdn.gitbook.com/assets%2F-LSy0aAo8OKT4I-Ahftv%2F-MJOTqJ9Kdy3dIFdYcWY%2F-MJOTysqaRR8JH_lJByq%2FWeb%20Enumeration_OffSecNewbie.com.png)
## Web Servers
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
#### Example full syntax
````
dirb http://10.10.10.10:80/secret/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -X .txt 
````
- This command tests the /secret/ directory 
- It specifies to use the wordlist `directory-list-2.3-medium.txt`
- With the `-x` flag it sets gobuster to test for `.txt` file extensions i.e. admin.txt, secret.txt
### Gobuster Sub-Domain Enumeration
````
gobuster vhost -u http://horizontall.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t 150
/\/\/\/\/\/\/\/\/\/\/
Found: api-prod.horizontall.htb (Status: 200) [Size: 413]
````
### Dirsearch

- Full Syntax
````
dirsearch -u http://10.10.54.223:80/island/2100 -t 16 -r -e ticket -f -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
````
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
### BFAC
- Advanced backup-file artifacts for testing web applications
- https://github.com/mazen160/bfac
- Install 
````
git clone https://github.com/mazen160/bfac
sudo python3 setup.py install
````
- Find backup files on the website/application
````
bfac --url http://$ip/ --level 4
````
- If you manage to download a backupfile, grep for users - might be a password as well
## Burp Spider Website
- Set Foxy Proxy to 127.0.0.1 8080 and enable it 
- Turn off intercept
- Refresh the page you want to spider
- Navigate to `Target/Site Map` in `Burp Suite`
![Screenshot 2021-11-15 161926](https://user-images.githubusercontent.com/75596877/141855360-dcc55d3f-f455-4605-8a07-a9987d8dec2e.png)




