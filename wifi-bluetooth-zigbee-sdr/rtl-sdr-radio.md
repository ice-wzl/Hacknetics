# RTL-SDR Radio

### Disclaimer

* Please do not transmit anything on a frequency you are unlicensed or unauthorized to transmit on. I am not responsible for your actions.

### Find Frequencies&#x20;

[https://www.radioreference.com/db/browse/ctid/1212](https://www.radioreference.com/db/browse/ctid/1212)

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

```
#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <frequency>"
    echo "Example: $0 101.1M"
    exit 1
fi

frequency=$1

# Run rtl_fm with the specified frequency
rtl_fm -f "$frequency" -M wbfm -s 200k -r 48000 - | aplay -r 48000 -f S16_LE

```

* Example usage, this is the frequency for NOAA in Baltimore, MD

```
./fmradio.sh 162.40M
Found 1 device(s):
  0:  Realtek, RTL2838UHIDIR, SN: 00000001

Using device 0: Generic RTL2832U OEM
Found Rafael Micro R820T tuner
Tuner gain set to automatic.
Tuned to 162716000 Hz.
Oversampling input by: 6x.
Oversampling output by: 1x.
Buffer size: 6.83ms
Allocating 15 zero-copy buffers
Sampling at 1200000 S/s.
Output at 200000 Hz.
Playing raw data 'stdin' : Signed 16 bit Little Endian, Rate 48000 Hz, Mono
underrun!!! (at least 327.957 ms long)
```

### Fun Frequencies&#x20;

* Baltimore City Fire Dispatch

```
./fmradio.sh 46.460M
```

* NOAA Baltimore&#x20;

```
./fmradio.sh 162.40M
```
