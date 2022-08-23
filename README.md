---
description: Collection of tips and tricks from myself and others!
---

# OSCP-Prep
# Git-Book of this Repo:
- https://taubl-jack.gitbook.io/oscp-prep/
## Path

### Start with recon-enumeration folder

* Start the scans: What is open?
* Use `autorecon 10.10.10.10 -v`
* Once completed, rescan all ports with service detection `nmap -sS -sV -sC 10.10.10.10 | tee nmap_output.txt`
* Consider running some targeted scripts against services running.

```
nmap --script "http*" 10.10.10.10 -p 8080 -vv | tee nmap_http_scripts.txt
```

* Identify the Ports and Services running.

### Web Server Running?

* Go To: `/web/web-servers.md`
* Find out CMS type and version --> check `exploitdb`
* Look for usernames
* Run `nikto`, `gobuster` --> try and map out the website
* `robots.txt` file?
* Default Credentials

```
admin:admin
administrator:administrator
admin:administrator
admin:password
administrator:password
admin admin123
admin root123
admin password1
admin administrator1
admin changeme1
admin password123
admin qwerty123
admin administrator123
admin changeme123
```

#### Upload Vulnerability PHP web shells

* The best one for Linux and Windows
* `/shells/web-shells/php-reverse-shell/src/php_reverse_shell.php`

### FTP Running

* Try `anonymous` login method
* If you can get a username from another port try `hydra`
* Make sure to connect to it as the `root` user from your local box
* Remember the difference between Active and Passive mode

### SSH/Telnet Running port 22, 23

* Be on the look out for LFI on a web server --> Private keys
* Think about Hydra if you can find a username

### Email Ports 25, 110, 143?

* `/recon-enumeration/recon-enumeration.md`

### NFS port 2049

* `/recon-enumeration/recon-enumeration.md`
* Check for shares that are accessible

### NetBios or Microsoft-ds Running ports 137, 138, 139, 445

* `/recon-enumeration/recon-enumeration.md` --> SMB Enumeration section
* Use `smbmap`, `nmap --script`, `enum4linux`, `smbclient`, `rpcclient`
* Check all enum4linux output especially toward the bottom for potential usernames
* Can be brute forced with `medusa`, and `nmap --script "smb-brute"`

### Redis port 6379

* `/recon-enumeration/recon-enumeration.md`
* Redis Section

### Rsync port 873

* `/recon-enumeration/recon-enumeration.md`
* Rsync Section

## On a Windows Box

* `/windows-priv-esc/win-priv-esc.md`
* Set up secondary Shell with `msfvenom` and `multi/handler`
* Check for hidden files as well
* Can you enable RDP and use `xfreerdp` to mount your kali share to the target?

### On a Linux Box

* `/lin-priv-esc/lin-priv-esc.md`
* Set up secondary Shell with `msfvenom` and `multi/handler`
* Always stabilize your shells!
* Get `lse.sh` and `linpeas.sh` on the box and in `/dev/shm`
* `/lin-priv-esc/priv-esc-scripts/`
