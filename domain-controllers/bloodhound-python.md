# Bloodhound Python

### Install&#x20;

```
mkdir bloodhound; cd bloodhound
python3 -m venv .venv
source .venv/bin/activate 

pip3 install bloodhound
--or-- 
git clone https://github.com/fox-it/BloodHound.py.git
cd bloodhound 
python3 setup.py install
```

* This tool can pull alot of network resources which can be disastrous if the network has network level monitoring
* Limit bandwidth with `--searchbase`

#### ACL Query (lots of bandwidth)

```
proxychains bloodhound-python -C ACL --domain rastalabs.local --username administrator --ldappassword password123 --domain-controller 10.10.120.1 -ns 10.10.120.2 --dns-tcp
```

* Above query will collect ACL for any and all objects that are not users or computers in the domain

#### Resolve all group memberships in domain&#x20;

```
proxychains bloodhound-python -C Group--domain rastalabs.local --username administrator --ldappassword password123 --domain-controller 10.10.120.1 -ns 10.10.120.2 --dns-tcp
```

#### Run queries on DC only&#x20;

```
proxychains bloodhound-python -C DCOnly --domain rastalabs.local --username administrator --ldappassword password123 --domain-controller 10.10.120.1 -ns 10.10.120.2 --dns-tcp
```

#### Domain Trusts

```
proxychains bloodhound-python -C Trusts --domain rastalabs.local --username administrator --ldappassword password123 --domain-controller 10.10.120.1 -ns 10.10.120.2 --dns-tcp
```

#### Objects

```
proxychains bloodhound-python -C ObjectProps --domain rastalabs.local --username administrator --ldappassword password123 --domain-controller 10.10.120.1 -ns 10.10.120.2 --dns-tcp
```

* Above will query properties off all objects, largest query limit with `--searchbase`
