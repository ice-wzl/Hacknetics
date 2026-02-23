# Engagement types (black / grey / white box)

| Type | Description |
|------|-------------|
| **Black-box** | Little or no prior knowledge. Tester performs full recon (e.g. external test with only org name, or internal with no IP list). Most realistic to a real attacker; can miss issues that need internal/design context. |
| **Grey-box** | Some information provided up front: in-scope IPs/ranges, low-priv credentials, app/network diagrams. Simulates insider or post-breach; less time on recon, more on misconfigs and exploitation. |
| **White-box** | Full access to design, source, configs, credentials. Aim is maximum finding coverage; not representative of attacker perspective. |

Choose scope and rules of engagement (e.g. no DoS, no phishing) per SOW and get them in writing.
