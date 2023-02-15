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

    <figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>
*
