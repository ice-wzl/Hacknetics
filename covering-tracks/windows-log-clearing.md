# Windows Log Clearing 
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
