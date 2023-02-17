# Special Privileges and Security Descriptors

#### Overview

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
