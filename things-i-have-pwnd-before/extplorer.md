# eXtplorer

eXtplorer is a PHP file manager often found under `/filemanager/`. If you already have a web shell, check the web root for it because its local user database can expose reusable credentials.

## Discovery

```bash
feroxbuster -u http://TARGET -x php,txt,html
```

Common paths:

```text
/filemanager/
/filemanager/index.php
/filemanager/config/.htusers.php
```

Version and install clues are often in:

```text
/filemanager/README.txt
/filemanager/CHANGELOG.txt
/filemanager/extplorer.xml
```

## Credential File

If you can read local files as the web server user, inspect:

```bash
cat /var/www/html/filemanager/config/.htusers.php
```

Example format:

```php
$GLOBALS["users"]=array(
    array('admin','21232f297a57a5a743894a0e4a801fc3','/var/www/html','http://localhost','1','','7',1),
    array('dora','$2a$08$HASH','/var/www/html','http://localhost','1','','0',1),
);
```

The first field is the username and the second field is the password hash.

## Cracking Hashes

Older/admin entries may be raw MD5:

```bash
hashcat -a 0 -m 0 admin.hash /usr/share/wordlists/rockyou.txt
# 21232f297a57a5a743894a0e4a801fc3:admin
```

User entries may be bcrypt:

```bash
hashcat --identify hashes.txt
hashcat -a 0 -m 3200 bcrypt.hash /usr/share/wordlists/rockyou.txt
```

Try cracked user passwords against local users, SSH, `su`, and any other exposed management service. eXtplorer usernames commonly line up with system users in lab environments.
