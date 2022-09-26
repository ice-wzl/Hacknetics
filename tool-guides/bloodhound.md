# Bloodhound

### Installing bloodhound on kali:

```
apt-get install bloodhound
```

### Configure Bloodhound

* we need to configure neo4j - mainly just change default passwords, so let's run:

```
neo4j console
#ensure you are the root user, or it will fail
```

<figure><img src="../.gitbook/assets/image (2) (2).png" alt=""><figcaption></figcaption></figure>

* Nav to `http://localhost:7474`&#x20;
* Config a DB user account by changing default passwords from `neo4j:neo4j` to something else

### Running Bloodhound

* Run bloodhound with:

```
bloodhound
#ensure you are the root user
```

* Now log into the DB with the user and password you just set up&#x20;

![](<../.gitbook/assets/image (3) (1).png>)

### Data Injection and Enumeration

* In order for BloodHound to do its magic, we need to enumerate a victim domain. The enumeration process produces a JSON file that describes various relationships and permissions between AD objects as mentioned earlier, which can then be imported to BloodHound. Once the resulting JSON file is ingested/imported to BloodHound, it will allow us to visually see the ways (if any) how Active Directory and its various objects can be (ab)used to elevate privileges, ideally to Domain Admin.
* Above paragraph taken from this great guide:

```
https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/abusing-active-directory-with-bloodhound-on-kali-linux
```

### SharpHound

* The tool that does the AD enumeration is SharpHound.
* It can be downloaded in release form here
* [https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors](https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors)
* It comes in a .exe or .ps1 file

#### AD Enumeration with SharpHound

* If you are on a machine that is a member of a domain but are authenticated as just a local use (not a domain user) you will get an error that states:

```
Unable to contact domain. Try from a domain context!
```

* If you have creds to a domain user use the `runas` utility:

```
runas /user:svc-alfresco@10.10.10.161 powershell
#if machine is not a domain member 
runas /netonly /user:svc-alfresco@10.10.10.161 powershell
```

* Once that is done or you have a domain compromised account we can proceed:
* Powershell Version:

```
. .\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All -JSONFolder "c:\Users\svc-alfresko\Desktop"
```

* C# method

```
./SharpHound.exe
```

* Both of these will produce a .zip, exfil that file back to bloodhound and simply drag and drop it into the GUI

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

### Execution

* Once the data is ingested, as mentioned, we can play around with the built in queries to find things like All Domain Admins, Shortest Path to Domain Admins and similar, that may help us as an attacker to escalate privileges and compromise the entire domains/forest.
* Mark the user account you have compromised as `"Owned"`  --> Find user you own --> right click --> Mark User as Owned

![](<../.gitbook/assets/image (5).png>)

* Now from the `Analysis` tab a great query is `Shortest Path from Owned Principles`

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

* If you over over the lines and --> right click --> help it will give you information along with commands to take advantage of vulns

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>
