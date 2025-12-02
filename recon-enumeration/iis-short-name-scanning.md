# IIS Short name scanning

### Shortscan (Github)

* The best shortname scanner I have found so far
* [https://github.com/bitquark/shortscan](https://github.com/bitquark/shortscan)
* Build both binaries&#x20;

```
// shortutil
go build
// shortscan
go build
```

* Make a shortname wordlist based upon another common wordlist

```
./shortutil wordlist /usr/share/seclists/Discovery/Web-Content/common.txt > common.txt 
```

* Fire up the scanner

```
./shortscan --wordlist ../shortutil/raft-small-words.txt http://10.13.38.11           ✭main 
🌀 Shortscan v0.9.2 · an IIS short filename enumeration tool by bitquark

════════════════════════════════════════════════════════════════════════════════
URL: http://10.13.38.11/
Running: Microsoft-IIS/10.0
Vulnerable: Yes!
════════════════════════════════════════════════════════════════════════════════
NEWFOL~2             NEWFOL?    
DS_STO~1             DS_STO?             .DS_STORE
TRASHE~1             TRASHE?    
TEMPLA~1             TEMPLA?             TEMPLATES
WEB~1.CON            WEB.CON?   
NEWFOL~1             NEWFOL?    
════════════════════════════════════════════════════════════════════════════════

════════════════════════════════════════════════════════════════════════════════
URL: http://10.13.38.11/TEMPLATES/
Running: Microsoft-IIS/10.0
Vulnerable: No (or no 8.3 files exist)
════════════════════════════════════════════════════════════════════════════════
```

#### IIS-ShortName-Scanner

* [https://github.com/irsdl/IIS-ShortName-Scanner/tree/master](https://github.com/irsdl/IIS-ShortName-Scanner/tree/master)

```
java -jar iis_shortname_scanner.jar 

# IIS Short Name (8.3) Scanner version 2023.4 - scan initiated 2025/10/29 00:58:24
Target: http://10.13.38.11/
|_ Result: Vulnerable!
|_ Used HTTP method: OPTIONS
|_ Suffix (magic part): /~1/.rem
|_ Extra information:
  |_ Number of sent requests: 27
```
