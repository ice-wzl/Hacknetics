# sort

### Show the sorted version of file

`sort test.txt`

### Show the sorted version of file in the reverse order

`sort -r test.txt`

### Show the sorted version of file according to 2nd column (n is used if column contains numerical values)

`sort -nk2 test.txt`&#x20;

### Show the sorted version of file according to 3rd column (no numerical value in column 3)

`sort -k3 test.txt`

### Use sort command with a pipeline (without any file)

`ls -lah | sort -nk2`

### Sort the lines and remove duplicates (again this is just showing, not changing any content)

`sort -u test.txt`

### Sort the contents of 2 files and concetenate the output

`sort file1.txt file2.txt`

### Sort the contents of 2 files and concetenate the output, then remove the duplicates

`sort -u file1.txt file2.txt`

### `Credit`&#x20;

[`https://github.com/areyou1or0/Bash-Fu/blob/master/sort`](https://github.com/areyou1or0/Bash-Fu/blob/master/sort)
