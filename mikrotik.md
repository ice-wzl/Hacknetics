# Mikrotik

## Supout Decoder

## What is supout.rif file? <a href="#supout.rif-whatissupout.riffile" id="supout.rif-whatissupout.riffile"></a>

The support file is used for debugging MikroTik RouterOS and to solve the support questions faster. All MikroTik Router information is saved in a binary file, which is stored in the router and can be downloaded from the router using FTP or WinBox. If required, then you can generate the file on the "/flash" folder on devices with FLASH type memory or external storage drive, by specifying the full path to the file "name=flash/supout.rif". You can view the contents of this file in your [Mikrotik account](https://www.mikrotik.com/), simply click on "Supout.rif viewer" located in the left column and upload the file.

* Generate one from the web port or Winbox by scrolling all the way down on the left hand menu
* Click on `Make Supout.rif`
* The file will appear in the `Files`menu of the web dashboard or Winbox, download it

### Decoding Supout.rif

* [https://github.com/farseeker/go-mikrotik-rif](https://github.com/farseeker/go-mikrotik-rif)

```
git clone https://github.com/farseeker/go-mikrotik-rif
cd go-mikrotik-rif
go build main.go

main /path/to/supout.rif
```
