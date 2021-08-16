## Grep and Sed
- Useful Regex
- Find mac addresses
````
cat file1 | sed -e 's/^.*\([a-fA-F0-9]\{12\}\).*$/\1/'
````
-Find ip addresses
````
cat file1 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
````
- Find backups on Linux
````
locate shadow 
find / -type f -name *.bak 2>/dev/null
````

