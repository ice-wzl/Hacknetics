<p class="has-line-data" data-line-start="0" data-line-end="1">Meterpreter commands</p>
<p class="has-line-data" data-line-start="2" data-line-end="3">Core commands will be helpful to navigate and interact with the target system. Below are some of the most commonly used. Remember to check all available commands running the help command once a Meterpreter session has started.</p>
<p class="has-line-data" data-line-start="4" data-line-end="16">Core commands<br>
background: Backgrounds the current session<br>
exit: Terminate the Meterpreter session<br>
guid: Get the session GUID (Globally Unique Identifier)<br>
help: Displays the help menu<br>
info: Displays information about a Post module<br>
irb: Opens an interactive Ruby shell on the current session<br>
load: Loads one or more Meterpreter extensions<br>
migrate: Allows you to migrate Meterpreter to another process<br>
run: Executes a Meterpreter script or Post module<br>
sessions: Quickly switch to another session<br>
File system commands</p>
<p class="has-line-data" data-line-start="17" data-line-end="27">cd: Will change directory<br>
ls: Will list files in the current directory (dir will also work)<br>
pwd: Prints the current working directory<br>
edit: will allow you to edit a file<br>
cat: Will show the contents of a file to the screen<br>
rm: Will delete the specified file<br>
search: Will search for files<br>
upload: Will upload a file or directory<br>
download: Will download a file or directory<br>
Networking commands</p>
<p class="has-line-data" data-line-start="28" data-line-end="34">arp: Displays the host ARP (Address Resolution Protocol) cache<br>
ifconfig: Displays network interfaces available on the target system<br>
netstat: Displays the network connections<br>
portfwd: Forwards a local port to a remote service<br>
route: Allows you to view and modify the routing table<br>
System commands</p>
<p class="has-line-data" data-line-start="35" data-line-end="47">clearev: Clears the event logs<br>
execute: Executes a command<br>
getpid: Shows the current process identifier<br>
getuid: Shows the user that Meterpreter is running as<br>
kill: Terminates a process<br>
pkill: Terminates processes by name<br>
ps: Lists running processes<br>
reboot: Reboots the remote computer<br>
shell: Drops into a system command shell<br>
shutdown: Shuts down the remote computer<br>
sysinfo: Gets information about the remote system, such as OS<br>
Others Commands (these will be listed under different menu categories in the help menu)</p>
<p class="has-line-data" data-line-start="48" data-line-end="62">idletime: Returns the number of seconds the remote user has been idle<br>
keyscan_dump: Dumps the keystroke buffer<br>
keyscan_start: Starts capturing keystrokes<br>
keyscan_stop: Stops capturing keystrokes<br>
screenshare: Allows you to watch the remote user’s desktop in real time<br>
screenshot: Grabs a screenshot of the interactive desktop<br>
record_mic: Records audio from the default microphone for X seconds<br>
webcam_chat: Starts a video chat<br>
webcam_list: Lists webcams<br>
webcam_snap: Takes a snapshot from the specified webcam<br>
webcam_stream: Plays a video stream from the specified webcam<br>
getsystem: Attempts to elevate your privilege to that of local system<br>
hashdump: Dumps the contents of the SAM database<br>
Although all these commands may seem available under the help menu, they may not all work. For example, the target system might not have a webcam, or it can be running on a virtual machine without a proper desktop environment.</p>
