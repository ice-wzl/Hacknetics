# Python3 Cheatsheet

### Comments&#x20;

```python
# Comment on a single line

user = "JDoe" # Comment after code
```

### Arithmetic Operations

* `+` for addition
* `-` for subtraction
* `*` for multiplication
* `/` for division
* `%` for modulus (returns the remainder)
* `**` for exponentiation

```python
# Arithmetic operations

result = 10 + 30
result = 40 - 10
result = 50 * 5
result = 16 / 4
result = 25 % 2
result = 5 ** 3
```

### Plus-Equals Operator `+=` <a href="#heading-plus-equals-operator" id="heading-plus-equals-operator"></a>

```python
# Plus-Equal Operator

counter = 0
counter += 10

# This is equivalent to

counter = 0
counter = counter + 10

# The operator will also perform string concatenation

message = "Part 1 of message "
message += "Part 2 of message"
```

### Variables <a href="#heading-variables" id="heading-variables"></a>

```python
# These are all valid variable names and assignment

user_name = "codey"
user_id = 100
verified = False

# A variable's value can be changed after assignment

points = 100
points = 120
```

### Modulo Operator `%` <a href="#heading-modulo-operator" id="heading-modulo-operator"></a>

* The result of the expression `4 % 2` would result in the value 0, because 4 is evenly divisible by 2 leaving no remainder.
* The result of the expression `7 % 3` would return 1, because 7 is not evenly divisible by 3, leaving a remainder of 1.

A modulo calculation returns the remainder of a division between the first and second number. For example:

```python
# Modulo operations

zero = 8 % 4

nonzero = 12 % 5
```

### Integers  <a href="#heading-integers" id="heading-integers"></a>

```python
# Example integer numbers

chairs = 4
tables = 1
broken_chairs = -2
sofas = 0

# Non-integer numbers

lights = 2.5
left_overs = 0.0
```

### String Concatenation <a href="#heading-string-concatenation" id="heading-string-concatenation"></a>

```python
# String concatenation

first = "Hello "
second = "World"

result = first + second #Hello World

long_result = first + second + "!" #Hello World!
```

### Strings

```python
user = "User Full Name"
game = 'Monopoly'

longer = "This string is broken up \
over multiple lines"
```

### Floating Point Numbers <a href="#heading-floating-point-numbers" id="heading-floating-point-numbers"></a>

```python
# Floating point numbers

pi = 3.14159
meal_cost = 12.99
tip_percent = 0.20
```

### `print()` Function <a href="#heading-print-function" id="heading-print-function"></a>

```python
print("Hello World!")

print(100)

pi = 3.14159
print(pi)
```

### elif Statements

```python
# elif Statement

pet_type = "fish"

if pet_type == "dog":
  print("You have a dog.")
elif pet_type == "cat":
  print("You have a cat.")
elif pet_type == "fish":
  # this is performed
  print("You have a fish")
else:
  print("Not sure!")
```

### or Operator

* The Python `or` operator combines two Boolean expressions and evaluates to `True` if at least one of the expressions returns `True`. Otherwise, if both expressions are `False`, then the entire expression evaluates to `False`.

```python
True or True      # Evaluates to True
True or False     # Evaluates to True
False or False    # Evaluates to False
1 < 2 or 3 < 1    # Evaluates to True
3 < 1 or 1 > 6    # Evaluates to False
1 == 1 or 1 < 2   # Evaluates to True
```

### Equal Operator `==` <a href="#heading-equal-operator" id="heading-equal-operator"></a>

```python
# Equal operator
if 'Yes' == 'Yes':  # evaluates to True  
    print('They are equal')

if (2 > 1) == (5 < 10):  # evaluates to True  
    print('Both expressions give the same result')

c = '2'd = 2
if c == d:  
    print('They are equal')
else:  
    print('They are not equal')
```

### Not Equals Operator `!=` <a href="#heading-not-equals-operator" id="heading-not-equals-operator"></a>

```python
# Not Equals Operator

if "Yes" != "No":
  # evaluates to True
  print("They are NOT equal")

val1 = 10
val2 = 20

if val1 != val2:
  print("They are NOT equal")

if (10 > 1) != (10 > 1000):
  # True != False
  print("They are NOT equal")
```

### Comparison Operators <a href="#heading-comparison-operators" id="heading-comparison-operators"></a>

```python
a = 2
b = 3py
a < b  # evaluates to True
a > b  # evaluates to False
a >= b # evaluates to False
a <= b # evaluates to True
a <= a # evaluates to True
```

