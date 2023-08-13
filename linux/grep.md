# grep

### Search all lines with specified string in a file

`grep "string" test.txt`&#x20;

### Search all lines with specified string in a file pattern (test\_1.txt, test\_2.txt, test\_3.txt ...)

`grep "string" test_*.txt`&#x20;

### Case insensitive search all lines with specified string in a file

`grep -i "string" test.txt`&#x20;

### match regex in files (\*)

`grep "REGEX" test.txt`

### Match lines with the pattern starts with "first" and ends with "last" with anything in-between

`grep "start.*end" test.txt`&#x20;

### search for full words, not for sub-strings

`grep -iw "is" test.txt`

### display line matches the pattern and N lines after match

`grep -A 3 "string" test.txt`&#x20;

### display line matches the pattern and N lines before match

`grep -B 2 "string" test.txt`&#x20;

### display line matches the pattern and N lines before match and N lines after match

`grep -C 2 "string" test.txt`&#x20;

### search all files recursively

`grep -r "string" *`&#x20;

### display all lines that doesn’t match the given pattern

`grep -v "string" test.txt`&#x20;

### display lines that doesn’t match all the given pattern (if there are more than one pattern)

`grep -v -e "string1" -v -e "string2" test.txt`

### count the number of lines that matches the pattern

`grep -c "string" test.txt`

### count the number of lines that don’t match the pattern

`grep -v -c "string" test.txt`

### display only the filenames containing the given pattern (test\_1.txt, test\_2.txt, test\_3.txt ...)

`grep -l "string" test_*.txt`

### Show only the matched string, not the whole line

`grep -o "start.*end" test.txt`

### show line number while displaying the output

`grep -n "string" test.txt`

* (\*) Regex: ? The preceding item is optional and matched at most once.
* The preceding item will be matched zero or more times.
* The preceding item will be matched one or more times. {n} The preceding item is matched exactly n times. {n,} The preceding item is matched n or more times. {,m} The preceding item is matched at most m times. {n,m} The preceding item is matched at least n times, but not more than m times.&#x20;

### Credit:&#x20;

{% embed url="https://github.com/areyou1or0/Bash-Fu/blob/master/grep" %}

* Useful Regex

### Find mac addresses

```
cat file1 | sed -e 's/^.*\([a-fA-F0-9]\{12\}\).*$/\1/'
```

### Find ip addresses

```
cat file1 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
```
