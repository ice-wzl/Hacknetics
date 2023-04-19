---
description: Collection of tips and tricks from myself and others!
---

# OSCP-Prep

Git-Book of this Repo:

* [<mark style="color:yellow;">https://ice-wzl.gitbook.io/oscp-prep/</mark>](https://ice-wzl.gitbook.io/oscp-prep/)

### Red Team Quality of Life Scripts

#### Clipboard monitor&#x20;

* Never be unsure of what is in your clipboard buffer again

{% file src=".gitbook/assets/clip (1).py" %}

```
//create small window and run with
python3 clip.py
```

<figure><img src=".gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

#### Scripted Window

* Have you ever neglected to take notes on an important engagement, or forgotten to save off a key command?  scriptme.py will solve those issues.  Personally I much prefer this solution to the built in script command.

{% file src=".gitbook/assets/scriptme.py" %}

<figure><img src=".gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

### Terminator Config

* Note: systems have different fonts installed, if you use this config and the font spacing is wild, use the system default, or choose your own.

```
open terminal 
right click --> preferences --> profiles --> check the use system fixed width font
```

* These days I find myself using Terminator the most (and tmux), see below for my terminator config.
* To use it place this file at `~/.config/terminator/config`
* And make sure terminator is installed `sudo apt install terminator -y`
* Make sure to remove the .txt part when you pull the file down locally&#x20;

{% file src=".gitbook/assets/config.txt" %}

### Big Thanks to our Sponsors

<img src=".gitbook/assets/qmaPi6hK_400x400.jpg" alt="" data-size="original"><img src=".gitbook/assets/tp-blog-1864x980-10 (1).png" alt="" data-size="original">
