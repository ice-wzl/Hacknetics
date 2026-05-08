# Remote Mouse

Remote Mouse is Windows desktop control software. If it is installed and running, check both the exposed control ports and the local GUI attack surface.

## Discovery

Look for the process and listening ports:

```cmd
tasklist /svc | findstr /i RemoteMouse
netstat -ano | findstr /i "1978 1979 1980"
```

Common listeners:

```text
TCP    0.0.0.0:1978    0.0.0.0:0    LISTENING
TCP    0.0.0.0:1979    0.0.0.0:0    LISTENING
TCP    0.0.0.0:1980    0.0.0.0:0    LISTENING
UDP    0.0.0.0:1978    *:*
```

Map the PID back to the binary:

```powershell
Get-Process -Id <PID>
```

Scan externally if the host firewall allows it:

```bash
nmap -sT TARGET -p 1978,1979,1980
```

## Remote Mouse 3.008

Known public references:

- CVE-2021-35448
- https://www.exploit-db.com/exploits/50047
- https://www.exploit-db.com/exploits/50258
- https://github.com/p0dalirius/RemoteMouse-3.008-Exploit

The remote control ports may be filtered from the network while the local GUI is still exploitable from an RDP session.

### Local GUI Privilege Escalation

If Remote Mouse 3.008 is running in the tray:

1. Open Remote Mouse from the system tray.
2. Go to **Settings**.
3. Click **Change...** in the **Image Transfer Folder** section.
4. In the **Save As** prompt, enter `C:\Windows\System32\cmd.exe` in the address bar.
5. A command prompt can spawn in the elevated Remote Mouse context.

Check context immediately:

```cmd
whoami /all
```