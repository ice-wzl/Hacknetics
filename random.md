# Random

### Cool heredoc&#x20;

* Use when you are on a `/bin/sh` and need to `su` but dont want to go into a full `tty`

```
su - root <<!
Passw0rd
id
ls /root
!
Password: uid=0(root) gid=0(root) groups=0(root)
Desktop  Documents  Downloads  go  Music  Pictures  Public  Templates  thinclient_drives  Videos
```
