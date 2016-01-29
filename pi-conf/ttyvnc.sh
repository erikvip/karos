#!/bin/bash

# Startup linuxvnc in a tmux/screen session to allow VNC access to /dev/tty1

# We also startup framebuffervnc to allow access to the framebuffer session at /dev/fb0
# Note that framebuffer takes no input...it just lets you see the screen remotely

# Check if existing 'vnc' session is present, and kill it first
tmux has-session -t vnc 2> /dev/null && tmux kill-session -t vnc;

# Kill any ghost vnc sessions
sudo pkill --full linuxvnc
sudo pkill --full x11vnc

tmux new -d -n vnc -s vnc "/usr/bin/sudo /usr/bin/linuxvnc 1"\; \
	set-option remain-on-exit on \; \
	split-window "/bin/bash -c -- 'while [ 1 == 1 ]; do /usr/bin/sudo /usr/bin/x11vnc -reopen -display :0 -rfbauth /etc/vncpasswd -auth /home/pi/.Xauthority; sleep 2; done;'; /bin/bash" \
	> /dev/null; 



