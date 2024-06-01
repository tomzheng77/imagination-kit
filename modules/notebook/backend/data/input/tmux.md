# Tmux Configuration
- https://www.youtube.com/watch?v=DzNmUNvnB04
- https://tmuxcheatsheet.com/
- https://github.com/tmux-plugins/tpm/issues/67
- https://github.com/dreamsofcode-io/tmux/blob/main/tmux.conf
- https://github.com/catppuccin/Terminal.app
- https://github.com/epk/SF-Mono-Nerd-Font
- may need to restart tmux entirely (kill current sessions)

### Tmux Package Manager Setup
- `git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm`
- `vim ~/.config/tmux/tmux.conf`
  - change the contents to Appendix A
- `tmux source ~/.config/tmux/tmux.conf`
- <prefix> + I to install plugins
- Mac OS: disable settings > keyboard
  - so then Ctrl+Space doesn't change the language

### Appendix A
```
# Set true color
set-option -sa terminal-overrides ",xterm*:Tc"

# Enable mouse support
set -g mouse on

# Start windows and panes at 1, not 0
set -g base-index 1
set -g pane-base-index 1
set-window-option -g pane-base-index 1
set-option -g renumber-windows on

# Open panes in current directory
bind '"' split-window -v -c '#{pane_current_path}'
bind % split-window -h -c "#{pane_current_path}"

# Set prefix
unbind C-b
set -g prefix C-Space
bind C-Space send-prefix

# Vim style pane selection
bind h select-pane -L
bind j select-pane -D 
bind k select-pane -U
bind l select-pane -R

# TODO: Fix on Mac OS
# bind -n C-H previous-window
# bind -n C-L next-window

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'christoomey/vim-tmux-navigator'

# TODO: Fix on Mac OS
# set -g @catppuccin_flavour 'latte'
# set -g @plugin 'catppuccin/tmux'

# Is needed for Mac OS
set-environment -g PATH "/opt/homebrew/bin:/usr/local/bin:/bin:/usr/bin"
run '~/.tmux/plugins/tpm/tpm'
```

### Tmux Concepts
- sessions
- windows
- panes
