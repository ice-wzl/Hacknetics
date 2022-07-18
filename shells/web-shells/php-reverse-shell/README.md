# PHP Reverse Shell

Just a little refresh on the popular PHP reverse shell script [pentestmonkey/php-reverse-shell](https://github.com/pentestmonkey/php-reverse-shell). Credits to the original author!

Works on Linux OS and macOS with `/bin/sh` and Windows OS with `cmd.exe`. Script will automatically detect an underlying OS.

Works with both `ncat` and `multi/handler`.

Tested on XAMPP for Linux v7.3.19 (64-bit) with PHP v7.3.19 on Kali Linux v2020.2 (64-bit).

Tested on XAMPP for OS X v7.4.10 (64-bit) with PHP v7.4.10 on macOS Catalina v10.15.6 (64-bit).

Tested on XAMPP for Windows v7.4.3 (64-bit) with PHP v7.4.3 on Windows 10 Enterprise OS (64-bit).

In addition, everything was tested on Docker images [nouphet/docker-php4](https://hub.docker.com/r/nouphet/docker-php4) with PHP v4.4.0 and [steeze/php52-nginx](https://hub.docker.com/r/steeze/php52-nginx) with PHP v5.2.17.

Made for educational purposes. I hope it will help!

**Process pipes on Windows OS do not support asynchronous operations so `stream_set_blocking()`, `stream_select()`, and `feof()` will not work properly, but I found a workaround.**

## How to Run

[/src/php\_reverse\_shell.php](https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/php\_reverse\_shell.php) requires PHP v5.0.0 or greater, mainly because `proc_get_status()` is being used.

[/src/php\_reverse\_shell\_older.php](https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/php\_reverse\_shell\_older.php) requires PHP v4.3.0 or greater.

**Change the IP address and port number inside the script as necessary.**

Copy [/src/php\_reverse\_shell.php](https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/php\_reverse\_shell.php) to your server's web root directory (e.g. to /opt/lampp/htdocs/ on XAMPP) or upload it to your target's web server.

Navigate to the file with your preferred web browser.

***

Check the [simple PHP web shell](https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/simple\_php\_web\_shell\_post.php) based on HTTP POST request.

Check the [simple PHP web shell](https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/simple\_php\_web\_shell\_get.php) based on HTTP GET request. You must [URL encode](https://www.urlencoder.org) your commands.

Check the [simple PHP web shell v2](https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/simple\_php\_web\_shell\_get\_v2.php) based on HTTP GET request. You must [URL encode](https://www.urlencoder.org) your commands.

Find out more about PHP obfuscation techniques for older versions of PHP at [lcatro/PHP-WebShell-Bypass-WAF](https://github.com/lcatro/PHP-WebShell-Bypass-WAF). Credits to the author!

***

Check the minified scripts in [/src/minified/](https://github.com/ivan-sincek/php-reverse-shell/tree/master/src/minified) directory.

## Set Up a Listener

To set up a listener, open your preferred console on Kali Linux and run one of the examples below.

Set up an `ncat` listener:

```
ncat -nvlp 9000
```

Set up a `multi/handler` module:

```
msfconsole -q

use exploit/multi/handler

set PAYLOAD windows/shell_reverse_tcp

set LHOST 192.168.8.185

set LPORT 9000

exploit
```
