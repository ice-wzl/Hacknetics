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
