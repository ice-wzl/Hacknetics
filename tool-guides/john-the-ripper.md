# John
## Identifying Hashes
- https://hashes.com/en/tools/hash_identifier
- https://www.tunnelsup.com/hash-analyzer/
- https://md5hashing.net/hash/ 
## Online Hash Crackers
- https://crackstation.net
- https://hashes.com/en/decrypt/hash
## Format-Specific Cracking
Once you have identified the hash that you're dealing with, you can tell john to use it while cracking the provided hash using the following syntax:
````
john --format=[format] --wordlist=[path to wordlist] [path to file]
````
- This is the flag to tell John that you're giving it a hash of a specific format, and to use the following format to crack it
- `--format=` 
### Example Usage:
````
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash_to_crack.txt
````
- A Note on Formats:
- When you are telling john to use formats, if you're dealing with a standard hash type, e.g. md5 as in the example above, you have to prefix it withraw- to tell john you're just dealing with a standard hash type, though this doesn't always apply. 
- To check if you need to add the prefix or not, you can list all of John's formats using john --list=formats and either check manually, or grep for your hash type using something like 
````
john --list=formats | grep -iF "md5".
````
## Cracking Windows Hashes
### NTHash and NTLM
- NThash is the hash format that modern Windows Operating System machines will store user and service passwords in. 
- It's also commonly referred to as "NTLM" which references the previous version of Windows format for hashing passwords known as "LM", thus "NT/LM".
-You can acquire NTHash/NTLM hashes by dumping the SAM database on a Windows machine.
- By using a tool like Mimikatz or from the Active Directory database: NTDS.dit. 
- You may not have to crack the hash to continue privilege escalation- as you can often conduct a "pass the hash" attack instead, but sometimes hash cracking is a viable option if there is a weak password policy.
## Cracking Hashes on Linux
### Unshadowing
- John can be very particular about the formats it needs data in to be able to work with it, for this reason- in order to crack /etc/shadow passwords, you must combine it with the /etc/passwd file in order for John to understand the data it's being given. To do this, we use a tool built into the John suite of tools called unshadow. The basic syntax of unshadow is as follows:
````
unshadow [path to passwd] [path to shadow]
````
- `unshadow` - Invokes the unshadow tool
- `[path to passwd]` - The file that contains the copy of the /etc/passwd file you've taken from the target machine
- `[path to shadow]` - The file that contains the copy of the /etc/shadow file you've taken from the target machine
### Example Usage:
````
unshadow local_passwd local_shadow > unshadowed.txt
````
#### Note on the files
- When using unshadow, you can either use the entire /etc/passwd and /etc/shadow file- if you have them available, or you can use the relevant line from each, for example:
- FILE 1 - local_passwd
- Contains the /etc/passwd line for the root user:
````
root:x:0:0::/root:/bin/bash
````
- FILE 2 - local_shadow
- Contains the /etc/shadow line for the root user:
````
root:$6$2nwjN454g.dv4HN/$m9Z/r2xVfweYVkrr.v5Ft8Ws3/YYksfNwq96UL1FX0OJjY1L6l.DS3KEVsZ9rOVLB/ldTeEL/OIhJZ4GMFMGA0:18576::::::
````
### Cracking
- We're then able to feed the output from unshadow, in our example use case called "unshadowed.txt" directly into John. 
- We should not need to specify a mode here as we have made the input specifically for John. 
- However in some cases you will need to specify the format as we have done previously using: `--format=sha512crypt`.
````
john --wordlist=/usr/share/wordlists/rockyou.txt --format=sha512crypt unshadowed.txt
````
## Cracking Zip Password Protected File
### Zip2John
- Similarly to the unshadow tool that we used previously, we're going to be using the zip2john tool to convert the zip file into a hash format that John is able to understand
- The basic usage is like this:
````
zip2john [options] [zip file] > [output file]
````
- `[options]` - Allows you to pass specific checksum options to zip2john, this shouldn't often be necessary
- `[zip file]` - The path to the zip file you wish to get the hash of
- `>` - This is the output director, we're using this to send the output from this file to the...
- `[output file]` - This is the file that will store the output from
#### Example Usage
````
zip2john zipfile.zip > zip_hash.txt
````
#### Cracking
- We're then able to take the file we output from zip2john in our example use case called "zip_hash.txt" and, as we did with unshadow, feed it directly into John as we have made the input specifically for it.
````
john --wordlist=/usr/share/wordlists/rockyou.txt zip_hash.txt
````
## Cracking a Password Protected RAR Archive
### Rar2John
- Almost identical to the zip2john tool that we just used, we're going to use the rar2john tool to convert the rar file into a hash format that John is able to understand. 
- The basic syntax is as follows:
````
rar2john [rar file] > [output file]
````
- `rar2john` - Invokes the rar2john tool
- `[rar file]` - The path to the rar file you wish to get the hash of
- `>` - This is the output director, we're using this to send the output from this file to the...
- `[output file]` - This is the file that will store the output from
#### Example Usage
````
rar2john rarfile.rar > rar_hash.txt
````
#### Cracking
- Once again, we're then able to take the file we output from rar2john in our example use case called "rar_hash.txt" and, as we did with zip2john we can feed it directly into John..
````
john --wordlist=/usr/share/wordlists/rockyou.txt rar_hash.txt
````
## Cracking SSH Keys
### SSH2John
- As the name suggests ssh2john converts the id_rsa private key that you use to login to the SSH session into hash format that john can work with. 
- Note that if you don't have ssh2john installed, you can use ssh2john.py, which is located in the `/opt/john/ssh2john.py`. 
- If you're doing this, replace the ssh2john command with python3 /opt/ssh2john.py or on Kali, python /usr/share/john/ssh2john.py.
````
ssh2john [id_rsa private key file] > [output file]
````
- `ssh2john` - Invokes the ssh2john tool
- `[id_rsa private key file]` - The path to the id_rsa file you wish to get the hash of
- `>` - This is the output director, we're using this to send the output from this file to the...
- `[output file]` - This is the file that will store the output from
#### Example Usage
````
ssh2john id_rsa > id_rsa_hash.txt
````
#### Cracking
- For the final time, we're feeding the file we output from ssh2john, which in our example use case is called "id_rsa_hash.txt" and, as we did with rar2john we can use this seamlessly with John:
````
john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa_hash.txt
````
## PGP Keys
- Have a file `tryhackme.adc` (the PGP Private Key block) and `credential.pgp` (the encrypted file)
- Use `gpg2john` output the PGP key to a hash format
````
gpg2john tryhackme.asc > hash
````
- Should look like this:
````
tryhackme:$gpg$*17*54*3072*713ee3f57cc950f8f89155679abe2476c62bbd286ded0e049f886d32d2b9eb06f482e9770c710abc2903f1ed70af6fcc22f5608760be*3*254*2*9*16*0c99d5dae8216f2155ba2abfcc71f818*65536*c8f277d2faf97480:::tryhackme <stuxnet@tryhackme.com>::tryhackme.asc
````
- Crack the hash
````
john --wordlist=/usr/share/wordlists/rockyou.txt hash
john --format=gpg --wordlist=/usr/share/wordlists/rockyou.txt hash
````
- Should end up with the file contents
````
tryhackme:alexandru:::tryhackme <stuxnet@tryhackme.com>::tryhackme.asc
````
- Now need to use gpg to import the key back on the target box
````
gpg --import tryhackme.asc
gpg --decrypt credential.pgp
````
### Note
- All credit goes to the creator(s) of the John the Ripper Tool on THM.
- www.tryhackme.com/room/johntheripper0










