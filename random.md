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

### Bypass a disabled command prompt with /k

```
# Win+R (To bring up Run Box)
cmd.exe /k "whoami"
```

**Description:** _'This command prompt has been disabled by your administrator...' Can usually be seen in environments such as kiosks PCs, a quick hacky work around is to use /k via the windows run box. This will carry out the command and then show the restriction message, allowing for command execution._
