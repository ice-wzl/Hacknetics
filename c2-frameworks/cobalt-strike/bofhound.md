# BOFHound

BOFHound parses Cobalt Strike logs to generate BloodHound-compatible data without running SharpHound on target.

---

## Data Collection (Beacon)

Run these LDAP queries from Beacon to collect the necessary data:

```
# Collect domains, OUs, GPOs with security descriptors
ldapsearch (|(objectClass=domain)(objectClass=organizationalUnit)(objectClass=groupPolicyContainer)) --attributes *,ntsecuritydescriptor

# Collect users, computers, groups with security descriptors
ldapsearch (|(samAccountType=805306368)(samAccountType=805306369)(samAccountType=268435456)) --attributes *,ntsecuritydescriptor
```

---

## Processing Logs

```bash
# From Ubuntu/WSL - copy CS logs
cd /mnt/c/Users/Attacker/Desktop
scp -r attacker@TEAMSERVER:/opt/cobaltstrike/logs .

# Run BOFHound
bofhound -i logs
```

Output can be imported into BloodHound.

---

## Restricted Groups - Get Local Admins

BloodHound may miss local admin relationships defined via GPO Restricted Groups. Extract manually:

### Download GptTmpl.inf

```
# Find GPO path via BloodHound or ldapsearch
ls \\inlanefreight.local\SysVol\inlanefreight.local\Policies\{GPO-GUID}\Machine\Microsoft\Windows NT\SecEdit\

# Download the file
download \\inlanefreight.local\SysVol\inlanefreight.local\Policies\{GPO-GUID}\Machine\Microsoft\Windows NT\SecEdit\GptTmpl.inf
```

### Add Custom Edges in BloodHound

After identifying the group SID from GptTmpl.inf, add AdminTo edges:

```cypher
# Add AdminTo relationship for a group to computers
MATCH (x:Computer{objectid:'S-1-5-21-DOMAIN-SID-COMPUTER-RID'})
MATCH (y:Group{objectid:'S-1-5-21-DOMAIN-SID-GROUP-RID'})
MERGE (y)-[:AdminTo]->(x)
```

---

## WMI Filters

**Important:** BloodHound does NOT show WMI Filters. GPOs may appear to apply to computers but are actually filtered out.

### Enumerate WMI Filters on GPOs

```
# Find GPOs with WMI filters
ldapsearch (objectClass=groupPolicyContainer) --attributes displayname,gPCWQLFilter

# Example output:
# displayName: AppLocker
# gPCWQLFilter: [inlanefreight.local;{E91C83FB-ADBF-49D5-9E93-0AD41E05F411};0]
```

### Get Filter Details

```
# Query the WMI filter container
ldapsearch (objectClass=msWMI-Som) --attributes name,msWMI-Name,msWMI-Parm2 --dn "CN=SOM,CN=WMIPolicy,CN=System,DC=inlanefreight,DC=local"

# Example output:
# name: {E91C83FB-ADBF-49D5-9E93-0AD41E05F411}
# msWMI-Name: Windows 10+
# msWMI-Parm2: 1;3;10;61;WQL;root\CIMv2;SELECT * from Win32_OperatingSystem WHERE Version like "10.%";
```

This filter means the GPO only applies to Windows 10+ systems - older versions are excluded even if in the target OU.

---

## Key Takeaways

- BOFHound collects BloodHound data via Beacon without SharpHound
- Restricted Groups in GPOs can grant local admin - manually add edges
- WMI Filters can exclude computers from GPO application - BloodHound won't show this
