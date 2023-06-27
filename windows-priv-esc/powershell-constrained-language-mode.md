# Powershell Constrained Language Mode

* Enumerate which language mode powershell is currently in&#x20;

```
$ExecutionContext.SessionState.LanguageMode
```

* Attempt to change from constrained language mode to full language mode&#x20;

```
$ExecutionContext.SessionState.LanguageMode=[System.Management.Automation.PSLanguageMode]::FullLanguage
```
