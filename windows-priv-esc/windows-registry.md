# Windows Registry 
## Folder/predefined key	
### `HKEY_CURRENT_USER`	
- Contains the root of the configuration information for the user who is currently logged on. 
- The user's folders, screen colors, and Control Panel settings are stored here. This information is associated with the user's profile. 
- This key is sometimes abbreviated as `HKCU`.
### `HKEY_USERS` 
- Contains all the actively loaded user profiles on the computer. `HKEY_CURRENT_USER` is a subkey of `HKEY_USERS`. `HKEY_USERS` is sometimes abbreviated as `HKU`.
### `HKEY_LOCAL_MACHINE`	
- Contains configuration information particular to the computer (for any user). This key is sometimes abbreviated as `HKLM`.
### `HKEY_CLASSES_ROOT`	
- Is a subkey of `HKEY_LOCAL_MACHINE\Software`. The information that is stored here makes sure that the correct program opens when you open a file by using Windows Explorer. 
- This key is sometimes abbreviated as `HKCR`.
- Starting with Windows 2000, this information is stored under both the `HKEY_LOCAL_MACHINE` and `HKEY_CURRENT_USER` keys. The `HKEY_LOCAL_MACHINE\Software\Classes` key contains default settings that can apply to all users on the local computer. 
- The `HKEY_CURRENT_USER\Software\Classes` key has settings that override the default settings and apply only to the interactive user.
- The `HKEY_CLASSES_ROOT` key provides a view of the registry that merges the information from these two sources. 
- `HKEY_CLASSES_ROOT` also provides this merged view for programs that are designed for earlier versions of Windows. 
- To change the settings for the interactive user, changes must be made under `HKEY_CURRENT_USER\Software\Classes` instead of under HKEY_CLASSES_ROOT.
- To change the default settings, changes must be made under `HKEY_LOCAL_MACHINE\Software\Classes` .If you write keys to a key under `HKEY_CLASSES_ROOT`, the system stores the information under `HKEY_LOCAL_MACHINE\Software\Classes`.
- If you write values to a key under `HKEY_CLASSES_ROOT`, and the key already exists under `HKEY_CURRENT_USER\Software\Classes`, the system will store the information there instead of under `HKEY_LOCAL_MACHINE\Software\Classes`.
### `HKEY_CURRENT_CONFIG` 
-	Contains information about the hardware profile that is used by the local computer at system startup.















































