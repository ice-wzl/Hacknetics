# Windows Log Clearing 
- If you use the .bat script in this directory and it is blocked
````
unblock-file -path "C:\Users\Administrator\Desktop\filename.bat"
````
- Unblock All Files in a Folder in PowerShell - (without confirmation prompt)
````
get-childitem "full path of folder" | unblock-file
````
- OR

- (with confirmation prompt)
````
get-childitem "full path of folder" | unblock-file -confirm
````
## cmd.exe 
- One liner
````
for /F "tokens=*" %1 in ('wevtutil.exe el') DO wevtutil.exe cl "%1"
````
## powershell.exe 
- One liner 
````
Get-WinEvent -ListLog * | where {$_.RecordCount} | ForEach-Object -Process { [System.Diagnostics.Eventing.Reader.EventLogSession]::GlobalSession.ClearLog($_.LogName) }
````
- OR
````
Get-EventLog -LogName * | ForEach { Clear-EventLog $_.Log } 
````
- OR
````
wevtutil el | Foreach-Object {wevtutil cl "$_"}
````
## Manual 
- ![image](https://user-images.githubusercontent.com/75596877/173405840-0356ddb3-ee78-4f61-8085-fc923adecedc.png)

