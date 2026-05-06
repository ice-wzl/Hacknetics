# ttyd

`ttyd` exposes a terminal over HTTP/WebSocket. If it is unauthenticated, browsing to the service can give an interactive shell directly in the browser.

## Discovery

```bash
nmap -sC -sV TARGET -p 8000
# 8000/tcp open  http  ttyd 1.7.3
# http-title: ttyd - Terminal
# http-server-header: ttyd/1.7.3
```

Browse to:

```text
http://TARGET:8000/
```

## What To Check

After landing in the browser shell:

```bash
id
pwd
hostname
ss -antpu
ps -elf --forest
ls -la /opt
```

Check how `ttyd` was launched. Supervisor configs often disclose the working directory, user context, and other local services:

```bash
cat /etc/supervisor/supervisord.conf
ls -la /etc/supervisor/conf.d/
cat /etc/supervisor/conf.d/*.conf
```

Example:

```ini
[program:ttyd]
user=user
command=ttyd -p 8000 -w /home/user/ -W bash
```

`-W` allows clients to write to the terminal. If exposed without authentication, treat it as shell access.
