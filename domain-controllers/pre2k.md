# Pre2k

Pre2k is a tool to query for the existence of pre-windows 2000 computer objects which can be leveraged to gain a foothold in a target domain as discovered by [@Oddvarmoe](https://twitter.com/Oddvarmoe). Pre2k can be ran from an uanuthenticated context to perform a password spray from a provided list of recovered hostnames (such as from an RPC/LDAP null bind) or from an authenticated context to perform a targeted or broad password spray.

* https://github.com/garrettfoster13/pre2k

## INSTALL AND BUILD VENV

```
git clone https://github.com/garrettfoster13/pre2k.git 
cd pre2k/ 
python3 -m venv venv 
source venv/bin/activate 
pip3 install .
```

### Enumerate with Users File

```
pre2k unauth -d vintage.htb -dc-ip 10.10.12.45 -save -inputfile users
```
