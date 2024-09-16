# gqrx

### Overview&#x20;

* multi-platform, open source SDR application&#x20;
* install on linux

```
sudo apt install gqrx
```

* Shows waterfall display as well as FFT display. Easier to detect signal transmission
* Easy to record samples to disk&#x20;

### FM Radio

* launch with&#x20;

```
gqrx --edit
# select the correct device
```

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

* in my case im using a RTL device so i select that one
* ensure you tune to the right frequency (remember its in kHZ not MHZ)
* select WFM (stereo)
* Can see the red in the waterfall display meaning there is a strong signal present&#x20;

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

* can bookmark frequency for easy return finding in the future&#x20;
