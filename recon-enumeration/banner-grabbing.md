# Banner Grabbing

## Telnet Banner Grab

```
telnet 10.10.182.147 80
GET / HTTP/1.0
host: telnet
```

```
GET / HTTP/1.1
host: telnet
```

![telnet banner grab](https://user-images.githubusercontent.com/75596877/138183428-3c6b4c51-f1c4-4c48-9038-f252f6110a70.png)

## NetCat Banner Grab

```
nc 10.10.182.147
GET / HTTP/1.1
host: netcat
```

**When Nmap -sV truncates or omits banner detail:** Connect manually with `nc` and capture with `tcpdump`. The full banner often arrives in a **PSH-ACK** segment (`Flags [P.]`) that Nmap may not display.

```bash
# Terminal 1: capture traffic between you and target
sudo tcpdump -i eth0 host 10.10.14.2 and 10.129.2.28

# Terminal 2: connect to the service
nc -nv 10.129.2.28 25
```

In the tcpdump output, look for the `Flags [P.]` (PSH-ACK) line — it contains the full banner, e.g. `220 inlane ESMTP Postfix (Ubuntu)`.

```
GET / HTTP/1.0
host: netcat
```

### NetCat FTP Banner Grab

![nc ftp](https://user-images.githubusercontent.com/75596877/138183900-60957ad6-0460-44d9-b64a-14cbd2f6e4a1.png)

### Openssl banner grab&#x20;

* Used when https is open on the host&#x20;

```
openssl s_client -connect domain.com:443 
GET / HTTP/1.0
```

## HTTP Header Grabbing (curl)

```bash
# HTTP headers only (no body)
curl -I http://TARGET
curl -I https://TARGET

# Follow redirects
curl -IL http://TARGET
```

Look for:
- `Server:` - Web server software/version
- `X-Powered-By:` - Backend technology (PHP, Express, etc.)
- `X-Redirect-By:` - CMS (e.g., WordPress)