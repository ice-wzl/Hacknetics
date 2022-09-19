# Pen Testing Email

## SMTP Port 25 default

### SMTP User Enum

```
smtp-user-enum -M VRFY -U /usr/share/wordlists/dirb/common.txt -t [target ip]
```

* `-M` -> Sets the mode, the options are: EXPN, VRFY, RCPT (default VRFY)
* `-u` -> Check if a remote exists on a system
* `-U` -> File of usernames to check via smtp service
* `-t` -> Server host running the smtp service
* Examples:

```
smtp-user-enum -M VRFY -U users.txt -t 10.0.0.1
smtp-user-enum -M EXPN -u admin1 -t 10.0.0.1
smtp-user-enum -M RCPT -U users.txt -T mail-server-ips.txt
smtp-user-enum -M EXPN -D example.com -U users.txt -t 10.0.0.1
```

## POP3 Port 110 default

* Connect to the targets pop3 port

```
telnet 10.10.10.10 110
user <username>
pass <password>
list #see emails 
retr 1 #retrieve email 1
retr 2 #retrive email 2 
```

* ![alt text](https://i2.wp.com/2.bp.blogspot.com/-4rztPGl7PRs/W\_L6dz7yPTI/AAAAAAAAbQ8/oQGQ3S6S3CMLVcKt3clCF7QMSFRC16tIgCEwYBhgL/s1600/8.png?w=640\&ssl=1)
* Command to retrieve emails:

```
RETR 1
RETR 2
```

##
