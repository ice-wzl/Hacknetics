# AV Evasion
## Applocker
- AppLocker is an application whitelisting technology introduced with Windows 7. 
- It allows restricting which programs users can execute based on the programs path, publisher and hash.
- If AppLocker is configured with default AppLocker rules, we can bypass it by placing our executable in the following directory: 
````
C:\Windows\System32\spool\drivers\color
````
- This is whitelisted by default.
-Windows powershell saves all previous commands into a file called ConsoleHost_history. 
This is located at 
````
%userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
````





























