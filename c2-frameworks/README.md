# c2-frameworks

### Disowning binaries launched from SSH

* Often with C2 frameworks you will be in an SSH session on linux and will spawn a C2 payload to revieve your reverse connection back. &#x20;
* When this process is launched in the context of you ssh session, it to will die if/when you exit the ssh shell.
* Need to disown the process before exiting your ssh session&#x20;

```
#launch secondary payload
./bad.elf &
#view your current jobs 
jobs -l
#output
[1]-  4581 Running                 ./bad.elf &
#disown jobs
disown -h jobID
disown -h %2
## You should not see any jobs running on the screen ##
#verify with
jobs -l
##If disown is not on the target machine##
./bad.elf &!
```

### Example

[https://www.cyberciti.biz/faq/unix-linux-disown-command-examples-usage-syntax/#5](https://www.cyberciti.biz/faq/unix-linux-disown-command-examples-usage-syntax/#5)

```
## Step 1: update system ##
apt-get upgrade &> /root/system.update.log &
 
## Step 2: Mark apt-get so that SIGHUP is not sent when you exit and go for tea ##
disown -h 
```
