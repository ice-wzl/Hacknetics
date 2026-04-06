# LLMNR/NBT-NS Poisoning

## Overview
- LLMNR (Link-Local Multicast Name Resolution) and NBT-NS (NetBIOS Name Service) are alternate name resolution methods when DNS fails
- LLMNR uses port 5355/UDP, NBT-NS uses port 137/UDP
- ANY host on the network can reply to these requests - this is where we poison
- We spoof an authoritative name resolution source to capture NTLMv1/v2 hashes
- Combined with lack of SMB signing, can lead to SMB Relay attacks

## Attack Flow
1. Host attempts to connect to \\print01.inlanefreight.local but mistypes it
2. DNS server responds - host unknown
3. Host broadcasts to the local network asking if anyone knows the location
4. Attacker (running Responder) responds claiming to be the requested host
5. Host sends authentication request with username and NTLMv2 password hash
6. Hash can be cracked offline or used in SMB Relay

## Responder (Linux)

### Passive Analysis Mode
```bash
sudo responder -I ens224 -A
```

### Active Poisoning (Default)
```bash
sudo responder -I ens224
```

### Common Flags
- `-A` - Analyze mode (passive, no poisoning)
- `-wf` - Start WPAD rogue proxy + fingerprint remote OS
- `-v` - Verbose output
- `-F` - Force NTLM auth on WPAD (may cause login prompt)
- `-P` - Force proxy auth (use sparingly)

### Responder Logs
- Hashes saved to `/usr/share/responder/logs/`
- Format: `(MODULE_NAME)-(HASH_TYPE)-(CLIENT_IP).txt`
- Also stored in SQLite database (configurable in `Responder.conf`)

### Required Ports
```
UDP 137, UDP 138, UDP 53, UDP/TCP 389, TCP 1433, UDP 1434, TCP 80, TCP 135, TCP 139, TCP 445, TCP 21, TCP 3141, TCP 25, TCP 110, TCP 587, TCP 3128, Multicast UDP 5355 and 5353
```

### Protocols Supported
- LLMNR, DNS, MDNS, NBNS, DHCP, ICMP, HTTP, HTTPS, SMB, LDAP, WebDAV, Proxy Auth, MSSQL, DCE-RPC, FTP, POP3, IMAP, SMTP auth

## Inveigh (Windows)

### PowerShell Version
```powershell
Import-Module .\Inveigh.ps1
Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y
```

### C# Version (InveighZero)
```powershell
.\Inveigh.exe
```
- Press ESC to enter interactive console
- Type `HELP` for available commands:
  - `GET NTLMV2UNIQUE` - View unique captured NTLMv2 hashes
  - `GET NTLMV2USERNAMES` - View usernames and source IPs
  - `GET CLEARTEXT` - View captured cleartext credentials
  - `STOP` - Stop Inveigh

## Cracking Captured Hashes

### NTLMv2 with Hashcat
```bash
hashcat -m 5600 forend_ntlmv2 /usr/share/wordlists/rockyou.txt
```
- NetNTLMv2 hashes CANNOT be used for pass-the-hash - must be cracked offline
- NTLMv1 hashes use mode 5500

## Remediation
- Disable LLMNR via Group Policy: Computer Configuration > Administrative Templates > Network > DNS Client > "Turn OFF Multicast Name Resolution"
- Disable NBT-NS: Network adapter properties > IPv4 > Advanced > WINS > "Disable NetBIOS over TCP/IP"
- NBT-NS can be disabled via GPO startup script:
```powershell
$regkey = "HKLM:SYSTEM\CurrentControlSet\services\NetBT\Parameters\Interfaces"
Get-ChildItem $regkey | foreach { Set-ItemProperty -Path "$regkey\$($_.pschildname)" -Name NetbiosOptions -Value 2 -Verbose}
```
- Enable SMB Signing to prevent NTLM relay
- Network segmentation
- Monitor ports UDP 5355 and 137
- Monitor event IDs 4697 and 7045
