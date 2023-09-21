---
description: Collection of tips and tricks from myself and others!
---

# Hacknetics

Git-Book of this Repo:

* [<mark style="color:yellow;">https://ice-wzl.gitbook.io/hacknetics/</mark>](https://ice-wzl.gitbook.io/oscp-prep/)

### Red Team Quality of Life Scripts

#### Clipboard monitor&#x20;

* Never be unsure of what is in your clipboard buffer again

{% file src=".gitbook/assets/clip (1).py" %}

```
//create small window and run with
python3 clip.py
```

<figure><img src=".gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

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



{% file src=".gitbook/assets/config (2).txt" %}

### Tmux Config&#x20;

* tThis is the tmux config I am using these days&#x20;

```
mkdir -p ~/.config/tmux
#place both these files in your ~/.config/tmux directory 
#change the .local file, do not make changes to the .conf file 
```



{% file src=".gitbook/assets/tmux.conf.local" %}

###

{% file src=".gitbook/assets/tmux.conf" %}

### Big Thanks to our Sponsors

<img src=".gitbook/assets/qmaPi6hK_400x400.jpg" alt="" data-size="original"><img src=".gitbook/assets/tp-blog-1864x980-10 (2).png" alt="" data-size="original">