### if Statements&#x20;

```python
test_value = 100

if test_value > 1:
  # Expression evaluates to True
  print("This code is executed!")

if test_value > 1000:
  # Expression evaluates to False
  print("This code is NOT executed!")

print("Program continues at this point.")
```

### else Statements

```python
test_value = 50

if test_value < 1:
  print("Value is < 1")
else:
  print("Value is >= 1")

test_string = "VALID"

if test_string == "NOT_VALID":
  print("String equals NOT_VALID")
else:
  print("String equals something else!")
```

### and Operator

```python
True and True     # Evaluates to True
True and False    # Evaluates to False
False and False   # Evaluates to False
1 == 1 and 1 < 2  # Evaluates to True
1 < 2 and 3 < 1   # Evaluates to False
"Yes" and 100     # Evaluates to True
```

### not Operator&#x20;

```python
not True     # Evaluates to False
not False    # Evaluates to True
1 > 2        # Evaluates to False
not 1 > 2    # Evaluates to True
1 == 1       # Evaluates to True
not 1 == 1   # Evaluates to False
```

### Lists <a href="#heading-lists" id="heading-lists"></a>

List values are placed in between square brackets `[ ]`, separated by commas. It is good practice to put a space between the comma and the next value. The values in a list do not need to be unique (the same value can be repeated).

Empty lists do not contain any values within the square brackets.

```python
primes = [2, 3, 5, 7, 11]print(primes)
empty_list = []
```

### Adding Lists Together <a href="#heading-adding-lists-together" id="heading-adding-lists-together"></a>

In Python, lists can be added to each other using the plus symbol `+`. As shown in the code block, this will result in a new list containing the same items in the same order with the first list’s items coming first.

**Note:** This will not work for adding one item at a time (use `.append()` method). In order to add one item, create a new list with a single value and then use the plus symbol to add the list.

```python
items = ['cake', 'cookie', 'bread']
total_items = items + ['biscuit', 'tart']
print(total_items)
# Result: 
['cake', 'cookie', 'bread', 'biscuit', 'tart']
```

### Python Lists: Data Types <a href="#heading-python-lists-data-types" id="heading-python-lists-data-types"></a>

In Python, lists are a versatile data type that can contain multiple different data types within the same square brackets. The possible data types within a list include numbers, strings, other objects, and even other lists.

```python
numbers = [1, 2, 3, 4, 10]
names = ['Jenny', 'Sam', 'Alexis']
mixed = ['Jenny', 1, 2]
list_of_lists = [['a', 1], ['b', 2]]
```

### List Method `.append()` <a href="#heading-list-method-append" id="heading-list-method-append"></a>

In Python, you can add values to the end of a list using the `.append()` method. This will place the object passed in as a new element at the very end of the list.&#x20;

```python
orders = ['daisies', 'periwinkle']
orders.append('tulips')
print(orders)
# Result: 
['daisies', 'periwinkle', 'tulips']
```

### Zero-Indexing <a href="#heading-zero-indexing" id="heading-zero-indexing"></a>

In Python, list index begins at zero and ends at the length of the list minus one. For example, in this list, `'Andy'` is found at index `2`.

```python
names = ['Roger', 'Rafael', 'Andy', 'Novak']
```

### List Indices <a href="#heading-list-indices" id="heading-list-indices"></a>

To access a list element by index, square bracket notation is used: `list[index]`.

```python
berries = ["blueberry", "cranberry", "raspberry"]
berries[0]   # "blueberry"
berries[2]   # "raspberry"
```

### Negative List Indices <a href="#heading-negative-list-indices" id="heading-negative-list-indices"></a>

* To select the last element, `my_list[-1]`.
* To select the last three elements, `my_list[-3:]`.
* To select everything except the last two elements, `my_list[:-2]`.

```python
soups = ['minestrone', 'lentil', 'pho', 'laksa']
soups[-1]   # 'laksa'
soups[-3:]  # 'lentil', 'pho', 'laksa'
soups[:-2]  # 'minestrone', 'lentil'
```

### Modifying 2D Lists <a href="#heading-modifying-2d-lists" id="heading-modifying-2d-lists"></a>

In order to modify elements in a 2D list, an index for the sublist and the index for the element of the sublist need to be provided. The format for this is `list[sublist_index][element_in_sublist_index] = new_value`.

