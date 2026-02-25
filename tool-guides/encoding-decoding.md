# Encoding & Decoding Quick Reference

## Base64

### Encode

```bash
echo 'https://www.hackthebox.eu/' | base64
# aHR0cHM6Ly93d3cuaGFja3RoZWJveC5ldS8K

# Encode a file
base64 file.txt > encoded.txt
cat file.txt | base64
```

### Decode

```bash
echo 'aHR0cHM6Ly93d3cuaGFja3RoZWJveC5ldS8K' | base64 -d
# https://www.hackthebox.eu/

# Decode a file
base64 -d encoded.txt > decoded.txt
```

### Spotting Base64

- Contains only: `A-Z`, `a-z`, `0-9`, `+`, `/`
- Padding: `=` or `==` at the end
- Length is multiple of 4

---

## Hex

### Encode

```bash
echo 'https://www.hackthebox.eu/' | xxd -p
# 68747470733a2f2f7777772e6861636b746865626f782e65752f0a

# Alternative (single line output)
echo -n 'hello' | xxd -p
```

### Decode

```bash
echo '68747470733a2f2f7777772e6861636b746865626f782e65752f0a' | xxd -p -r
# https://www.hackthebox.eu/

# From hex string to text
echo -n '48656c6c6f' | xxd -r -p
# Hello
```

### Spotting Hex

- Contains only: `0-9`, `a-f` (or `A-F`)
- Even number of characters

---

## ROT13

### Encode/Decode (Same Command)

```bash
echo 'https://www.hackthebox.eu/' | tr 'A-Za-z' 'N-ZA-Mn-za-m'
# uggcf://jjj.unpxgurobk.rh/

# Decode (apply again)
echo 'uggcf://jjj.unpxgurobk.rh/' | tr 'A-Za-z' 'N-ZA-Mn-za-m'
# https://www.hackthebox.eu/
```

### Online Tool

- https://rot13.com/

---

## URL Encoding

### Encode (Python)

```bash
python3 -c "import urllib.parse; print(urllib.parse.quote('Hello World!'))"
# Hello%20World%21
```

### Decode (Python)

```bash
python3 -c "import urllib.parse; print(urllib.parse.unquote('Hello%20World%21'))"
# Hello World!
```

### Common URL Encoded Characters

| Character | Encoded |
|-----------|---------|
| Space | `%20` or `+` |
| `!` | `%21` |
| `"` | `%22` |
| `#` | `%23` |
| `$` | `%24` |
| `%` | `%25` |
| `&` | `%26` |
| `'` | `%27` |
| `(` | `%28` |
| `)` | `%29` |
| `*` | `%2a` |
| `+` | `%2b` |
| `,` | `%2c` |
| `/` | `%2f` |
| `:` | `%3a` |
| `;` | `%3b` |
| `<` | `%3c` |
| `=` | `%3d` |
| `>` | `%3e` |
| `?` | `%3f` |
| `@` | `%40` |
| `[` | `%5b` |
| `\` | `%5c` |
| `]` | `%5d` |
| `^` | `%5e` |
| Newline | `%0a` |
| `{` | `%7b` |
| `}` | `%7d` |
| `|` | `%7c` |
| `~` | `%7e` |
| `` ` `` | `%60` |

### Online URL Encoder/Decoder

- [urlencoder.org](https://www.urlencoder.org/) — paste raw payloads and get the encoded version; useful when Burp's encoder is not handy

---

## Cipher Identification

### Online Tools

- [Cipher Identifier](https://www.boxentriq.com/code-breaking/cipher-identifier) - Auto-detect encoding type
- [CyberChef](https://gchq.github.io/CyberChef/) - Swiss army knife for encoding

---

## JavaScript Deobfuscation

### Beautify Minified JS

```bash
# Using js-beautify
pip install jsbeautifier
js-beautify script.js > script-beautified.js
```

### Online Tools

| Tool | URL | Use Case |
|------|-----|----------|
| Prettier | https://prettier.io/playground/ | Beautify/format code |
| Beautifier | https://beautifier.io/ | Beautify/format code |
| UnPacker | https://matthewfl.com/unPacker.html | Unpack `(p,a,c,k,e,d)` obfuscation |
| de4js | https://lelinhtinh.github.io/de4js/ | Multiple deobfuscation methods |
| Obfuscator.io | https://obfuscator.io/ | Obfuscate JS (for testing) |

### Recognizing Packer Obfuscation

Look for initial function signature:

```javascript
eval(function(p,a,c,k,e,d){...})
```

### Manual Deobfuscation Trick

Replace `eval` with `console.log` to print the deobfuscated code instead of executing it:

```javascript
// Change this:
eval(function(p,a,c,k,e,d){...})

// To this:
console.log(function(p,a,c,k,e,d){...})
```
