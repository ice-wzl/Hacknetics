# Spiderfoot

* Spiderfoot is an open source OSINT data collection and analysis&#x20;
* Support for Windows, Linux, macOS
* Need to provide a seed target such as a domain name, host name, or an email address
* Available at https://spiderfoot.net
* Spiderfoot HX (cloud version) offers many more options than the command line version

### Spiderfoot docker

* The best way to get spiderfoot going is with docker
* Download the latest release&#x20;

```
#un-tar the archive, and cd into the directory
sudo docker build -t spiderfoot .
#confirm all good 
sudo docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
spiderfoot   latest    f31101d48569   33 seconds ago   323MB
sudo docker run -p 5009:5001 -d spiderfoot
6f7a0f0ef099bc618d495da75d9ce57ff57ad5f85c9ba9315fce10fc45400724
sudo docker ps                            
CONTAINER ID   IMAGE        COMMAND                  CREATED         STATUS         PORTS                                       NAMES
6f7a0f0ef099   spiderfoot   "/opt/venv/bin/pytho…"   4 seconds ago   Up 3 seconds   0.0.0.0:5009->5001/tcp, :::5009->5001/tcp   bold_ride

```

* Now connect to the instanse with the spiderfoot client&#x20;

```
python ./sfcli.py -s http://localhost:5009
 
  _________      .__    .___          ___________            __                                                     
 /   _____/_____ |__| __| _/__________\_   _____/___   _____/  |_                                                   
 \_____  \\____ \|  |/ __ |/ __ \_  __ \    __)/  _ \ /  _ \   __\                                                  
 /        \  |_> >  / /_/ \  ___/|  | \/     \(  <_> |  <_> )  |                                                    
/_______  /   __/|__\____ |\___  >__|  \___  / \____/ \____/|__|                                                    
        \/|__|           \/    \/          \/                                                                       
                Open Source Intelligence Automation.                                                                
                by Steve Micallef | @spiderfoot
                                                                                                                    
[*] Version 4.0.0.
[*] Server http://localhost:5009 responding.
[*] Loaded previous command history.
[*] Type 'help' or '?'.
sf> 

```

### Connecting

* IMO it is much easier to use the WebUI version vice CLI
* To connect as a client simply browse to `http://localhost:5009`
