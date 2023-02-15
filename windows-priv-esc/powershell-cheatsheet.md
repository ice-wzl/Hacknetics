# powershell-cheatsheet

## Powershell

### Powershell Downgrade Attack

* Logging in Powershell past v2.0 is insane.  To limit this logging perform a version switch to 2.0

```
powershell.exe -Version 2.0 -NoLogo -NoProfile
```

### Resources

* https://learnxinyminutes.com/docs/powershell/

### Basic Enumeration

```
systeminfo
```

### Hotfixes

```
Get-HotFix | Format-List
Get-Hotfix -Id KB4023834
Get-Hotfix | measure
```

#### Creating Objects From Previous cmdlets

![Zdxicjj](https://user-images.githubusercontent.com/75596877/150692716-9d937291-9a6b-4e29-84b0-6a812eb31460.png)

```
Get-ChildItem | Select-Object -Property Mode, Name
```

* You can also use the following flags to select particular information:
* `first` - gets the first x object
* `last` - gets the last x object
* `unique` - shows the unique objects
* `skip` - skips x objects

#### Checking the Stopped Processes

```
Get-Service | Where-Object -Property Status -eq Stopped
```

#### Sort Object

```
Get-ChildItem | Sort-Object
```

## Find File Recursive

```
Get-Childitem –Path C:\ -Recurse -Force -ErrorAction SilentlyContinue | findstr /i "interesting-file.txt"
Get-ChildItem -Path C:\ -Include *.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue
```

* ![image](https://user-images.githubusercontent.com/75596877/150693932-501b2d5c-3695-4a41-8662-27b121d7f5ac.png)
* Hash File

```
Get-FileHash -Algorithm md5 .\interesting-file.txt.txt
```

* Will default to `SHA-256`

### See all Cmdlets Installed

```
Get-Command | Where-Object -Property CommandType -eq Cmdlet | measure
```

### Users

* See users on the sytem
* ![image](https://user-images.githubusercontent.com/75596877/150695096-edaaf297-0394-4213-a415-7d46cedecee2.png)

```
net users
Get-LocalUser
```

* See what user a SID belongs to

```
Get-LocalUser -SID "S-1-5-21-1394777289-3961777894-1791813945-501"
```

* Pull value from users

```
get-localuser * | select * #find parameter you want and then pass into second command value
get-localuser * | select * | findstr /i "Passwordrequired"
```

### Groups

* See Groups

```
Get-LocalGroup
```

### IP Address Information / TCP/UDP Connections

```
Get-NetIPAddress
Get-NetTCPConnections
GEt-NetTCPConnection | Where-Object -Property State -Match Listen
Get-Net-UDPEndpoints
```

* View all TCP ports `Listen`

```
Get-NetTCPConnection | Select RemoteAddress, State | findstr /i "Listen"
```

### Base64 Powershell Decode

```
certutil -decode "C:\Users\Administrator\Desktop\b64.txt" decode.txt
Get-Content decode.txt
```

### Find backup Files

```
Get-ChildItem -Path C:\ -Include *.bak* -File -Recurse -ErrorAction SilentlyContinue
```

* ![image](https://user-images.githubusercontent.com/75596877/150698655-206da003-197d-4899-8983-b59e2981f226.png)

### Find specific string inside a file

```
Get-ChildItem C:\* -Recurse | Select-String -pattern API_KEY
```

### Services and Processes

```
Get-Service
Get-Process
```

### Scheduled Tasks

```
Get-ScheduleTask -TaskName new-sched-task
Get-ScheduleTask
```

### See Owner and Access

```
Get-ACL C:\
```

* ![image](https://user-images.githubusercontent.com/75596877/150699211-9e56bd19-9287-452f-a5ab-c1dc71dabb7b.png)

### Scanners

* Localhost port scanner

```
 1..1024 | % {echo ((new-object Net.Sockets.TcpClient).Connect("127.0.0.1",$_)) "Port $_ is open!"} 2>$null
```

* PowerShell port scanner:

```
1..1024 | % {echo ((new-object Net.Sockets.TcpClient).Connect("10.0.0.100",$_)) "Port $_ is open!"} 2>$null
```

* Test-Netconnection scan a range of IPs for a single port:

```
foreach ($ip in 1..20) {Test-NetConnection -Port 80 -InformationLevel "Detailed" 192.168.1.$ip}
```

* PS IP range & port range scanner:

```
1..20 | % { $a = $_; 1..1024 | % {echo ((new-object Net.Sockets.TcpClient).Connect("10.0.0.$a",$_)) "Port $_ is open!"} 2>$null}
```

* PS test egress filtering:

```
1..1024 | % {echo ((new-object Net.Sockets.TcpClient).Connect("allports.exposed",$_)) "Port $_ is open!"
```
