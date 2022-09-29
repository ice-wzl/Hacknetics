# JWT Tokens

### Format

* JWT tokens will be denoted by alpha numeric stings broken up by two `.` characters.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InR5bGVyXzdjMDc3NzBmZDciLCJpYXQiOjE2NjQyODc1ODV9.bxi-fAIhRRRuZyP7qZTSIuuSEl8qHwZal86C-JCFMPg
```

* Decode the JWT and see what data it stores at:
* [https://jwt.io/](https://jwt.io/)
*

    <figure><img src="../.gitbook/assets/image (2) (1) (3).png" alt=""><figcaption></figcaption></figure>

### JWT Tool

* Offers an automated way to test JWT tokens and how the site is using them, looks for common vulns

#### Install&#x20;

```
sudo git clone https://github.com/ticarpi/jwt_tool
cd jwt_tool/
python3 -m pip install termcolor cprint pycryptodomex requests
```

#### Usage&#x20;

```
python3 jwt_tool.py -M at -t "http://104.248.162.85:31635/" -rh "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InR5bGVyXzdjMDc3NzBmZDciLCJpYXQiOjE2NjQyODc1ODV9.bxi-fAIhRRRuZyP7qZTSIuuSEl8qHwZal86C-JCFMPg"
```
