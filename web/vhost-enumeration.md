# vhost Enumeration

### Gobuster

```
gobuster vhost -u http://machine.htb -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt
```

### FFuf Fuzzing for subdomains

```
ffuf -u http://vulnnet.thm -H "Host: FUZZ.vulnnet.thm" -w /usr/share/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -fs 5829
```

* Notice that you will get back responses with a similar character count, these are often the ones that will fail, to make the output more readable, filter on the bad character count and look for one with a unique character count.

#### Another ffuf example

* In this example we know the first part of the subdomain used by the company, however we need to bruteforce the second half of the sub domain.

```
ffuf -w /mnt/home/dasor/wordlist/directory-list-2.3-big.txt:FUZZ -u http://trick.htb/ -H 'Host: preprod-FUZZ.trick.htb' -v -fs 5480
```

#### ffuf Filter out 302 redirects when looking for subdomains

* Sometimes the web server will 302 your request when bruteforcing for subdomains.
* First create a new burp listener as such&#x20;

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

Now you can use the below command and throw all the requests through the burp proxy to view the requests

```
ffuf -u http://localhost:8888 -H "Host: FUZZ.mentorquotes.htb" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -fc 302
```

* Browsing to burp, we can see all the requests and the 302 redirects.  Try and figure out what stands out, if most requests are 302's look for 404's or other status codes

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

* Apply our filter removing all 302's

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

* Below is a command to filter the status code without using a burp proxy

```
ffuf -u http://mentorquotes.htb -H "Host: FUZZ.mentorquotes.htb" -w /usr/share/seclists/Disc
```

#### ffuf with Cookie and Matching a status code&#x20;

* \-b Cookie data `"NAME1=VALUE1; NAME2=VALUE2"` for copy as curl functionality.
* \-mc Match HTTP status codes, or "all" for everything. (default: 200,204,301,302,307,401,403)

```
ffuf -u http://machine.htb -H "Host: FUZZ.machine.htb" -mc 200 -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt -b "PHPSESSID=28330d435522c7f6080f8d63b86c7daa"
```
