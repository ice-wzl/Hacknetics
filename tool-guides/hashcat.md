# Hashcat

## Generating hashes (printf vs echo)

When you need to **generate a hash** for comparison, overwriting a stored hash, or building a hash:password pair (e.g. for salted formats), use **`printf`**, not **`echo`**. `echo` is inconsistent and easy to get wrong:

| Command | What gets hashed | SHA256 result |
|--------|------------------|---------------|
| `echo "hello"` | `hello` + newline (6 bytes) | `5891b5b5...` |
| `echo -n "hello"` | `hello` (5 bytes) ✓ | `2cf24dba...` |
| `echo -n 0 "hello"` | `0hello` (no newline) | `d0023e67...` |
| **`echo -n0 "hello"`** | **`0hello`** — `-n0` is parsed as flag `-n` then arg `0` | **`ec094cf2...`** (wrong) |
| **`printf "hello"`** | **`hello`** (5 bytes) ✓ | **`2cf24dba...`** |

**Pitfall:** Typing `echo -n0 "hello"` (thinking “no newline” + “hello”) actually hashes **`0hello`**, so your generated hash never matches the app’s hash of `"hello"` and overwrite/login fails. Use **`printf "password"`** so the exact bytes are under your control.

```bash
# Correct: exact string, no newline
printf "hello" | sha256sum
# 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824  -

# For salted formats, use the tool’s expected input (e.g. pass then salt) or hashcat to generate.
```

---

## Hash Identification

```bash
# Identify hash type
hashcat --identify hash.txt

# Using hashid
hashid hash.txt

# Using hash-identifier
hash-identifier
```

---

## Common Hash Modes

| Mode | Hash Type | Example Use |
|------|-----------|-------------|
| 0 | MD5 | Web apps, databases |
| 10 | md5($pass.$salt) | Salted MD5 (pass first) |
| 20 | md5($salt.$pass) | Salted MD5 (salt first), CMS Made Simple |
| 100 | SHA1 | Web apps |
| 1400 | SHA256 | Modern apps, CrushFTP |
| 1700 | SHA512 | Modern apps, CrushFTP |
| 1800 | sha512crypt ($6$) | Linux /etc/shadow |
| 500 | md5crypt ($1$) | Older Linux |
| 1600 | Apache $apr1$ MD5 | .htpasswd files |
| 3200 | bcrypt ($2*$) | Modern web apps |
| 10900 | PBKDF2-HMAC-SHA256 | Flask/Werkzeug, Superset, Grafana, Mirth Connect 4.4.0+ |
| 1000 | NTLM | Windows SAM/NTDS |
| 5600 | NetNTLMv2 | Windows network auth |
| 13100 | Kerberos TGS-REP (etype 23) | Kerberoasting |
| 18200 | Kerberos AS-REP (etype 23) | AS-REP Roasting |
| 5300 | IKE-PSK MD5 | IPsec VPN |
| 5400 | IKE-PSK SHA1 | IPsec VPN |
| 2500 | WPA/WPA2 | WiFi |
| 22000 | WPA-PBKDF2-PMKID+EAPOL | WiFi (modern) |
| 13400 | KeePass 1/2 (.kdbx) | Password managers |

### Network Device Hashes (Cisco)

| Mode | Hash Type | Example |
|------|-----------|---------|
| 500 | Cisco-IOS Type 5 ($1$) | `enable secret 5 $1$salt$hash` |
| 5700 | Cisco-IOS Type 4 (SHA256) | `enable secret 4 hash` |
| 9200 | Cisco-IOS Type 8 (PBKDF2-SHA256) | `$8$salt$hash` |
| 9300 | Cisco-IOS Type 9 (scrypt) | `$9$salt$hash` |

**Cisco Type 5 (MD5) Example:**

```bash
# From router config: enable secret 5 $1$pdQG$o8nrSzsGXeaduXrjlvKc91
hashcat -a 0 -m 500 '$1$pdQG$o8nrSzsGXeaduXrjlvKc91' /usr/share/wordlists/rockyou.txt

# Output: $1$pdQG$o8nrSzsGXeaduXrjlvKc91:stealth1agent
```

**Mirth Connect 4.4.0+ (PBKDF2, mode 10900):** Stored hash is Base64; first 8 bytes = salt, rest = PBKDF2 output. Convert to `sha256:600000:SALT_B64:HASH_B64` (salt and hash Base64-encoded, strip trailing `=`). See [Mirth Connect](things-i-have-pwnd-before/mirth-connect.md) for Python conversion and DB extraction.

**Cisco Type 7 - NOT for hashcat!** Type 7 is reversible obfuscation, not encryption:

```bash
# Online: https://www.firewall.cx/cisco-technical-knowledgebase/cisco-routers/358-cisco-type7-password-crack.html

# Python
pip install cisco-type7
cisco-type7 decrypt "0242114B0E143F015F5D1E161713"
```

---

## Basic Usage

```bash
# Dictionary attack
hashcat -a 0 -m MODE hash.txt /usr/share/wordlists/rockyou.txt

# bcrypt (e.g. from CMS DB)
hashcat -a 0 -m 3200 admin.hash /usr/share/wordlists/rockyou.txt

# With rules
hashcat -a 0 -m MODE hash.txt wordlist.txt -r /usr/share/hashcat/rules/best64.rule

# Show cracked
hashcat -m MODE hash.txt --show
```

