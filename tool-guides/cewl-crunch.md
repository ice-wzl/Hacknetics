# Cewl
- Custom password list creator
## Example Syntax
````
user@thm$ cewl -w list.txt -d 5 -m 5 http://thm.labs
````
- -w will write the contents to a file. In this case, list.txt.

- -m 5 gathers strings (words) that are 5 characters or more

- -d 5 is the depth level of web crawling/spidering (default 2)

- `http://thm.labs` is the URL that will be used

# Crunch
- crunch is one of many powerful tools for creating an offline wordlist.
## Example Syntax
````
user@thm$ crunch 2 2 01234abcd -o crunch.txt
````
- Creates a wordlist containing all possible combinations of `two` characters including `a-d` and `0-4`.
- -o specifies a file to save to
````
crunch 8 8 0123456789abcdefABCDEF -o crunch.txt
````
- Creates a wordlist containing all possible combinations of `a-f` and `0-9`
- *WARNING* above command creates a file that is 459GB in size
### Additional Flags
- @ --> lower case alpha characters
- , --> upper case alpha characters
- % --> numberic characters
- ^ --> special characters including spaces
## Example
- If we know part of the password is `pass` followed by two numbers `XX` we can generate a wordlist with the `%` flag.
````
crunch 6 6 -t pass%%
````
- Output of wordlist
````
Crunch will now generate the following amount of data: 700 bytes
0 MB
0 GB
0 TB
0 PB
Crunch will now generate the following number of lines: 100
pass00
pass01
pass02
pass03
````
