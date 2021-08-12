# Cmd Injection
## Where Would You Find Command Injection
- In the following places:
- Text boxes that take in input
- Hidden URLs that take input
- E.g. `/execute/command-name`
- Or through queries e.g. `/location?parameter=command`
- When using URLs, remember to URL encode the characters that aren’t accepted
- Hidden ports:
- Some frameworks open debug ports that take in arbitrary commands 
## Tools
### dirsearch
````
dirsearch -u http://10.10.145.15:3000/api/cmd -t 16 -w /usr/share/wordlists/dirb/common.txt
````





















