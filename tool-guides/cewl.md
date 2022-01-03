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
