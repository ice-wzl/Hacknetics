# tmux
## tmux Create New Session
````
tmux new -s name-of-session
````
## Reverse History Search 
- Press `Ctrl+R` and type what you are searching for, then hit enter when the command appears 
## Pre-Fix Key 
- By default it is `Ctrl+B`
## Create a New Window 
- `Ctrl+B C`
## Switch Back to First Window 
- `Ctrl+B 0`
### Switch to Bash 
- Prefix Key + 1
## Nested tmux Sessions
- SSH into remote host 
- Can run `tmux ls` and view the tmux sessions 
- Example:
````
MINER: 1 windows (created Mon Novv 27 21:33:24 2022) [186x47]
````
- To attatch to that session 
````
tmux attatch -t MINER
````
- Use prefix key + d to detatch from the connected session 
## Split Terminals Vertical 
- `Ctrl+B %`
## Split Terminals Horizontal 
- `Ctrl+B "`

## Send Current Pane to another session 
## Custom tmux config 
- File located `~/.tmux`
````
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
````

































