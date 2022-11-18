# Windows Defender

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
