# RTL-SDR Radio

### Install Dependencies

* I am using an RTL-SDR V3&#x20;
* `sudo apt-get install gqrx-sdr rtl-sdr`

### FM Radio

* Tune to your correct frequency&#x20;

```
rtl_fm -f 101.1M -M wbfm -s 200k -r 48000 - | aplay -r 48000 -f S16_LE
```

* **`-f 101.1M`:** Set the frequency to 101.1 MHz.
* **`-M wbfm`:** Set the mode to wideband FM.
* **`-s 200k`:** Set the sample rate to 200 kHz.
* **`-r 48000`:** Resample to 48 kHz, which is standard for audio playback.
* **`aplay -r 48000 -f S16_LE`:** Play the audio using the ALSA player (`aplay`).

### FM Radio Wrapper Script

