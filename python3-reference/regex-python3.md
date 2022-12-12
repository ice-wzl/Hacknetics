# Regex Python3

### Character Sets in Regular Expressions <a href="#heading-character-sets-in-regular-expressions" id="heading-character-sets-in-regular-expressions"></a>

* Regular expression character sets denoted by a pair of brackets `[]` will match any of the characters included within the brackets.&#x20;
* For example, the regular expression `con[sc]en[sc]us` will match any of the spellings `consensus`, `concensus`, `consencus`, and `concencus`.

### Optional Quantifiers in Regular Expressions <a href="#heading-optional-quantifiers-in-regular-expressions" id="heading-optional-quantifiers-in-regular-expressions"></a>

* In Regular expressions, optional quantifiers are denoted by a question mark `?`.&#x20;
* It indicates that a character can appear either 0 or 1 time.&#x20;
* For example, the regular expression `humou?r` will match the text `humour` as well as the text `humor`.

### Literals in Regular Expressions <a href="#heading-literals-in-regular-expressions" id="heading-literals-in-regular-expressions"></a>

* In Regular expression, the `literals` are the simplest characters that will match the exact text of the literals.&#x20;
* For example, the regex `monkey` will completely match the text `monkey` but will also match `monkey` in text `The monkeys like to eat bananas.`

### Fixed Quantifiers in Regular Expressions <a href="#heading-fixed-quantifiers-in-regular-expressions" id="heading-fixed-quantifiers-in-regular-expressions"></a>

* In Regular expressions, fixed quantifiers are denoted by curly braces `{}`.&#x20;
* It contains either the exact quantity or the quantity range of characters to be matched.&#x20;
* For example, the regular expression `roa{3}r` will match the text `roaaar`, while the regular expression `roa{3,6}r` will match `roaaar`, `roaaaar`, `roaaaaar`, or `roaaaaaar`.

### Alternation in Regular Expressions <a href="#heading-alternation-in-regular-expressions" id="heading-alternation-in-regular-expressions"></a>

* Alternation indicated by the pipe symbol `|`, allows for the matching of either of two subexpressions.&#x20;
* For example, the regex `baboons|gorillas` will match the text `baboons` as well as the text `gorillas`.

### Anchors in Regular Expressions <a href="#heading-anchors-in-regular-expressions" id="heading-anchors-in-regular-expressions"></a>

* Anchors (hat `^` and dollar sign `$`) are used in regular expressions to match text at the start and end of a string, respectively.&#x20;
* For example, the regex `^Monkeys: my mortal enemy$` will completely match the text `Monkeys: my mortal enemy` but not match `Spider Monkeys: my mortal enemy` or `Monkeys: my mortal enemy in the wild`.&#x20;
* The `^` ensures that the matched text begins with `Monkeys`, and the `$` ensures the matched text ends with `enemy`.

### Regular Expressions <a href="#heading-regular-expressions" id="heading-regular-expressions"></a>

* Regular expressions are sequence of characters defining a pattern of text that needs to be found.&#x20;
* They can be used for parsing the text files for specific pattern, verifying test results, and finding keywords in emails or webpages.

### Wildcards in Regular expressions <a href="#heading-wildcards-in-regular-expressions" id="heading-wildcards-in-regular-expressions"></a>

* In Regular expression, wildcards are denoted with the period `.` and it can match any single character (letter, number, symbol or whitespace) in a piece of text.&#x20;
* For example, the regular expression `.........` will match the text `orangutan`, `marsupial`, or any other 9-character text.

### Regular Expression Ranges <a href="#heading-regular-expression-ranges" id="heading-regular-expression-ranges"></a>

* Regular expression ranges are used to specify a range of characters that can be matched.&#x20;
* Common regular expression ranges include: \[A-Z]. : match any uppercase letter \[a-z]. : match any lowercase letter \[0-9]. : match any digit \[A-Za-z] : match any uppercase or lowercase letter.

### Shorthand Character Classes in Regular Expressions <a href="#heading-shorthand-character-classes-in-regular-expressions" id="heading-shorthand-character-classes-in-regular-expressions"></a>

* Shorthand character classes simplify writing regular expressions. For example, `\w` represents the regex range `[A-Za-z0-9_]`, `\d` represents \[0-9], `\W` represents `[^A-Za-z0-9_]` matching any character not included by `\w`, `\D` represents `[^0-9]` matching any character not included by `\d`.

### Kleene Star & Kleene Plus in Regular Expressions <a href="#heading-kleene-star--kleene-plus-in-regular-expressions" id="heading-kleene-star--kleene-plus-in-regular-expressions"></a>

* In Regular expressions, the Kleene star(`*`) indicates that the preceding character can occur 0 or more times.&#x20;
* For example, `meo*w` will match `mew`, `meow`, `meooow`, and `meoooooooooooow`.&#x20;
* The Kleene plus(`+`) indicates that the preceding character can occur 1 or more times.&#x20;
* For example, `meo+w` will match `meow`, `meooow`, and `meoooooooooooow`, but not match `mew`.

### Grouping in Regular Expressions <a href="#heading-grouping-in-regular-expressions" id="heading-grouping-in-regular-expressions"></a>

* In Regular expressions, grouping is accomplished by open `(` and close parenthesis `)`.&#x20;
* Thus the regular expression `I love (baboons|gorillas)` will match the text `I love baboons` as well as `I love gorillas`, as the grouping limits the reach of the `|` to the text within the parentheses.

### Credit for This Page:

[https://www.codecademy.com/learn/paths/build-chatbots-with-python/tracks/rule-based-chatbots/modules/intro-to-regex/cheatsheet](https://www.codecademy.com/learn/paths/build-chatbots-with-python/tracks/rule-based-chatbots/modules/intro-to-regex/cheatsheet)