```python
# A 2D list of names and hobbies
class_name_hobbies = [["Jenny", "Breakdancing"], ["Alexus", "Photography"], ["Grace", "Soccer"]]
# The sublist of Jenny is at index 0. The hobby is at index 1 of the sublist. 
class_name_hobbies[0][1] = "Meditation"
print(class_name_hobbies)
# Output
[["Jenny", "Meditation"], ["Alexus", "Photography"], ["Grace", "Soccer"]]
```

### Accessing 2D Lists <a href="#heading-accessing-2d-lists" id="heading-accessing-2d-lists"></a>

In order to access elements in a 2D list, an index for the sublist and the index for the element of the sublist both need to be provided. The format for this is `list[sublist_index][element_in_sublist_index]`.

```python
# 2D list of people's heights
heights = [["Noelle", 61], ["Ali", 70], ["Sam", 67]]
# Access the sublist at index 0, and then access the 1st index of that sublist. 
noelles_height = heights[0][1] 
print(noelles_height)
# Output# 
61
```

### List Method `.remove()` <a href="#heading-list-method-remove" id="heading-list-method-remove"></a>

The `.remove()` method in Python is used to remove an element from a list by passing in the value of the element to be removed as an argument. In the case where two or more elements in the list have the same value, the first occurrence of the element is removed.

```python
# Create a list
shopping_line = ["Cole", "Kip", "Chris", "Sylvana", "Chris"] 
# Removes the first occurance of "Chris"
shopping_line.remove("Chris")
print(shopping_line)
# Output# 
["Cole", "Kip", "Sylvana", "Chris"]
```

### List Method `.count()` <a href="#heading-list-method-count" id="heading-list-method-count"></a>

The `.count()` Python list method searches a list for whatever search term it receives as an argument, then returns the number of matching entries found.

```python
backpack = ['pencil', 'pen', 'notebook', 'textbook', 'pen', 'highlighter', 'pen']
numPen = backpack.count('pen')
print(numPen)
# Output: 
3
```

### Determining List Length with `len()` <a href="#heading-determining-list-length-with-len" id="heading-determining-list-length-with-len"></a>

The Python `len()` function can be used to determine the number of items found in the list it accepts as an argument.

```python
knapsack = [2, 4, 3, 7, 10]
size = len(knapsack)
print(size) 
# Output: 
5
```

### List Method `.sort()` <a href="#heading-list-method-sort" id="heading-list-method-sort"></a>

The `.sort()` Python list method will sort the contents of whatever list it is called on. Numerical lists will be sorted in ascending order, and lists of Strings will be sorted into alphabetical order. It modifies the original list, and has no return value.

```python
exampleList = [4, 2, 1, 3]
exampleList.sort()
print(exampleList)
# Output: 
[1, 2, 3, 4]
```

### List Slicing <a href="#heading-list-slicing" id="heading-list-slicing"></a>

A _slice_, or sub-list of Python list elements can be selected from a list using a colon-separated starting and ending point.

The syntax pattern is `myList[START_NUMBER:END_NUMBER]`. The slice will include the `START_NUMBER` index, and everything until but excluding the `END_NUMBER` item.

When slicing a list, a new list is returned, so if the slice is saved and then altered, the original list remains the same.

```python
tools = ['pen', 'hammer', 'lever']
tools_slice = tools[1:3] 
# ['hammer', 'lever']
tools_slice[0] = 'nail'
# Original list is unaltered:
print(tools) 
# ['pen', 'hammer', 'lever']
```

### `sorted()` Function <a href="#heading-sorted-function" id="heading-sorted-function"></a>

The Python `sorted()` function accepts a list as an argument, and will return a new, sorted list containing the same elements as the original. Numerical lists will be sorted in ascending order, and lists of Strings will be sorted into alphabetical order. It does not modify the original, unsorted list.

```python
unsortedList = [4, 2, 1, 3]
sortedList = sorted(unsortedList)
print(sortedList)
# Output: 
[1, 2, 3, 4]
```

### List Method `.insert()` <a href="#heading-list-method-insert" id="heading-list-method-insert"></a>

The Python list method `.insert()` allows us to add an element to a specific index in a list.

It takes in two inputs:

* The index that you want to insert into.
* The element that you want to insert at the specified index.

```python
# Here is a list representing a line of people at a store
store_line = ["Karla", "Maxium", "Martim", "Isabella"]
# Here is how to insert "Vikor" after "Maxium" and before "Martim"
store_line.insert(2, "Vikor")
print(store_line) 
# Output: 
['Karla', 'Maxium', 'Vikor', 'Martim', 'Isabella']
```

