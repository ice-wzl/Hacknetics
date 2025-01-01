# feroxbuster

* My current favorite web spider, domain enumeration tool&#x20;

### Basic Scan&#x20;

```
feroxbuster -u http://cozyhosting.htb
```

### Proxy traffic through Burp

```
./feroxbuster -u http://127.1 --insecure --proxy http://127.0.0.1:8080
```

### Proxy traffic through a SOCKS proxy (including DNS lookups)

```
./feroxbuster -u http://127.1 --proxy socks5h://127.0.0.1:9050
```
