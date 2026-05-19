# Afrog

Afrog can run vulnerability checks against specific ports and surface exploitable paths from detected services.

## Scan Specific Ports

Use `-p` to limit scanning to ports already found during service enumeration:

```bash
afrog -t TARGET -ps -p 22,53,80,8000,4505,4506 -c 15 -rl 100
```

Useful SaltStack findings can look like:

```text
CVE-2020-16846 CRITICAL http://TARGET:8000/run
CVE-2021-25282 CRITICAL http://TARGET:8000/run
```

## Resume a Scan

If Afrog stops mid-run, resume with the generated `.afg` state file:

```bash
afrog -t TARGET -ps -p 22,53,80,8000,4505,4506 -c 15 -rl 100 -resume afrog-resume-TARGET-DATE.afg
```