## Example

```
hashcat --identify jbercov.hash
  18200 | Kerberos 5, etype 23, AS-REP                        | Network Protocol

hashcat -a 0 -m 18200 jbercov.hash.hashcat /usr/share/seclists/rockyou.txt --force
```

## Example

* Hash `f806fc5a2a0d5ba2471600758452799c`

```
hashcat -a 0 -m 0 f806fc5a2a0d5ba2471600758452799c /usr/share/wordlists/rockyou.txt
hashcat (v6.1.1) starting...
f806fc5a2a0d5ba2471600758452799c:rockyou

Session..........: hashcat
Status...........: Cracked
Hash.Name........: MD5
Hash.Target......: f806fc5a2a0d5ba2471600758452799c
Time.Started.....: Mon Oct 11 08:20:50 2021 (0 secs)
Time.Estimated...: Mon Oct 11 08:20:50 2021 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   114.1 kH/s (0.02ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 40/40 (100.00%)
Rejected.........: 0/40 (0.00%)
Restore.Point....: 0/40 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: 123456 -> 123123

Started: Mon Oct 11 08:20:49 2021
Stopped: Mon Oct 11 08:20:52 2021
```

* \-a 0 sets the attack mode to a dictionary attack
* \-m 0 sets the hash mode for cracking MD5 hashes; for other types, run hashcat -h for a list of supported hashes.
* `f806fc5a2a0d5ba2471600758452799c` this option could be a single hash like our example or a file that contains a hash or multiple hashes.
* `/usr/share/wordlists/rockyou.txt` the wordlist/dictionary file for our attack
* We run hashcat with --show option to show the cracked value if the hash has been cracked:

```
hashcat -a 0 -m 0 F806FC5A2A0D5BA2471600758452799C /usr/share/wordlists/rockyou.txt --show
f806fc5a2a0d5ba2471600758452799c:rockyou
```

## Mask Character Sets

| Charset | Characters |
|---------|-----------|
| `?l` | `abcdefghijklmnopqrstuvwxyz` |
| `?u` | `ABCDEFGHIJKLMNOPQRSTUVWXYZ` |
| `?d` | `0123456789` |
| `?h` | `0123456789abcdef` |
| `?H` | `0123456789ABCDEF` |
| `?s` | `` !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ `` |
| `?a` | `?l?u?d?s` (all printable) |
| `?b` | `0x00 – 0xff` (all bytes) |

---

## Brute-Force / Mask Attack (-a 3)

```bash
# Brute force a 4 digit pin
hashcat -a 3 -m 0 hash.txt ?d?d?d?d

# Known prefix with unknown digits (e.g. password format: susan_nasus_<digits>)
hashcat -m 1400 -a 3 hash.txt 'susan_nasus_?d?d?d?d?d?d?d?d?d'
```

When the password length is unknown, run incrementally — start short and increase:

```bash
hashcat -m 1400 -a 3 hashes.txt 'prefix_?d'
hashcat -m 1400 -a 3 hashes.txt 'prefix_?d?d'
hashcat -m 1400 -a 3 hashes.txt 'prefix_?d?d?d'
hashcat -m 1400 -a 3 hashes.txt 'prefix_?d?d?d?d'
hashcat -m 1400 -a 3 hashes.txt 'prefix_?d?d?d?d?d'
hashcat -m 1400 -a 3 hashes.txt 'prefix_?d?d?d?d?d?d'
hashcat -m 1400 -a 3 hashes.txt 'prefix_?d?d?d?d?d?d?d'
hashcat -m 1400 -a 3 hashes.txt 'prefix_?d?d?d?d?d?d?d?d'
hashcat -m 1400 -a 3 hashes.txt 'prefix_?d?d?d?d?d?d?d?d?d'
```

Or use `--increment` to auto-increase length:

```bash
hashcat -m 1400 -a 3 hashes.txt 'prefix_?d?d?d?d?d?d?d?d?d' --increment --increment-min 1 --increment-max 9
```

---

## Hybrid Attack (-a 6 / -a 7)

Combine a wordlist with a mask. `-a 6` appends the mask to each word, `-a 7` prepends it.

```bash
# Wordlist + mask: each word from rockyou followed by 1 digit + 1 special char
hashcat -m 1400 -a 6 hashes.txt /usr/share/wordlists/rockyou.txt '?d?s'

# Mask + wordlist: 2 digits prepended to each word
hashcat -m 1400 -a 7 hashes.txt '?d?d' /usr/share/wordlists/rockyou.txt
```

---

## Generating Massive Wordlists with Rules

Combine rockyou with rule files to produce mutation-expanded lists:

```bash
hashcat --force --stdout /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule -r /usr/share/hashcat/rules/toggles1.rule > expanded.txt
```

**Reference:** [BlackHills Hashcat Cheatsheet](https://www.blackhillsinfosec.com/hashcat-cheatsheet/)

---

## Brute-Force 4-digit PIN Example

```
hashcat -a 3 -m 0 05A5CF06982BA7892ED2A6D38FE832D6 ?d?d?d?d
05a5cf06982ba7892ed2a6d38fe832d6:2021
```
