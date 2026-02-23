# Assessment organization

## Folder structure

Use a consistent folder layout per client/engagement so scans, evidence, and scope stay in one place.

```
Projects/
└── ClientName
    ├── EPT
    │   ├── evidence
    │   │   ├── credentials
    │   │   ├── data
    │   │   └── screenshots
    │   ├── logs
    │   ├── scans
    │   ├── scope
    │   └── tools
    └── IPT
        ├── evidence
        │   ├── credentials
        │   ├── data
        │   └── screenshots
        ├── logs
        ├── scans
        ├── scope
        └── tools
```

- **EPT** = External Penetration Test, **IPT** = Internal Penetration Test (or name per SOW).
- **scope** — IPs/ranges, hostnames, out-of-scope; feed into scanning tools.
- **scans** — Nmap, other scanner output.
- **evidence** — credentials, exfil samples, screenshots.
- **logs** — tool output, notes.
- **tools** — copies of scripts/exploits used for this engagement.

Use a fresh VM (or clean project dir) per assessment to avoid mixing client data and scope.
