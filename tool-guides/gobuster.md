### gobuster
- gobuster tries to find valid directories from a wordlist of possible directories. gobuster can also be used to valid subdomains using the same method.
#### Syntax
- Directory/File Brute force mode
````
dir
````
- DNS brute forcing mode
````
dns
````
- Flag for extentions to be tested against
````
-x
````
- Sets a wordlist to be used
````
-w
````
- Set username for basic authentication (if required by the directory)
````
-U
````
- Set password for basic authentication 
````
-P
````
- Set the status codes gobuster will recognize as valid
````
-s
````
- Skip ssl certificate validation
````
-k
````
- Set a user agent string
````
-a
````
- Specify and HTTP header
````
-H
````
- Set the url to brute force 
````
-u
````
- Location of the wordlists
````
/usr/share/wordlists
````
### Example full syntax
````
dirb http://10.10.10.10:80/secret/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -X .txt 
````
- This command tests the /secret/ directory 
- It specifies to use the wordlist `directory-list-2.3-medium.txt`
- and with the `-X` flag it sets gobuster to test for `.txt` file extensions i.e. admin.txt, secret.txt























