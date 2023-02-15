---
description: Page Under Construction
---

# WMI Persist With Event Filters

* There are many great automated ways to do this.
* [https://github.com/Sw4mpf0x/PowerLurk](https://github.com/Sw4mpf0x/PowerLurk)

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
$x='Our Filter'
$x=
$z='Our Consumer'
```

#### Now create the triggering event&#x20;



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
