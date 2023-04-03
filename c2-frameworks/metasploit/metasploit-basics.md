# Metasploit Basics

### MSFDB

* After install initialize the MSF database for the first time with&#x20;

```
sudo msfdb init
```

* View if the database is running/start the database&#x20;

```
sudo msfdb start
sudo msfdb status
sudo msfdb stop
```

* start the framework&#x20;

```
msfconsole -q
```

### Basics

* Search for modules&#x20;

```
search [regex]
```

* Specify exploit

```
use exploit /path/to/exploit
```

* Specify Payload&#x20;

```
set payload path/to/payload
```

* Set option

```
set [option] [value]
```

* Run Exploit

```
run
exploit 
#either will work 
```
