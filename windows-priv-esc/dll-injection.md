# DLL Injection & Hijacking

## DLL Injection Methods

### LoadLibrary
- Most common method
- Allocate memory in target process, write DLL path, create remote thread at LoadLibrary
```c
HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetProcessId);
LPVOID dllPathAddr = VirtualAllocEx(hProcess, NULL, strlen(dllPath), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE);
WriteProcessMemory(hProcess, dllPathAddr, dllPath, strlen(dllPath), NULL);
LPVOID loadLibAddr = (LPVOID)GetProcAddress(GetModuleHandle("kernel32.dll"), "LoadLibraryA");
CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)loadLibAddr, dllPathAddr, 0, NULL);
```

### Manual Mapping
- Manually load DLL sections into target process memory
- Avoids LoadLibrary detection by security tools
- Resolves imports and relocations manually

### Reflective DLL Injection
- DLL loads itself from memory using its own PE loader
- No filesystem artifacts
- Library implements ReflectiveLoader export function
- https://github.com/stephenfewer/ReflectiveDLLInjection

## DLL Hijacking

### DLL Search Order (Safe DLL Search Mode Enabled - Default)
1. Application directory
2. System directory (C:\Windows\System32)
3. 16-bit system directory
4. Windows directory
5. Current directory
6. PATH environment variable directories

### DLL Search Order (Safe DLL Search Mode Disabled)
1. Application directory
2. **Current directory** (moved up)
3. System directory
4. 16-bit system directory
5. Windows directory
6. PATH directories

### Finding Hijackable DLLs
- Use **Process Monitor (procmon)** to filter for `Load Image` operations or `NAME NOT FOUND` results
- Use **Process Explorer** to view loaded DLLs per process

### DLL Proxying
- Rename original `library.dll` to `library.o.dll`
- Create malicious `library.dll` that loads functions from `library.o.dll`, tampers, and returns
- Application uses malicious DLL transparently

### Invalid/Missing DLL Hijacking
- Find DLLs the application tries to load but can't find (`NAME NOT FOUND` in procmon)
- Place a malicious DLL with that name in the application directory
- DLL will execute `DllMain` when loaded

### Safe DLL Search Mode Registry
```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\SafeDllSearchMode
```
- Value 1 = enabled (default), Value 0 = disabled
