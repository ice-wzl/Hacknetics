# Engagement types (black / grey / white box)

| Type | Description |
|------|-------------|
| **Black-box** | Little or no prior knowledge. Tester performs full recon (e.g. external test with only org name, or internal with no IP list). Most realistic to a real attacker; can miss issues that need internal/design context. |
| **Grey-box** | Some information provided up front: in-scope IPs/ranges, low-priv credentials, app/network diagrams. Simulates insider or post-breach; less time on recon, more on misconfigs and exploitation. |
| **White-box** | Full access to design, source, configs, credentials. Aim is maximum finding coverage; not representative of attacker perspective. |

Choose scope and rules of engagement (e.g. no DoS, no phishing) per SOW and get them in writing.

---

## Security Assessment Types

| Assessment | Purpose | Key Traits |
|---|---|---|
| **Vulnerability Assessment** | Identify and categorize known weaknesses via scanning + validation. Little to no manual exploitation. | Checklist-driven, scanner-heavy, results in remediation plan. Appropriate for all orgs. |
| **Penetration Test** | Simulated attack to determine if/how a network can be penetrated. Manual + automated. | Requires signed legal scope, medium-to-high security maturity orgs. Goes beyond scanning into exploitation, lateral movement, post-exploitation. |
| **Security Audit** | Externally mandated compliance check (government, industry). | Not voluntary — driven by regulation (PCI DSS, HIPAA, etc.). |
| **Bug Bounty** | Public program inviting researchers to find vulns for payment. | Large orgs with high maturity; need a dedicated triage team. Usually no automated scanning allowed. |
| **Red Team** | Evasive black-box attack simulation by experienced operators. Goal-oriented (e.g. reach a critical DB). | Only reports the chain that reached the objective, not every finding. |
| **Purple Team** | Red + Blue working together. Blue observes/provides input during red team campaigns. | Collaborative; improves detection and response in real-time. |

Pentester specializations: **Application** (web apps, APIs, mobile, thick-client, source code review), **Network/Infrastructure** (networking devices, servers, AD, scanners like Nessus alongside manual testing), **Physical** (door bypass, tailgating, vent crawling), **Social Engineering** (phishing, vishing, pretexting).

---

## Vulnerability Assessment vs. Penetration Test

- A **VA** goes through a checklist: _Do we meet this standard? Do we have this config?_ The assessor runs a vuln scan, validates critical/high/medium findings to rule out false positives, but does **not** pursue priv esc, lateral movement, or post-exploitation.
- A **pentest** simulates a real attack. It includes manual techniques beyond what scanners find. Only appropriate after some VAs have been conducted and fixes applied.
- They complement each other. Orgs should run VAs continuously and pentests annually or semi-annually.

---

## Compliance Standards

| Standard | Scope | Notes |
|---|---|---|
| **[PCI DSS](https://www.pcisecuritystandards.org/pci_security/)** | Orgs that store/process/transmit cardholder data (banks, online stores). | Requires internal + external scanning. Cardholder Data Environment (CDE) must be segmented from the regular network. |
| **[HIPAA](https://www.hhs.gov/programs/hipaa/index.html)** | Healthcare — protects patient data. | Risk assessment + vulnerability identification required for accreditation. |
| **[FISMA](https://www.cisa.gov/federal-information-security-modernization-act)** | U.S. government operations and information. | Requires documented vulnerability management program. |
| **[ISO 27001](https://www.iso.org/isoiec-27001-information-security.html)** | International information security management. | Requires quarterly internal + external scans. |

---

## Pentesting Standards

| Standard | Focus |
|---|---|
| **[PTES](http://www.pentest-standard.org/index.php/Main_Page)** | Pre-engagement → Intel Gathering → Threat Modeling → Vuln Analysis → Exploitation → Post-Exploitation → Reporting |
| **[OSSTMM](https://www.isecom.org/OSSTMM.3.pdf)** | 5 channels: Human Security, Physical Security, Wireless, Telecommunications, Data Networks |
| **[NIST Pentest Framework](https://www.nist.gov/cyberframework)** | Planning → Discovery → Attack → Reporting |
| **[OWASP](https://owasp.org)** | [WSTG](https://owasp.org/www-project-web-security-testing-guide/) (web), [MSTG](https://owasp.org/www-project-mobile-security-testing-guide/) (mobile), [FSTM](https://github.com/scriptingxss/owasp-fstm) (firmware) |

---

## Key Risk Terminology

- **Vulnerability** — a weakness (code, config, process) that could be exploited. Registered via [CVE](https://cve.mitre.org/) and scored with [CVSS](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator).
- **Threat** — a process or actor that could exploit a vulnerability.
- **Exploit** — code or technique that takes advantage of a vulnerability. Sources: [Exploit-DB](https://exploit-db.com), [Rapid7 DB](https://www.rapid7.com/db/), GitHub.
- **Risk** — the possibility of harm from a threat exploiting a vulnerability. Measured by **likelihood × impact**.

| | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| **High Likelihood** | Medium (3) | High (4) | Critical (5) |
| **Medium Likelihood** | Low (2) | Medium (3) | High (4) |
| **Low Likelihood** | Lowest (1) | Low (2) | Medium (3) |

---

## CVSS Scoring

[CVSS v3.1 Calculator](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator) — scores range 0–10 based on three metric groups:

**Base Metrics** (characteristics of the vuln itself):
- *Exploitability*: Attack Vector, Attack Complexity, Privileges Required, User Interaction
- *Impact*: Confidentiality, Integrity, Availability (CIA triad)

**Temporal Metrics** (change over time):
- *Exploit Code Maturity*: Unproven → PoC → Functional → High
- *Remediation Level*: Official Fix → Temporary Fix → Workaround → Unavailable
- *Report Confidence*: Unknown → Reasonable → Confirmed

**Environmental Metrics** (org-specific context):
- Modified Base Metrics adjusted by the org's CIA requirements (Not Defined / Low / Medium / High).

[Microsoft DREAD](https://en.wikipedia.org/wiki/DREAD_(risk_assessment_model)) is a complementary 10-point scale based on: **D**amage Potential, **R**eproducibility, **E**xploitability, **A**ffected Users, **D**iscoverability.

---

## CVE Lifecycle

[OVAL](https://oval.mitre.org/) (Open Vulnerability Assessment Language) provides XML-based definitions for detecting vulns without exploitation. Four definition classes: Vulnerability, Compliance, Inventory, Patch. ID format: `oval:org.mitre.oval:obj:1116`.

**CVE ID assignment stages:**

1. Confirm the issue is a vulnerability (code exploitable, impacts CIA) and no existing CVE covers it.
2. Contact the affected vendor (good-faith responsible disclosure).
3. If vendor is a CNA, they assign the CVE. Otherwise use a third-party CNA.
4. Fall back to the [CVE Web Form](https://cveform.mitre.org/).
5. Receive confirmation email; provide additional info if requested.
6. CVE ID assigned (not yet public).
7. Public disclosure once all parties are aware.
8. Announce — ensure each CVE maps to a distinct vulnerability.
9. Provide details for the official [NVD](https://nvd.nist.gov/) listing.

**Responsible disclosure** means working with the vendor to ensure a patch is available before public announcement, preventing zero-day exploitation.
