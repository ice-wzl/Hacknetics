# tmux

* If you ever get a weird error about netsted sessions, just unset the env var TMUX with&#x20;

```
TMUX=
```

## tmux Create New Session

```
tmux new-session -s <session name>
--OR--
tmux new -s <session name>
```

### tmux List existing session&#x20;

```
tmux list-sessions
```

### tmux Attatch Existing session&#x20;

```
tmux attatch-session -t <session-id/session-name>
```

### tmux Kill Existing session&#x20;

```
tmux kill-session -t <session-id/session-name>
```

### Delete all sessions except current&#x20;

```
tmux kill-session -a 
```

## Reverse History Search

* Press `Ctrl+R` and type what you are searching for, then hit enter when the command appears

## Pre-Fix Key

* By default it is `Ctrl+B`

## Create a New Window

```
Ctrl+b c
```

## Switch between windows

```
Ctrl+b [0-9]
--OR-- 
Ctrl+b right/left arrow keys 
```

* or to go one previous&#x20;

```
Ctrl+b p
```

* to go to next&#x20;

```
Ctrl+b n
```

### Detach Session&#x20;

```
Ctrl+b d
```

### Rename Window

```
Ctrl+b ,
```

### Move current pane left/right&#x20;

```
Ctrl+b { #move left 
Ctrl+b } #move right 
```

### Exit pane&#x20;

```
Ctrl+b x
```

### Resizing Panes&#x20;

```
#resize height 
Ctrl+b uparrow
Ctrl+b downarrow 
#resize width 
Ctrl+b leftarrow 
Ctrl+b rightarrow 
```

### Convert pane to window&#x20;

```
Ctrl+b ! 
```

## Nested tmux Sessions

* SSH into remote host
* Can run `tmux ls` and view the tmux sessions
* Example:

```
MINER: 1 windows (created Mon Novv 27 21:33:24 2022) [186x47]
```

* To attatch to that session

```
tmux attatch -t MINER
```

* Use prefix key + d to detatch from the connected session

## Split Terminals Vertical

* `Ctrl+B %`

## Split Terminals Horizontal

* `Ctrl+B "`



## Custom tmux config

* File located `~/.tmux`

```
set -g prefix C-a
bind C-a send-prefix
unbind C-b

#Quality of life stuff 
set -g history-limit 10000
set -g allow-rename off

#Join Windows
bind-key j commpand-prompt -p "join pane from:" "join-pane -s '%%'" 
bind-key -s command-prompt -p "send pane to:" "join-pane -t '%%'"

#search mode VI (default is emacs)
set-windows-option -g mode-keys vi

run-shell /opt/tmux-logging/logging.tmux
```
