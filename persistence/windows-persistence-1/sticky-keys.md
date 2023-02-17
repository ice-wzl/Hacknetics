# Sticky Keys

* To establish persistence using Sticky Keys, we will abuse a shortcut enabled by default in any Windows installation that allows us to activate Sticky Keys by pressing SHIFT 5 times.
* After inputting the shortcut, we should usually be presented with a screen that looks as follows:

<figure><img src="https://user-images.githubusercontent.com/75596877/181267438-2b171902-fbbe-4bb9-b08e-7c3c69e40795.png" alt=""><figcaption></figcaption></figure>

* After pressing SHIFT 5 times, Windows will execute the binary in `C:\Windows\System32\sethc.exe`.
* If we are able to replace such binary for a payload of our preference, we can then trigger it with the shortcut. Interestingly, we can even do this from the login screen before inputting any credentials.
* A straightforward way to backdoor the login screen consists of replacing `sethc.exe` with a copy of `cmd.exe`.
* That way, we can spawn a console using the sticky keys shortcut, even from the logging screen.
* To overwrite `sethc.exe`, we first need to take ownership of the file and grant our current user permission to modify it.
* Only then will we be able to replace it with a copy of `cmd.exe`. We can do so with the following commands:

```
takeown /f c:\Windows\System32\sethc.exe

SUCCESS: The file (or folder): "c:\Windows\System32\sethc.exe" now owned by user "PURECHAOS\Administrator".

icacls C:\Windows\System32\sethc.exe /grant Administrator:F
processed file: C:\Windows\System32\sethc.exe
Successfully processed 1 files; Failed processing 0 files

copy c:\Windows\System32\cmd.exe C:\Windows\System32\sethc.exe
Overwrite C:\Windows\System32\sethc.exe? (Yes/No/All): yes
        1 file(s) copied.
```

* After doing so, lock your session from the start menu:
* You should now be able to press SHIFT five times to access a terminal with SYSTEM privileges directly from the login screen:

![](https://user-images.githubusercontent.com/75596877/181267037-094a49f2-7a4c-4a80-bee8-2a1ea8e14c52.png)

## Utilman

* Notice that this registry key has no equivalent in HKLM, making your backdoor apply to the current user only.
* After doing this, sign out of your current session and log in again, and you should receive a shell (it will probably take around 10 seconds).
* Utilman is a built-in Windows application used to provide Ease of Access options during the lock screen:
* When we click the ease of access button on the login screen, it executes `C:\Windows\System32\Utilman.exe` with `SYSTEM` privileges. If we replace it with a copy of `cmd.exe`, we can bypass the login screen again.
* To replace `utilman.exe`, we do a similar process to what we did with `sethc.exe`:
