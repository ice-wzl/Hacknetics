# Windows Survey

* Quick Windows Survey&#x20;

```
//powershell only
$ExecutionContext.SessionState.LanguageMode
[System.Environment]::OSVersion.Version
dir env:
----
systeminfo 
whoami /priv  
ipconfig /all 
route print  
net users   
qwinsta  
net localgroup    
set  
net use
net share
tasklist /v /fi "username eq system"
tasklist /svc
--or--
tasklist /v
netstat -ano
netsh firewall show state 
netsh firewall show config 
schtasks /query
```
