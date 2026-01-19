# Burp Suite

Web proxy for intercepting, modifying, and repeating HTTP requests.

**Install:** Download from [portswigger.net/burp](https://portswigger.net/burp/releases/) or run `java -jar burpsuite.jar`

---

## Quick Start

1. Start Burp Suite
2. `Proxy` tab > Click `Open Browser` (pre-configured Chromium)
3. Browse target website - requests appear in `Proxy > HTTP History`

---

## Proxy Setup

### Pre-Configured Browser

Fastest method - click `Open Browser` in `Proxy > Intercept` tab.

### Manual Firefox Setup

1. Install [FoxyProxy](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/)
2. Add proxy: `127.0.0.1:8080`
3. Install CA cert:
   - Browse to `http://burp` with proxy enabled
   - Click `CA Certificate` to download
   - Firefox: `about:preferences#privacy` > `View Certificates` > `Authorities` > `Import`
   - Check "Trust this CA to identify websites"

### Change Proxy Port

`Proxy > Proxy settings > Proxy listeners`

---

## Intercepting Requests

### Enable/Disable Intercept

`Proxy > Intercept` tab > Click `Intercept is on/off`

### Intercept Workflow

1. Enable intercept
2. Make request in browser
3. Request appears in Burp
4. Modify request as needed
5. Click `Forward` to send (or `Drop` to discard)

### Intercept Responses

`Proxy > Proxy settings > Response interception rules` > Enable `Intercept responses`

---

## Repeater

Send requests multiple times with modifications.

### Usage

1. Find request in `Proxy > HTTP History`
2. Right-click > `Send to Repeater` (or `Ctrl+R`)
3. Go to `Repeater` tab (`Ctrl+Shift+R`)
4. Modify request
5. Click `Send`
6. View response

### Tips

- Right-click > `Change Request Method` to toggle GET/POST
- Use `Ctrl+U` to URL-encode selected text

---

## Intruder (Fuzzer)

Automate attacks with wordlists.

### Setup

1. Send request to Intruder (`Ctrl+I`)
2. **Positions tab:** Select text, click `Add §` to mark injection points
3. **Payloads tab:** Load wordlist

### Attack Types

| Type | Description |
|------|-------------|
| Sniper | Single payload position at a time |
| Battering Ram | Same payload in all positions |
| Pitchfork | Different payload per position (parallel) |
| Cluster Bomb | All combinations of payloads |

### Payload Options

```
Payload Type:
- Simple List     → Load wordlist file
- Runtime file    → Stream from file (large wordlists)
- Numbers         → Sequential/random numbers
- Brute forcer    → Character set permutations
```

### Payload Processing

Add rules to modify payloads:
- `Skip if matches regex` - Filter payloads
- `Add prefix/suffix` - Append strings
- `Encode` - URL/Base64 encode

### Filter Results

`Settings > Grep - Match` - Flag responses containing specific strings (e.g., `200 OK`)

### Note

⚠️ **Free version limited to 1 request/second** - Use ZAP Fuzzer or ffuf for speed

---

## Match & Replace

Auto-modify requests/responses.

### Setup

`Proxy > Proxy settings > HTTP match and replace rules > Add`

### Common Uses

```
# Change User-Agent
Type: Request header
Match: ^User-Agent.*$
Replace: User-Agent: Custom Agent
Regex: True

# Enable disabled fields
Type: Response body
Match: type="number"
Replace: type="text"

# Remove length limits
Type: Response body
Match: maxlength="3"
Replace: maxlength="100"
```

---

## Decoder

Encode/decode data.

### Access

`Decoder` tab or `Burp Inspector` (in Repeater/Proxy)

### Supported Formats

- URL encoding
- Base64
- HTML entities
- Hex
- ASCII hex
- Gzip

### Quick Encode

In Repeater: Select text > Right-click > `Convert Selection > URL > URL-encode`

Or: Select text > `Ctrl+U`

---

## Scanner (Pro Only)

### Target Scope

1. `Target > Site map` - View discovered paths
2. Right-click target > `Add to scope`
3. `Target > Scope` - View/edit scope

### Crawl

Discover all pages/links:

1. `Dashboard > New Scan`
2. Select `Crawl`
3. Configure speed (Fastest/Normal)
4. Start scan

### Passive Scan

Analyze responses without sending new requests:
- Right-click request > `Do passive scan`
- Finds: Missing headers, DOM XSS, info leaks

### Active Scan

Full vulnerability scan:
- Right-click request > `Do active scan`
- Or: `Dashboard > New Scan > Crawl and Audit`

**Tests:** SQLi, XSS, Command Injection, Path Traversal, etc.

### Reports

`Target > Site map` > Right-click target > `Issue > Report issues for this host`

---

## Useful Extensions

Install from `Extender > BApp Store`

| Extension | Purpose |
|-----------|---------|
| Active Scan++ | Enhanced scanner |
| Autorize | Authorization testing |
| Logger++ | Advanced logging |
| JWT Editor | JWT manipulation |
| Param Miner | Hidden parameter discovery |
| Retire.js | JS vulnerability detection |
| Turbo Intruder | Fast fuzzing (Python) |
| Hackvertor | Advanced encoding |

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Send to Repeater | `Ctrl+R` |
| Send to Intruder | `Ctrl+I` |
| Go to Repeater | `Ctrl+Shift+R` |
| Forward request | `Ctrl+F` |
| URL encode selection | `Ctrl+U` |
| Toggle intercept | `Ctrl+T` |
| Search | `Ctrl+Shift+F` |

---

## Proxy CLI Tools

### With Proxychains

```bash
# Edit /etc/proxychains.conf
# Add: http 127.0.0.1 8080

proxychains -q curl http://target.com
proxychains -q sqlmap -u "http://target.com/?id=1"
```

### With cURL

```bash
curl -x http://127.0.0.1:8080 http://target.com
curl --proxy http://127.0.0.1:8080 -k https://target.com
```

### With Metasploit

```bash
msf6 > set PROXIES HTTP:127.0.0.1:8080
```

---

## Tips

- Use `Logger` tab to see all traffic (including from scanner)
- `Comparer` tab for diff'ing responses
- Right-click requests to `Copy as curl command`
- `Target > Site map` shows full application structure
- Enable `Unhide hidden form fields` in `Proxy > Proxy settings > Response modification rules`
