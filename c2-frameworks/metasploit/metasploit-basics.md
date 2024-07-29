# Metasploit Basics

### MSFDB

* After install initialize the MSF database for the first time with&#x20;

```
sudo msfdb init
```

* View if the database is running/start the database&#x20;

```
sudo msfdb start
sudo msfdb status
sudo msfdb stop
```

* start the framework&#x20;

```
msfconsole -q
```

### Basics

* Search for modules&#x20;

```
search [regex]
```

* search for type along with keyword

```
search type:post -S "firefox"
```

* Specify exploit

```
use exploit /path/to/exploit
```

### Types of Payloads&#x20;

* Singles
  * **Singles** are payloads that are self-contained and completely standalone. These can be as simple as running calc.exe, adding a user to the system or deleting a file. Since single payloads are self-contained, they can be caught with non-metasploit handlers like [netcat](https://en.wikipedia.org/wiki/Netcat) for example.
* Stager
  * **Stagers** are payloads that setup a network connection between victim and attacker and download additional components or applications. A typical example of a stager is one that makes the victim system setup a tcp connection _to_ the attacker: the _**reverse\_tcp**_ stager. Another example is the _**bind\_tcp**_ stager that lets the victim open a tcp listener to which the attacker will make a connection.
* Stages
  * **Stages** are payload components that are downloaded by a stager. These payloads provide advanced features with no size limits. Some examples are a simple shell, but also VNC Injection, iPhone 'ipwn' shell and Meterpreter
* In Metasploit, the type of payload can be deducted from its name.
  * Single payloads have the format `<target> / <single>`
  * Stager/Stage payloads have the format `<target> / <stage> / <stager>`
* When executing the [show payloads](https://www.coengoedegebure.com/metasploit-wannacry-windowsupdate#anchor\_showpayloads) command in Metasploit, it shows a list of compatible payloads (or all payloads when not executed in the context of a module).

```
show payloads
```

* Specify Payload&#x20;

```
set payload path/to/payload
```

* Set option

```
set [option] [value]
```

* Run Exploit

```
run
exploit 
#either will work 
```
