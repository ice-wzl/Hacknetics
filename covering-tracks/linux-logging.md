# Linux Logging

## Limit Logging from SSH Session

* To avoid logging in `/var/log/wtmp`&#x20;
*

## Finding Writable Directories for your Current User

```
find / -type d -perm -0222 2>/dev/null
```

* Good hiding spots:

```
/dev/shm
/usr/local/man 
/usr/src
```

## Unix Logging

* Main log files can be identified by viewing

```
/etc/syslog.conf
```

* Majority of the log files

```
/var/log
```

## Hiding Shell History

* Kill bash shell and prevent command writing to `.bash_history`

```
kill -9 $$
```

* Dont save history for shell session, run as your first command when you get on the box

```
unset HISTFILE
```

* On some distributions adding a leading space will prevent the command from writing
* This will only work if the eviromental variable `HISTCONTROL` is set to `ignorespace`

```
 ls 
```

## Accounting Entries in Unix

* Currently logged in users
* Distro Dependent

```
/var/log/utmp
```

* Successful login attempts

```
/var/log/wtmp
```

* Unsuccessful login attempts
* Some admins will turn this off so evidence of miss typed password in the username field are not saved

```
/var/log/btmp
```

* File to show login name, port, and last login time for each user

```
/var/log/lastlog
```

* These are binary files and need special tools in order to edit

## Log Files to Check

```
/var/log/auth.log
/var/log/syslog
/var/log/messages
/var/spool/mail/root
/var/log/secure
/var/log/cron
/var/log/httpd/access_log*
/var/log/httpd/error_log*
```
