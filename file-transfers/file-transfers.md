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

## Nginx PUT Upload Server

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

## Sub-Pages

| Page | Covers |
|---|---|
| [PowerShell Transfers](powershell-transfers.md) | Net.WebClient, Invoke-WebRequest, BITS, Base64, PSUpload, WinRM, COM objects, AES encryption, evasion |
| [Linux Transfers](linux-transfers.md) | wget, curl, fileless, bash /dev/tcp, base64, SCP, OpenSSL |
| [Python Transfers](python-transfers.md) | http.server, uploadserver, download/upload one-liners |
| [PHP Transfers](php-transfers.md) | PHP web server, download one-liners, upload receiver |
| [Ruby & Perl Transfers](ruby-perl-transfers.md) | Ruby web server, Ruby/Perl download one-liners |
| [SMB Transfers](smb-transfers.md) | Impacket SMB server, Windows copy, WebDav |
| [FTP Transfers](ftp-transfers.md) | pyftpdlib, PowerShell FTP, FTP command files |
| [Netcat Transfers](netcat-transfers.md) | nc/ncat send/receive, /dev/tcp, gzip compression |
| [Windows Native Transfers](windows-native-transfers.md) | CertUtil, Bitsadmin, CertReq, RDP mount, cscript JS/VBS, LOLBINs |
