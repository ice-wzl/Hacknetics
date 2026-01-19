# Hashcat

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
| 100 | SHA1 | Web apps |
| 1400 | SHA256 | Modern apps, CrushFTP |
| 1700 | SHA512 | Modern apps, CrushFTP |
| 1800 | sha512crypt ($6$) | Linux /etc/shadow |
| 500 | md5crypt ($1$) | Older Linux |
| 3200 | bcrypt ($2*$) | Modern web apps |
| 10900 | PBKDF2-HMAC-SHA256 | Flask/Werkzeug, Superset |
| 1000 | NTLM | Windows SAM/NTDS |
| 5600 | NetNTLMv2 | Windows network auth |
| 13100 | Kerberos TGS-REP (etype 23) | Kerberoasting |
| 18200 | Kerberos AS-REP (etype 23) | AS-REP Roasting |
| 5300 | IKE-PSK MD5 | IPsec VPN |
| 5400 | IKE-PSK SHA1 | IPsec VPN |
| 2500 | WPA/WPA2 | WiFi |
| 22000 | WPA-PBKDF2-PMKID+EAPOL | WiFi (modern) |
| 13400 | KeePass 1/2 (.kdbx) | Password managers |

---

## Basic Usage

```bash
# Dictionary attack
hashcat -a 0 -m MODE hash.txt /usr/share/wordlists/rockyou.txt

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

## Brute-Force attack

* Brute force a 4 digit pin

```
hashcat -a 3 ?d?d?d?d --stdout
1234
0234
2234
3234
9234
4234
5234
8234
7234
6234
..
..
```

* \-a 3 sets the attacking mode as a brute-force attack
* ?d?d?d?d the ?d tells hashcat to use a digit. In our case, ?d?d?d?d for four digits starting with 0000 and ending at 9999
* \--stdout print the result to the terminal

## Example of 4 digit pin hash

```
hashcat -a 3 -m 0 05A5CF06982BA7892ED2A6D38FE832D6 ?d?d?d?d
05a5cf06982ba7892ed2a6d38fe832d6:2021

Session..........: hashcat
Status...........: Cracked
Hash.Name........: MD5
Hash.Target......: 05a5cf06982ba7892ed2a6d38fe832d6
Time.Started.....: Mon Oct 11 10:54:06 2021 (0 secs)
Time.Estimated...: Mon Oct 11 10:54:06 2021 (0 secs)
Guess.Mask.......: ?d?d?d?d [4]
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........: 16253.6 kH/s (0.10ms) @ Accel:1024 Loops:10 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 10000/10000 (100.00%)
Rejected.........: 0/10000 (0.00%)
Restore.Point....: 0/1000 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-10 Iteration:0-10
Candidates.#1....: 1234 -> 6764

Started: Mon Oct 11 10:54:05 2021
Stopped: Mon Oct 11 10:54:08 2021
```
