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

```
GET / HTTP/1.0
host: netcat
```

### NetCat FTP Banner Grab

![nc ftp](https://user-images.githubusercontent.com/75596877/138183900-60957ad6-0460-44d9-b64a-14cbd2f6e4a1.png)
