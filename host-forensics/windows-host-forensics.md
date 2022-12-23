# Windows Host Forensics

### Windows CLI Basics

| Command                  | Action                           |
| ------------------------ | -------------------------------- |
| dir                      | list files and folders           |
| cd \<dir>                | change to directory              |
| mkdir \<dir>             | make directory                   |
| rmdir \<dir>             | deliete directory                |
| copy \<source> \<target> | copy source to target            |
| move \<source> \<target> | move file from source to target  |
| ren \<old> \<new>        | rename form old to new           |
| del \<file>              | delete file                      |
| echo \<text>             | display text to STDOUT           |
| type \<text.txt>         | display contents of file         |
| cls                      | clear screen                     |
| ver                      | Windows Version + Build          |
| \<drive>:                | Change Drive                     |
| ipconfig /all            | get ip address                   |
| sc query state=all       | show services                    |
| tasklist /m              | show services and processes      |
| taskkill /PID \<PID> /F  | force kill process by id         |
| assoc                    | Show file type association       |
| cipher /w:\<dir>         | secure delete file or directory  |
| fc \<file> \<file>       | file compare                     |
| netstat -an              | display currently opened ports   |
| pathping                 | displays each hop in ping        |
| tracert                  | displays each hop and time       |
| powercfg                 | change power configuration       |
| chkdsk /f \<drive>       | check and fix disk errors        |
| drivequery /FO list /v   | list of drivers and status       |
| osk                      | on screen keyboard               |
| shutdown -s -t 3600      | schedule shutdown for 1 hour     |

### Powershell common cmdlets

| Command                          | Alias   | Action                                                                   |
| -------------------------------- | ------- | ------------------------------------------------------------------------ |
| Get-Content                      | cat     | get contents of file                                                     |
| Get-Service                      | gsv     | get services                                                             |
| Get-Process                      | gps     | show services and processes                                              |
| Stop-Processes -Id \<PID> -Force | kill    | force kill by pid                                                        |
| Clear-Content                    | clc     | clear contents of file                                                   |
| Get-Command                      | gc      | gets all commands                                                        |
| Compare-Object \<f1> \<f2>       | compare | compare f1 and f2                                                        |
| Copy-Item                        | cp      | copy and item                                                            |
| Get-Member                       | gm      | gets the properties and methods for objects                              |
| Invoke-WMIMethod                 | iwmi    | calls windows management instrumentation methods                         |
| cmd /c \<command                 |         | run command as windows command line                                      |
| Set-Alias                        | sal     | creates or changes an alias                                              |
| Select-Object                    | select  | selects objects or object properties                                     |
| ForEach-Object                   | %       | performs an operation against each item in a collection of input objects |
| Where-Object                     | ?       | selects objects from a collection based on their property values         |

### Windows Directories to examine

```powershell
#dns file
"C:\Windows\System32\drivers\etc\hosts"
#network config file
"C:\Windows\System32\drivers\etc\networks"
#usernames and passwords
"C:\Windows\System32\config\SAM"
#security log
"C:\Windows\System32\config\SECURITY"
#software log
"C:\Windows\System32\config\SOFTWARE"
#windows event logs
"C:\Windows\System32\winevt\*"
#backup of user and password
"C:\Windows\repair\SAM"
#Windows xp all users start up
"C:\Documents and Settings\All Users\Start Menu\Programs\Startup\*"
#windows xp user startup
"C:\Documents and Settings\User\Start Menu\Programs\Startup"
#windows all user startup
"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
#windows user startup
"C:\Users\*\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\StartUp"
#prefetch files
"C:\Windows\Prefetch"
#amcache.hve
"C:\Windows\AppCompat\Programs\Amcache.hve"
#NTUSER.dat
"C:\Windows\Users\*\NTUSER.dat"
```

###

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

### Registry ASEPs/Registry Persistance

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

* Additional Persistance Keys

```
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
```

### Common Windows Registry Locations to Check&#x20;

```powershell
#os information 
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion"
#product name 
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion" /v ProductName
#data of install 
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion" /v InstallDate
#registered owner
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion" /v RegisteredOwner
#system root
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion" /v SystemRoot
#time zone
reg query "HKLM\System\CurrentControllerSet\Control\TimeZoneInformation" /v ActiveTimeBias
#mapped network drives
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Explorer\Map Network Drive MRU"
#mounted devices
reg query "HKLM\System\MountedDevices"
#usb devices
reg query "HKLM\System\CurrentControllerSet\Enum\USBStor"
#audit policies
reg query "HKLM\Security\Policy\PolAdTev"
#installed software (machine)
reg query "HKLM\Softwware"
#installed software (user)
reg query "HKCU\Software"
#recent documents
reg query "HKCU\Software\Microsoft\Windows\Currentversion\Explorer\RecentDocuments"
#recent user locations
reg query "HKCU\Software\Microsoft\Windows\Currentversion\Explorer\ComDlg32\LastVistitedMRU"
#typed urls
reg query "HKCU\Software\Microsoft\Internet Explorer\TypedURLs"
#mru list
reg query "HKCU\Software\Microsoft\Windows\Currentversion\Explorer\RunMRU"
#last accessed registry keys
reg query "HKCU\Software\Microsoft\Windows\Currentversion\Applets\RegEdit" /v LastKey
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

### Dump Windows Memory&#x20;

```
winpmem_mini.exe 20221218-ircase#0100.mem
```

### Volatility

* Best to use a virtual enviroment&#x20;

```
python3 -m venv venv
source venv/bin/activate
```

#### General Usage&#x20;

```
./vol.py -f image_name --profile profile_name plugin_name
```

* Save off some enviromental variables that will help with command length and typos

```
export VOLATILITY_LOCATION=file:///path/image
export VOLATILITY_PROFILE=profile
```

#### Vol Plugins

* There are alot of created plugins, view plugins

```
python vol.py --info
```

#### Basic Image Information (Start Here)

* This provides basic information about the image, will suggest which volatility plugin to use&#x20;

```
./vol.py imageinfo
#OR on windows cmd
ver
#Output 
Microsoft Windows [Version 10.0.20348.1249]
#now search for the build version 
python vol.py --info | grep 20348
```

#### Listing Processes

```
vol.py pslist
```

#### Parent and Child Processes&#x20;

```
vol.py pstree
```

#### Network Connections

```
vol.py netscan
```

#### UserAssist&#x20;

* UserAssist registry keys track any program run from the GUI, create for creating IR timelines

```
vol.py userassist
```

#### Processs Command Line&#x20;

* See full command line used to start processes&#x20;

```
vol.py cmdline
```

#### Guidelines

* Suspicious process --> `pslist`, `pstree`
* Network Listener --> `netscan`, check processes&#x20;
* Suspicious program --> `userassist` , `cmdline` , processes
* Others --> `hivelist` `printkey` `svcscan` `dllist`

### Detecting PSEXEC in logs

```
Get-WinEvent -FilterHashTable @{ Logname='System'; ID='7045'} | where {$_.Message.contains("PSEXEC")}
```

### Enable Script Block Logging

```
New-Item -Path "HKLM\SOFTWARE\Wow6432Node\Policies\Microsoft\Windows\Powershell\ScriptBlockLogging" -Force
Set-ItemProperty -Path "HKLM\SOFTWARE\Wow6432Node\Policies\Microsoft\Windows\Powershell\ScriptBlockLogging" -Name "EnableScriptBlockLogging" -Value 1 -Force
```
