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
