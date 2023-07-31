# cut

### Basics&#x20;

* Display 2nd character from each line in a file&#x20;

```
cut -c2 test.txt
```

* Display first three characters from each line in a file&#x20;

```
cut -c1-3 test.txt
```

* Display forst 8 characters from each line in a file&#x20;

```
cut -c-8 test.txt
```

* Display 1st field when : is the delimeter between the fields in the file&#x20;

```
cut -d ':' -f1 test.txt
```

* Display the 1st and 6th fields when : is used as a delimiter&#x20;

```
cut -d ':' -f1,6 test.txt
```

* Display all fields except the 7th field when : is used as the delimiter

```
cut -d ':' -complement -s -f7 test.txt
```
