# Authentication Bypass
## Username Enumeration
- Try a random username that probably does not exist, and then try one that probably exists, is there a different error?
````
jksaljkfl <- username that does not exist
admin <- username that probably exists
guest <- another potential username
````
- We can use the existence of this error message to produce a list of valid usernames already signed up on the system by using the ffuf tool below
- The ffuf tool uses a list of commonly used usernames to check against for any matches.
- Capture the request in `Burp` to find the `Content-Type`, whether its a `GET` or `POST`
````
ffuf -w /usr/share/wordlists/SecLists/Usernames/Names/names.txt -X POST -d "username=FUZZ&email=x&password=x&cpassword=x" -H "Content-Type: application/x-www-form-urlencoded" -u http://MACHINE_IP/customers/signup -mr "username already exists"
````
- `-w` -> selects the file's location
- `-X` -> argument specifies the request method
- `-d` -> the data that we are going to send
- `FUZZ` -> keyword signifies where the contents from our wordlist will be inserted in the request
- `-H` -> for adding additional headers to the request
- `-u` ->  specifies the URL we are making the request to
- `-mr` -> is the text on the page we are looking for to validate we've found a valid username







































































