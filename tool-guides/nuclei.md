# nuclei

### About

* Nuclei is used to send requests across targets based on a template, leading to zero false positives and providing fast scanning on a large number of hosts. Nuclei offers scanning for a variety of protocols, including TCP, DNS, HTTP, SSL, File, Whois, Websocket, Headless etc. With powerful and flexible templating, Nuclei can be used to model all kinds of security checks.

### Installation&#x20;

* Kali

```
sudo apt update -y 
sudo apt install golang-go
sudo apt install nuclei
nuclei -h
```

### Ubuntu

```
sudo apt update -y
sudo apt install golang-go
cd /opt
git clone https://github.com/projectdiscovery/nuclei.git
cd nuclei/v2/cmd/nuclei/
sudo go build .
export $PATH=$PATH:/opt/nuclei/v2/cmd/nuclei #temp solution  
echo "$PATH=$PATH:/opt/nuclei/v2/cmd/nuclei" > ~/.bashrc #perm solution
source ~/.bashrc
```

### Easy Mode

```
nuclei -u https://my.target.site

#scan specific service 
nuclei -u my.target.site:5759

#scan multiple targets 
nuclei -l /path/to/list-of-targets.txt
```

### **Automatic Selection (-as)**

```
nuclei -u https:// my.target.site -as
```

This option will attempt to fingerprint the technology stack and components used on the target, then select templates that have been tagged with those tech stack keywords.

### **Rate Limiting** <a href="#rate-limiting" id="rate-limiting"></a>

```bash
nuclei -u https://my.target.site/ -rl 3 -c 2
```

These options allow restricting the number of requests being sent (150 per second by default) and how many concurrent templates are executed (25 by default). Example (restrict outgoing requests to 3 per second and only 2 concurrent templates)

### **Timeout Length (-timeout)**

```bash
nuclei -l list-of-targets.txt -timeout 1
```

<br>
