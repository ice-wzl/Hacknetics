# Wifi Overview

* Uses 802.11 standard&#x20;

### To DS / From DS

* To DS is FROM client TO AP
* From DS is FROM AP TO client

```
FROM DS 
AP ----------------> CLIENT
MAC Addresses: BSSID, SOURCE, DST

TO DS
AP <---------------- CLIENT
MAC Addresses: BSSID, SOURCE DST
```

### Common Packet Types&#x20;

* Association Request - Request to join a WLAN -> subtype of 0
* Authentication Request - Request authentication to WLAN -> subtype of 11&#x20;
* Probe Request -> STA looking for known WLANs (How "Connect Automatically works) -> subtype 4&#x20;
* Deauthentication request -> Disconnect Request -> subtype 12&#x20;
* Beacon Frame ->  AP beacon to advertise ssid and AP capabilities -> subtype 8

### Linux Monitor Mode configuration&#x20;

* `iw` creates and manages wireless interfaces&#x20;
* `ip` configures and ip and the up or down state&#x20;

```
iw dev wlan0 interface add wlan0mon type monitor 
ip link set wlan0mon up 
iw dev wlan0mon set channel 1 
iw dev wlan0mon info

# to delete interface 
iw dev wlan0mon del
```

### Airmon-ng Monitor Mode configuration&#x20;

* use the shell script with aircrack-ng&#x20;
* Does not deal with deleting interfaces

```
# see detected interfaces
airmon-ng

# place in monitor mode 
airmon-ng start wlan0 

# delete interfaces
iw dev wlan0 del
```

### Types of WIFI networks&#x20;

* IEEE 802.11b or 802.11g -> 20MHz channels at 2.4 GHz
* IEEE 802.11a -> 20MHz channels at 5 GHz
* IEEE 802.11n -> 20MHz or 40MHz channels at 2.4 GHz or 5 GHz
* IEEE 802.11ac -> 20MHz, 40MHz, 60MHz, 80MHz, 160MHz channels at 5 GHz
* IEEE 802.11ax -> 20MHz, 40MHz, 60MHz, 80MHz, 160MHz channels at 2.4 GHz or 5GHz

### Controlling Channel and Width

```
iw dev wlan0mon info | grep type
    type monitor
iw dev wlan0mon set channel 1 
iw dev wlan0mon set channel 132
iw dev wlan0mon info | grep channel
    channel 132 (5660 MHz), width: 20 MHz (no HT), center1: 5660 MHz
    
iw dev wlan0mon set channel 132 HT40+
iw dev wlan0mon info | grep channel 
    channel 132 (5660 MHz), width: 20 MHz (no HT), center1: 5670 MHz
iw dev wlan0man set channel HT40-
    channel 132 (5660 MHz), width: 20 MHz (no HT), center1: 5650 MHz
```
