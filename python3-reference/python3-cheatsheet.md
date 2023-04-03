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
