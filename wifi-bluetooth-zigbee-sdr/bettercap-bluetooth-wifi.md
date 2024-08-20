# Bettercap Bluetooth / Wifi

* Bettercap is an excellent tool for Bluetooth and Wifi assessments.

### Wifi Recon

* make sure your interface is in monitor mode.

```
bettercap -iface wlan0
>>> wifi.recon on 
```

* see captured networks&#x20;

```
wifi.show
```

### PMKID Capture&#x20;

* attempt to associate to all APs attempting to capture PMKID (first EAPOL frame)

```
sudo bettercap -iface wlan0mon 
wifi.recon on 
# wait to locate APs
wifi.show
wifi.assoc all
```
