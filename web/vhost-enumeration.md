# vhost Enumeration

### Gobuster

```
gobuster vhost -u http://machine.htb -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt
```

### FFuf Fuzzing for subdomains

```
ffuf -w /usr/share/SecLists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://vulnnet.thm -H "Host: FUZZ.vulnnet.thm" -fs 5829
```

* Notice that you will get back responses with a similar character count, these are often the ones that will fail, to make the output more readable, filter on the bad character count and look for one with a unique character count.

#### Another ffuf example

* In this example we know the first part of the subdomain used by the company, however we need to bruteforce the second half of the sub domain.

```
ffuf -w /mnt/home/dasor/wordlist/directory-list-2.3-big.txt:FUZZ -u http://trick.htb/ -H 'Host: preprod-FUZZ.trick.htb' -v -fs 5480
```

#### ffuf Filter out 302 redirects when looking for subdomains

* Sometimes the web server will 302 your request when bruteforcing for subdomains.
* First create a new burp listener as such&#x20;

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

Now you can use the below command and throw all the requests through the burp proxy to view the requests

```
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt:FUZZ -u http://localhost:8888 -H "Host: FUZZ.mentorquotes.htb" -fc 302
```

* Browsing to burp, we can see all the requests and the 302 redirects.  Try and figure out what stands out, if most requests are 302's look for 404's or other status codes

<figure><img src="../.gitbook/assets/image (2) (1) (1).png" alt=""><figcaption></figcaption></figure>

* Apply our filter removing all 302's

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

* Below is a command to filter the status code without using a burp proxy

```
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt:FUZZ -u http://mentorquotes.htb -H "Host: FUZZ.mentorquotes.htb" -fc 302
```

#### ffuf vhost filter by fixed size

When the default vhost returns a consistent response size, filter by that size so only different (valid) vhosts show:

```bash
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt:FUZZ \
  -u http://target.htb -H "Host: FUZZ.target.htb" -fs 230
ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-large-words.txt:FUZZ \
  -u http://target.htb -H "Host: FUZZ.target.htb" -fs 230
```

#### ffuf subdomain over HTTPS

* For HTTPS, use `-k` to skip certificate verification. Filter by status or size:
* `-fc 200` — exclude 200 (default vhost often returns 200)
* `-fs SIZE` — exclude responses with this size (baseline from invalid subdomains)

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt:FUZZ \
  -u https://target.htb -H "Host: FUZZ.target.htb" -k -fc 200
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt:FUZZ \
  -u https://target.htb -H "Host: FUZZ.target.htb" -k -fc 200
```

#### ffuf with Cookie and Matching a status code&#x20;

* \-b Cookie data `"NAME1=VALUE1; NAME2=VALUE2"` for copy as curl functionality.
* \-mc Match HTTP status codes, or "all" for everything. (default: 200,204,301,302,307,401,403)

```
ffuf -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt:FUZZ -u http://machine.htb -H "Host: FUZZ.machine.htb" -mc 200 -b "PHPSESSID=28330d435522c7f6080f8d63b86c7daa"
```

---

### WARNING: Avoid ffuf -ac (Auto-Calibrate) for vhost Enumeration

**IMPORTANT:** Do NOT blindly use `-ac` (auto-calibrate) for vhost enumeration. It can filter out important results like 421 status codes that indicate valid subdomains with different configurations.

**Example of a miss due to -ac:**

```bash
# BAD - May filter out valid subdomains
ffuf -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt:FUZZ \
  -u https://target.htb -H "Host: FUZZ.target.htb" -k -ac

# GOOD - Manually inspect results first, then filter
ffuf -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt:FUZZ \
  -u https://target.htb -H "Host: FUZZ.target.htb" -k

# Then filter based on observed baseline (e.g., filter 400 responses)
ffuf -w wordlist.txt:FUZZ -u https://target.htb -H "Host: FUZZ.target.htb" -k -fc 400
```

**Why this matters:** A 421 Misdirected Request often indicates a valid vhost that requires SNI or a different SSL certificate. Auto-calibrate may mark these as "baseline" and filter them out.

---

### wfuzz for vhost Enumeration

Alternative to ffuf with cleaner output for manual inspection.

```bash
# Basic vhost enumeration
wfuzz -c -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt \
  -u https://target.htb -H "Host: FUZZ.target.htb" --hw 28 --hc 400

# Hide specific word count and status codes
wfuzz -c -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt \
  -u https://target.htb -H "Host: FUZZ.target.htb" --hc 400,404 --hw 28
```

**Key flags:**
- `-c` - Color output
- `--hw` - Hide responses with specific word count
- `--hc` - Hide responses with specific status codes
- `--hh` - Hide responses with specific character count

**Example output showing valid subdomains:**

```
=====================================================================
ID           Response   Lines    Word       Chars       Payload
=====================================================================
000000024:   421        12 L     49 W       407 Ch      "admin"
000000373:   302        0 L      26 W       463 Ch      "intra"
```

**Tip:** Look for different status codes (421, 302) or varying response sizes to identify valid subdomains.

---

### Common Mistakes in vhost Enumeration

1. **Fuzzing the wrong domain:** If `intra.target.htb` exists, don't fuzz `FUZZ.intra.target.htb` - fuzz `FUZZ.target.htb` instead.

2. **Missing hosts file entry:** Ensure the base domain is in `/etc/hosts` before scanning.

3. **HTTPS without -k:** Use `-k` to skip SSL certificate verification for self-signed certs.
