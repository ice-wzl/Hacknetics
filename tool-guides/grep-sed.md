# Grep and Sed

* Useful Regex
* Find mac addresses

```
cat file1 | sed -e 's/^.*\([a-fA-F0-9]\{12\}\).*$/\1/'
```

* Find ip addresses

```
cat file1 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
```

