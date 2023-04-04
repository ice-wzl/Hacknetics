# Powershell Constrained Language Mode

* Attempt to change from constrained language mode to full language mode&#x20;

```
$ExecutionContext.SessionState.LanguageMode=[System.Management.Automation.PSLanguageMode]::FullLanguage
```
