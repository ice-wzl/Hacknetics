# Windows Host Forensics

### Windows Process with wmic

* Get a brief output of running processes

```
wmic process list brief 
```

* Get a large amount of output from running processes

```
amic process list full
```

* Get specific information about running processes&#x20;

```
wmic process get name,parentprocesspid,processid
```

* Focus in on a specific process&#x20;

```
wmic process where processid=pid_number get commandline
```

### Network Connections

* Overview of connections

```
netstat -na
```

* Show the owning process ID and associated exe's / DLLs

```
netstat -naob
```

* Refresh network connections every 5 seconds

```
netstat -naob 5
```

* Examine the built-in firewall settings Windows 7 -- Windows 10

```
netsh advfirewall show currentprofile
```

###
