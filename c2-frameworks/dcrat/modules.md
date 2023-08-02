# Modules

* See below for each modules documentation&#x20;
* To get to modules right click a call back and you will see the following options

| Surveillance                          |
| ------------------------------------- |
| Remote Shell                          |
| Remote Screen                         |
| Remote Camera                         |
| Remote Regedit                        |
| File Manager                          |
| Process Manager                       |
| Netstat                               |
| Record                                |
| Program Notifications (Start \| Stop) |

### Remote Shell

* Exactly what it sounds like
* Click on the module wait for below to appear

```
Microsoft Windows [Version 10.0.20348.1787]
(c) Microsoft Corporation. All rights reserved.
```

* This is a `cmd.exe` prompt not a powershell prompt!
* Use the white bar at the bottom to execute commands&#x20;

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

### Remote Screen

* Also exactly what it sounds like
* View the remote screen of the remote system&#x20;
* It can take a second to load, please be patient.
* Screen sharing can be controlled (off/on) with the `Start` button at the top left&#x20;
* Option to `View only` or control the remote machine via your `mouse` and `keyboard`&#x20;
* To turn either on press the respective button at the top
*   Can also take auto screenshots with the `Camera` button also at the top &#x20;

    * By default it will capture the screen every \~3 seconds
    * IMO that is far too fast, I am working on tuning it to roughly every 30 seconds to drop the amount of network traffic that is required with the screenshots.



    <figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

### Remote Camera

* View the remote systems webcam
* Requires loading `RemoteCamera.dll` into memory which will happen automatically
* If no camera if found the pop up will exit automatically&#x20;

### Remote Regedit

* Remotely view the registry in addition to creation of new keys or modification of existing keys&#x20;

<figure><img src="../../.gitbook/assets/image (6) (2).png" alt=""><figcaption></figcaption></figure>

* To create a new key click on `Edit` at the top and follow the prompts
* It is nearly identical to the normal `Regedit` program on Windows

### File Manager&#x20;

* File manager for remote upload, download, compressing and general file manager options
* Just point and click
* To move up a directory after traversing down the file system ensure you `Right Click --> Back`
  * That took me longer to figure out than I care to admit pubically

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

* When you download a file a `ClientsFolder` will get created, you can find your exfil'ed file there

```
DcRat\Binaries\Debug\ClientsFolder\1427F5A9B444217138E1 #String is client id
```

### Process Manager&#x20;

* Exactly like it sounds
* View running process
* Right Click to `Refresh` or `Kill` a specific process
* Refreshes pulls a up to date process list
* It is better opsec to not constantly upload as that can greatly increate the amount of network traffic

<figure><img src="../../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>

### Netstat

* Exactly like it sounds
* View network connection on the remote host
* `Right Click` and select `Refresh` or `Kill`&#x20;
* Selecting `Kill` attempts to kill the process creating that network connection

<figure><img src="../../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

### Record&#x20;

* Record the audio off the remote systems microphone&#x20;

<figure><img src="../../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

* If the remote system has no microphone you will get an error in the logs&#x20;

<figure><img src="../../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>

* Requires the `Audio.dll` file to be automatically loaded onto the remote systems memory&#x20;

### Program Notification

* Alert the operator when a specific remote process is launched on the system
* Defaults to `Uplay,QQ,Chrome,Edge,Word,Excel,PowerPoint,Epic,Steam`
* Currently changed to:

```
Chrome,Edge,Firefox,Word,Excel,PowerPoint,Task Manager
```

<figure><img src="../../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

| Control          |          |                   |                     |
| ---------------- | -------- | ----------------- | ------------------- |
| Send File -->    | From URL | Send File to Disk | Send File to Memory |
| Run Shellcode    |          |                   |                     |
| Message Box      |          |                   |                     |
| Chat             |          |                   |                     |
| Visit Website    |          |                   |                     |
| Change Wallpaper |          |                   |                     |
| Keylogger        |          |                   |                     |
| File Search      |          |                   |                     |

### Send File



### Run Shellcode



### MessageBox



### Chat&#x20;



### Visit Website



### Change Wallpaper



### Keylogger



### File Search

| Malware           |         |         |
| ----------------- | ------- | ------- |
| DDOS              |         |         |
| Ransomware -->    | Encrypt | Decrypt |
| Disable WD        |         |         |
| Password Recovery |         |         |
| Disable UAC       |         |         |

### DDOS



### Ransomware



### Disable WD



### Password Recovery



### Disable UAC



\-- All modules not currently listed yet

