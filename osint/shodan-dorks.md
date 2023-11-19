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
