# Windows Defender

* Defender can be a pain, but generally bypasses are abundant. This page is focused on enumeration not bypasses.

### Defender Enumeration with Powershell

```
Get-MpComputerStatus    #See the status of Defender 
Get-MpPreference        #See current Defender preferences
Add-MpPreference        #Change Defender Settings
Get-MpThreat            #See threat history for computer
Get-MpThreatCatalog     #Show any known threats
Get-MpThreatDetection   #Show all history for any detected threats
Remove-MpThreat         #Remove an active threat
Remove-MpPreference     #Create exclusion and default behavior 
Start-MpScan            #Start Defender Scan
Update-MpSignature      #Signature updates
Set-MpPreference        #Configures scans and updates     
```

### Processes&#x20;

```
tasklist /v 
```

* look for:

```
MsMpEng.exe
MpCmdRun.exe
```

### File System artifacts&#x20;

* download below files

```
dir "C:\ProgramData\Microsoft\Windows Defender\Support\MPLOG-<Datetime>.log"
dir "C:\ProgramData\Microsoft\Windows Defender\Support\MPDetection-<Datetime>.log"
```

### Registry&#x20;

```
reg query "HKLM\Software\Microsoft\Windows Defender"
reg query "HKLM\Software\Microsoft\Windows Defender\Real-Time Protection"
reg query "HKLM\Software\Microsoft\Windows Defender\Features"
reg query "HKLM\Software\Microsoft\Windows Defender\SpyNet"
reg query "HKLM\Software\Microsoft\Windows Defender\Windows Defender Exploit Guard"
reg query "HKLM\Software\Microsoft\Windows Defender\exclusions\paths"
```

### Enable Disable RealtimeProtection Powershell

* Turn On Real-time Protection

```
Set-MpPreference -DisableRealtimeMonitoring 0​​
Set-MpPreference -DisableRealtimeMonitoring $false
```

* Turn Off Real-time Protection

```
Set-MpPreference -DisableRealtimeMonitoring 1
Set-MpPreference -DisableRealtimeMonitoring $true
```
