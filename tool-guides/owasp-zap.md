# OWASP ZAP

Free, open-source web proxy and scanner. No throttling on fuzzer/scanner.

**Install:** Download from [zaproxy.org](https://www.zaproxy.org/download/) or run `java -jar zap.jar`

---

## Quick Start

1. Start ZAP (`zaproxy` command)
2. Click Firefox icon in toolbar (pre-configured browser)
3. Browse target - requests appear in `History` tab

---

## Proxy Setup

### Pre-Configured Browser

Click Firefox icon at end of top toolbar - auto-proxied through ZAP.

### Manual Firefox Setup

1. Install [FoxyProxy](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/)
2. Add proxy: `127.0.0.1:8080`
3. Export CA cert: `Tools > Options > Network > Server Certificates > Save`
4. Import in Firefox: `about:preferences#privacy` > `View Certificates` > `Authorities` > `Import`

### Change Proxy Port

`Tools > Options > Network > Local Servers/Proxies`

---

## Intercepting Requests

### Enable/Disable Intercept

- Click green circle button in toolbar (green = pass through, red = intercept)
- Or press `Ctrl+B`

### HUD Mode

ZAP's in-browser interface:
- Enable: Click HUD button (end of toolbar)
- Intercept: Click break button (left pane, second from top)
- `Step` = Forward and intercept next
- `Continue` = Forward and stop intercepting

### HUD Features

| Button | Function |
|--------|----------|
| Light bulb | Show/enable hidden fields |
| Comments | Show HTML comments |
| Spider | Start spider scan |
| Active Scan | Start vulnerability scan |

---

## Request Editor (Repeater)

Resend and modify requests.

### Usage

1. Find request in `History` tab
2. Right-click > `Open/Resend with Request Editor`
3. Modify request
4. Click `Send`

### From HUD

Click request in bottom History pane:
- `Replay in Console` - View response in HUD
- `Replay in Browser` - Render in browser

---

## Fuzzer

No speed throttling (unlike Burp free).

### Setup

1. Find request in History
2. Right-click > `Attack > Fuzz`
3. Select text to fuzz > Click `Add`
4. Choose payload type

### Payload Types

| Type | Description |
|------|-------------|
| File | Load custom wordlist |
| File Fuzzers | Built-in wordlists |
| Numberzz | Sequential numbers |
| Strings | Manual list |
| Regex | Pattern-based |

### Built-in Wordlists

Select `File Fuzzers` > Choose from:
- `dirbuster` - Directory lists
- `fuzzdb` - Attack payloads (install from Marketplace)

### Processors

Modify payloads before sending:
- URL Encode/Decode
- Base64 Encode/Decode
- MD5/SHA Hash
- Prefix/Postfix String

### Options

- `Concurrent Scanning Threads` - Set to 20+ for speed
- `Depth First` vs `Breadth First` strategy

### Filter Results

Sort by `Code` (HTTP status) or `Size Resp. Body`

---

## Replacer (Match & Replace)

Auto-modify requests/responses.

### Setup

`Ctrl+R` or `Tools > Replacer > Add`

### Options

| Field | Description |
|-------|-------------|
| Match Type | Request Header, Response Body, etc. |
| Match String | Text to find |
| Replacement String | Text to replace with |
| Initiators | Where to apply (all, specific tools) |

### Example - Custom User-Agent

```
Match Type: Request Header (will add if not present)
Match String: User-Agent
Replacement String: HackTheBox Agent 1.0
```

---

## Spider (Crawler)

Build site map by following links.

### Start Spider

- Right-click request in History > `Attack > Spider`
- Or HUD: Click Spider button (right pane)

### Ajax Spider

For JavaScript-heavy sites:
- HUD: Third button on right pane
- Discovers AJAX-loaded content

### View Results

`Sites` tab in main ZAP UI or HUD Sites Tree button

---

## Scanner

### Passive Scanner

Runs automatically on all proxied traffic.
- Check `Alerts` tab for findings
- No additional requests sent

### Active Scanner

Full vulnerability testing:
- Right-click target in Sites tree > `Attack > Active Scan`
- Or HUD: Click Active Scan button

**Tests:** SQLi, XSS, Command Injection, Path Traversal, CSRF, etc.

### View Alerts

- Main UI: `Alerts` tab
- HUD: Alert buttons (left/right panes)
- Click alert for details and PoC

### Alert Severity

| Level | Color | Examples |
|-------|-------|----------|
| High | Red | SQLi, RCE, Command Injection |
| Medium | Orange | XSS, CSRF, Missing security headers |
| Low | Yellow | Cookie flags, Information disclosure |
| Info | Blue | Interesting findings |

---

## Reporting

`Report > Generate HTML Report`

Other formats: XML, Markdown, JSON

---

## Marketplace Extensions

`Tools > Manage Add-ons > Marketplace`

### Recommended Add-ons

| Add-on | Purpose |
|--------|---------|
| FuzzDB Files | Attack wordlists |
| FuzzDB Offensive | More attack payloads |
| Wappalyzer | Technology fingerprinting |
| Retire.js | JS vulnerability detection |
| Access Control Testing | Authorization testing |
| JWT Support | JWT manipulation |

### Install Add-ons

1. `Manage Add-ons` > `Marketplace` tab
2. Find add-on
3. Click `Install`

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Toggle intercept | `Ctrl+B` |
| Open Replacer | `Ctrl+R` |
| Encoder/Decoder | `Ctrl+E` |
| Force browse | `Ctrl+L` |
| Active scan | Right-click > Attack |

---

## Encoder/Decoder/Hash

`Ctrl+E` or `Tools > Encode/Decode/Hash`

### Supported

- Base64
- URL
- ASCII Hex
- HTML Entity
- JavaScript
- MD5/SHA hashes

### Auto-Decode

Paste text in `Decode` tab - auto-detects encoding

---

## Proxy CLI Tools

### With Proxychains

```bash
# Edit /etc/proxychains.conf
# Add: http 127.0.0.1 8080

proxychains -q curl http://target.com
proxychains -q nmap -sT target.com
```

### With cURL

```bash
curl -x http://127.0.0.1:8080 http://target.com
```

---

## API / Automation

ZAP has a REST API for automation:

```bash
# Check API status
curl "http://localhost:8080/JSON/core/view/version/"

# Start spider
curl "http://localhost:8080/JSON/spider/action/scan/?url=http://target.com"

# Get alerts
curl "http://localhost:8080/JSON/core/view/alerts/"
```

### Command Line

```bash
# Headless scan
zap.sh -cmd -quickurl http://target.com -quickout report.html

# Daemon mode (API only)
zap.sh -daemon -port 8080
```

---

## Tips

- HUD tutorial: Click config button (bottom right) > "Take the HUD tutorial"
- Dark theme: `Tools > Options > Display > Look and Feel: Flat Dark`
- Ajax Spider catches dynamically loaded content
- Use Scope to limit scans: Right-click > `Include in Context`
- Export requests as cURL from History
