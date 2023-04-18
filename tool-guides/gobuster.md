# gobuster

#### gobuster

* gobuster tries to find valid directories from a wordlist of possible directories. gobuster can also be used to valid subdomains using the same method.

### Dir brute force mode&#x20;

```
gobuster dir -u http://10.10.10.10 -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt 
```

* If for example bad directories are `302` over to the 404 page&#x20;
* You will need to add 302 to the bad status codes list, only 404 is there by default&#x20;

```
gobuster dir -u http://10.10.10.10 -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt -b 302,404 
```

### Vhost enumeration&#x20;

```
gobuster vhost -u http://mailbox.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top-11000.txt
```
