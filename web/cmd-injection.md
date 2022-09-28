# Cmd Injection

## Where Would You Find Command Injection

* In the following places:
* Text boxes that take in input
* Hidden URLs that take input
* E.g. `/execute/command-name`
* Or through queries e.g. `/location?parameter=command`
* When using URLs, remember to URL encode the characters that aren’t accepted
* Hidden ports:
* Some frameworks open debug ports that take in arbitrary commands

### Overview

* Use command line symbols within the input to alter the executed command
* Pay close attention to functions within an application that tend to be performed by an OS command
* Two forms exist, blind command injection --> you do not see the returned output, and non-blind cmd injection --> the system command output gets returned back to you
* Ensure you use the proper system commands per the OS

```
cat vs type 
ping -c vs ping -n #ping -n causes an infinte ping loop in linux
ls vs dir
```

* Try to start with reading a world readable file&#x20;

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

## Non-Blind CMD Inj.

* At the most basic level:
* Use command line symbols within the input to alter the executed command
* Once you have identified a potential injection point, use command line symbols within the input to alter the executed command&#x20;

```
; | || & && > >>
```

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

* Once you have exploited non-blind cmd injection, escalate to a reverse shell.

### Blind CMD Injection

#### Identification

* ICMP and DNS are useful to determine blind cmd injection&#x20;

```
google.com; ping -c11 127.0.0.1 #server will hang for roughly 10 seconds
```

* Can also try to ping yourself, however many corporate environments have firewalls in place to stop this, so doesn't always mean blind cmd injection isn't taking place&#x20;
* Use `tcpdump` to capture the `icmp` echo requests.

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

* This proves blind cmd injection, escalate to reverse shell

### Burp Collaborator

*
