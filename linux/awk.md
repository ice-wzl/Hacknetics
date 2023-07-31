# awk

### Overview&#x20;

* `awk` is a data driven programming language for processing text based data

### Basics&#x20;

* Print every line in a file&#x20;

```
awk '{print}' test.txt
```

* Print the lines which contain the given parameter&#x20;

```
awk '/item/ {print}' test.txt
```

* Print the first and fourth field with whitespace as the delimeter&#x20;

```
awk '{print $1,$4}' test.txt 
```

* Display a block of text starting with the word start and stopping with the word stop&#x20;

```
awk '/start/,/stop/' test.txt
```
