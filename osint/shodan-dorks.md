# Shodan Dorks

* Good Shodan Dorks from my experience&#x20;

### SMB

* only port 445, country Iran, smb shares that allow you to connect to at least one share
  * Admin shares (annotated with a $ at the end) may still require valid username and password but this dork is for devices in which you can connect to at least one share

```
port:445 country:IR "Authentication: disabled"
port:445 "Authentication: disabled"
```

### Python HTTP Servers

* only port 8000, hunts for `python simple http servers`
* people make mistakes and forget their http servers are running
* it is horrifying how many individuals are hosting their entire vps with items like `ssh keys` exposed

```
Title:"Directory listing for /" port:8000
```

### FTP

* only port 21, it hunts for FTP servers that have anonymous access allowed&#x20;
* there is a staggering number of these

```
port:21 "User logged in"
```

### Web

* targets port 80, but you can drop that part to find even more results.
* This dork targets exposed .pem files which can be terrible for websites if there certs are publically exposed

```
http.title:"Index of /" http.html:".pem" port:80
```

### Tor

* this searches shodan for headers that have `onion-location` in the headers
* this is a indication that they are hosting a hidden service
* this is a security concern for hidden services as the whole idea behind hidden services is to hide its location&#x20;

```
onion-location
```

### Cameras

* webcam7 dork

```
("webcam 7" OR "webcamXP") http.component:"mootools" -401
```



### Additional Dorks

* there are many repos out there with Shodan dorks, but this is by far the best one I have found:
* [https://github.com/lothos612/shodan](https://github.com/lothos612/shodan)
