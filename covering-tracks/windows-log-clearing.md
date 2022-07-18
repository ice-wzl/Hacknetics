# Windows Log Clearing

```
@echo off

FOR /F "tokens=1,2*" %%V IN ('bcdedit') DO SET adminTest=%%V
IF (%adminTest%)==(Access) goto noAdmin
for /F "tokens=*" %%G in ('wevtutil.exe el') DO (call :do_clear "%%G")
echo.
echo All Event Logs have been cleared!
goto theEnd

:do_clear
echo clearing %1
wevtutil.exe cl %1
goto :eof

:noAdmin
echo Current user permissions to execute this .BAT file are inadequate.
echo This .BAT file must be run with administrative privileges.
echo Exit now, right click on this .BAT file, and select "Run as administrator".  
pause >nul

:theEnd
Exit
```

* Above `.bat` script will clear all windows logs, make sure to run with admin privileges!
* If you use the .bat script (see above) and it is blocked

```
unblock-file -path "C:\Users\Administrator\Desktop\filename.bat"
```

* Unblock All Files in a Folder in PowerShell - (without confirmation prompt)

```
get-childitem "full path of folder" | unblock-file
```

* OR
* (with confirmation prompt)

```
get-childitem "full path of folder" | unblock-file -confirm
```

## cmd.exe

* One liner

```
for /F "tokens=*" %1 in ('wevtutil.exe el') DO wevtutil.exe cl "%1"
```

## powershell.exe

* One liner

```
Get-WinEvent -ListLog * | where {$_.RecordCount} | ForEach-Object -Process { [System.Diagnostics.Eventing.Reader.EventLogSession]::GlobalSession.ClearLog($_.LogName) }
```

* OR

```
Get-EventLog -LogName * | ForEach { Clear-EventLog $_.Log } 
```

* OR

```
wevtutil el | Foreach-Object {wevtutil cl "$_"}
```

## Manual

* ![image](https://user-images.githubusercontent.com/75596877/173405840-0356ddb3-ee78-4f61-8085-fc923adecedc.png)
