# Windows Host Forensics

### Windows Process with wmic

* Get a brief output of running processes

```
wmic process list brief 
```

* Get a large amount of output from running processes

```
wmic process list full
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

### Windows Services

* Examine services via GUI built-in

```
services.msc
```

* Examine running services&#x20;

```
net start
```

* Get details about each service

```
sc query | more
```

* Map running process to windows services&#x20;

```
tasklist /svc
```

### Registry ASEPs

* Check common problem areas in Windows Registry&#x20;

```
#HKLM
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnceEx
#HKCU
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnceEx
```

### Checking for Malicious Accounts

* Windows built-in&#x20;

```
lusrmgr.msc
```

* List users / view user group membership

```
net user 
net user <username>
net localgroup Administrators
```

### Scheduled Tasks

* View using the GUI

```
schtasks
```

* Remember if using the CLI the `at` command will only show tasked where `at` was used to set up the task, `schtasks` shows all tasks.

### Unusual Log Entries&#x20;

* Suspicious Log entiries to look for, low hanging fruit

```
Event log services was stopped
Windows File Protection is not active on this system
A member was added to a security-enabled local group
##Several Failed logon attempts##
```

* For Win7 -- Win 10

```
wevtutil qe security /f:text
#Or
Get-EventLog -LogName Security | Format-List -Property *
```

### Key Sysinternals tools

* `Process Explorer` Enumerate running processes
* `Autoruns` Display a list of Autostart Extensibility Points (ASEP)
* `Process Monitor` Show file system, network, registry, and process information in real time
* `TCPView` Maps listening and active TCP UDP activity to applications
* `Procdump` Capture memory for a running process for analysis&#x20;
