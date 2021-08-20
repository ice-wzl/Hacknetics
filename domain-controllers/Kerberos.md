# Kerberos
## What is Kerberos
- Kerberos is the default authentication service for Microsoft Windows domains. 
- It is intended to be more "secure" than NTLM by using third party ticket authorization as well as stronger encryption.
## Basic Terms
- Ticket Granting Ticket (TGT) - A ticket-granting ticket is an authentication ticket used to request service tickets from the TGS for specific resources from the domain.
- Key Distribution Center (KDC) - The Key Distribution Center is a service for issuing TGTs and service tickets that consist of the Authentication Service and the Ticket Granting Service.
- Authentication Service (AS) - The Authentication Service issues TGTs to be used by the TGS in the domain to request access to other machines and service tickets.
- Ticket Granting Service (TGS) - The Ticket Granting Service takes the TGT and returns a ticket to a machine on the domain.
- Service Principal Name (SPN) - A Service Principal Name is an identifier given to a service instance to associate a service instance with a domain service account. Windows requires that services have a domain service account which is why a service needs an SPN set.
- KDC Long Term Secret Key (KDC LT Key) - The KDC key is based on the KRBTGT service account. It is used to encrypt the TGT and sign the PAC.
- Client Long Term Secret Key (Client LT Key) - The client key is based on the computer or service account. It is used to check the encrypted timestamp and encrypt the session key.
- Service Long Term Secret Key (Service LT Key) - The service key is based on the service account. It is used to encrypt the service portion of the service ticket and sign the PAC.
- Session Key - Issued by the KDC when a TGT is issued. The user will provide the session key to the KDC along with the TGT when requesting a service ticket.
- Privilege Attribute Certificate (PAC) - The PAC holds all of the user's relevant information, it is sent along with the TGT to the KDC to be signed by the Target LT Key and the KDC LT Key in order to validate the user.
## Ticket Granting Ticket Contents
- ![alt text](https://i.imgur.com/QFeXDN0.png)
## Service Ticket Contents 
- ![alt text](https://i.imgur.com/kUqrVBa.png)
## Kerberos Authentication Overview
- ![alt text](https://i.imgur.com/VRr2B6w.png)
### Kerberos Tickets Overview
- The main ticket that you will see is a ticket-granting ticket these can come in various forms such as a .kirbi for Rubeus .ccache for Impacket. 
- The main ticket that you will see is a .kirbi ticket. A ticket is typically base64 encoded and can be used for various attacks.
## Attack Privilege Requirements
- Kerbrute Enumeration - No domain access required 
- Pass the Ticket - Access as a user to the domain required
- Kerberoasting - Access as any user required
- AS-REP Roasting - Access as any user required
- Golden Ticket - Full domain compromise (domain admin) required 
- Silver Ticket - Service hash required 
- Skeleton Key - Full domain compromise (domain admin) required
## Enumeration with Kerbrute
- Add the domain name to `/etc/hosts`
### Abusing Pre-Authentication Overview -
- By brute-forcing Kerberos pre-authentication, you do not trigger the account failed to log on event which can throw up red flags to blue teams. 
- When brute-forcing through Kerberos you can brute-force by only sending a single UDP frame to the KDC allowing you to enumerate the users on the domain from a wordlist.
### Kerbrute Installation
- Download a precompiled binary for your OS - https://github.com/ropnop/kerbrute/releases
- Rename kerbrute_linux_amd64 to kerbrute
- `chmod +x kerbrute` - make kerbrute executable
### Enumerating Users w/ Kerbrute -
- Enumerating users allows you to know which user accounts are on the target domain and which accounts could potentially be used to access the network.
- `cd` into the directory that you put `Kerbrute`
- Download the wordlist to enumerate with (in this repo)
````
./kerbrute userenum --dc CONTROLLER.local -d CONTROLLER.local User.txt 
````
- This will brute force user accounts from a domain controller using a supplied wordlist
- ![1](https://user-images.githubusercontent.com/75596877/130246484-1b4fdb60-eb89-441b-b0c7-c1b06277c074.png)






















