### List Method `.pop()` <a href="#heading-list-method-pop" id="heading-list-method-pop"></a>

The `.pop()` method allows us to remove an element from a list while also returning it. It accepts one optional input which is the index of the element to remove. If no index is provided, then the last element in the list will be removed and returned.

```python
cs_topics = ["Python", "Data Structures", "Balloon Making", "Algorithms", "Clowns 101"]
# Pop the last element
removed_element = cs_topics.pop()
print(cs_topics)
# Output:# 
['Python', 'Data Structures', 'Balloon Making', 'Algorithms']
print(removed_element)
# 'Clowns 101'
# Pop the element "Baloon Making"
cs_topics.pop(2)
print(cs_topics)
# Output:# 
['Python', 'Data Structures', 'Algorithms']
```

### `break` Keyword <a href="#heading-break-keyword" id="heading-break-keyword"></a>

In a loop, the `break` keyword escapes the loop, regardless of the iteration number. Once `break` executes, the program will continue to execute after the loop.

In this example, the output would be:

* `0`
* `254`
* `2`
* `Negative number detected!`

```python
numbers = [0, 254, 2, -1, 3]
for num in numbers:  
    if (num < 0):    
        print("Negative number detected!")    
        break  
        print(num)  
        
# 0
# 254
# 2
# Negative number detected!
```

### Python List Comprehension <a href="#heading-python-list-comprehension" id="heading-python-list-comprehension"></a>

Python list comprehensions provide a concise way for creating lists. It consists of brackets containing an expression followed by a for clause, then zero or more for or if clauses: `[EXPRESSION for ITEM in LIST <if CONDITIONAL>]`.

The expressions can be anything - any kind of object can go into a list.

A list comprehension always returns a list.

```python
# List comprehension for the squares of all even numbers between 0 and 9
result = [x**2 for x in range(10) if x % 2 == 0]
print(result)
[0, 4, 16, 36, 64]
```

### Python For Loop <a href="#heading-python-for-loop" id="heading-python-for-loop"></a>

When writing a `for` loop, remember to properly indent each action, otherwise an `IndentationError` will result.

```python
for <temporary variable> in <list variable>:  
    <action statement>  
    <action statement> 
#each num in nums will be printed 
belownums = [1,2,3,4,5]
for num in nums:   
    print(num)
```

### The Python `continue` Keyword <a href="#heading-the-python-continue-keyword" id="heading-the-python-continue-keyword"></a>

In Python, the `continue` keyword is used inside a loop to skip the remaining code inside the loop code block and begin the next loop iteration.

```python
big_number_list = [1, 2, -1, 4, -5, 5, 2, -9]
# Print only positive numbers:
for i in big_number_list:  
    if i < 0:    
        continue  
        print(i)
```

### Python Loops with `range()`. <a href="#heading-python-loops-with-range" id="heading-python-loops-with-range"></a>

In Python, a `for` loop can be used to perform an action a specific number of times in a row.

The `range()` function can be used to create a list that can be used to specify the number of iterations in a `for` loop.

```python
# Print the numbers 0, 1, 2:
for i in range(3):  
    print(i)
# Print "WARNING" 3 times:
for i in range(3):  
    print("WARNING")
```

### Infinite Loop <a href="#heading-infinite-loop" id="heading-infinite-loop"></a>

An infinite loop is a loop that never terminates. Infinite loops result when the conditions of the loop prevent it from terminating.&#x20;

### Python `while` Loops <a href="#heading-python-while-loops" id="heading-python-while-loops"></a>

In Python, a `while` loop will repeatedly execute a code block as long as a condition evaluates to `True`.

The condition of a `while` loop is always checked first before the block of code runs. If the condition is not met initially, then the code block will never run.

```python
# This loop will only run 1 time
hungry = True
while hungry:  
    print("Time to eat!")  
    hungry = False
# This loop will run 5 times
i = 1
while i < 6:  
    print(i)  
    i = i + 1
```

### Python Nested Loops <a href="#heading-python-nested-loops" id="heading-python-nested-loops"></a>

In Python, loops can be _nested_ inside other loops. Nested loops can be used to access items of lists which are inside other lists. The item selected from the outer loop can be used as the list for the inner loop to iterate over.

```python
groups = [["Jobs", "Gates"], ["Newton", "Euclid"], ["Einstein", "Feynman"]]
# This outer loop will iterate over each list in the groups list
for group in groups:  
    # This inner loop will go through each name in each list  
    for name in group:    
        print(name)
```
