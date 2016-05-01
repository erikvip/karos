# FAQ - Questions and Answers for random things

### Gathering touch screen events

Just run **evtest** to see touch screen events.  You may also **cat /dev/input/event0** to see touch event coordinates. 

### Access the console via VNC

**linuxvnc** will let you share your tty consoles in text mode.  It is part of the *x11vnc* suite, so just apt-get install it, then run:

    sudo linuxvnc 1

Where 1 is the /dev/tty# you wish to share. 

Note that this will not handle the X display, if you wish to share your X sessions via vnc, use **Xvnc** from the *tightvncserver* package: 

- apt-get install tightvncserver
- vncpasswd /etc/vncpasswd
- Run this command to launch vnc (after X11 is running):

    sudo /usr/bin/x11vnc -reopen -display :0 -rfbauth /etc/vncpasswd -auth /home/pi/.Xauthority


I like to keep these vnc services running all the time, so here is a wrapper script using **tmux**, which can be added to */etc/rc.local* to run on startup. Save this as */home/pi/bin/ttyvnc.sh*:

    #!/bin/bash

    # Check if existing 'vnc' session is present, and kill it first
    tmux has-session -t vnc 2> /dev/null && tmux kill-session -t vnc;

    # Kill any ghost vnc sessions
    sudo pkill --full linuxvnc
    sudo pkill --full x11vnc

    # Startup a tmux session, run linuxvnc, x11vnc, and then detach tmux
    tmux new -d -n vnc -s vnc "/usr/bin/sudo /usr/bin/linuxvnc 1"\; \
        set-option remain-on-exit on \; \
        split-window "/bin/bash -c -- 'while [ 1 == 1 ]; do /usr/bin/sudo /usr/bin/x11vnc -reopen -display :0 -rfbauth /etc/vncpasswd -auth /home/pi/.Xauthority; sleep 2; done;'; /bin/bash" \
        > /dev/null;

Remember to chmod +x the script, and then throw it into */etc/rc.local*

    /home/pi/bin/ttyvnc.sh

### ListView is partially blank

When scrolling through the ListView in Kivy, labels may suddenly break after a certain point. 
This issue was observed on a Raspberry PI when gpu_mem was set to 64MB.  It does not matter if you're running inside X11 or straight through the framebuffer via python/pygame. My list (for the musicplayer) would not show any labels for the list items after about 72.  

Increasing gpu_mem to 128 fixed the issue. 

Testing script under gui/src/testing/listview_longlist.py

## Useful links

http://www.engineering-diy.blogspot.ro/2015/03/raspberry-pi-2-carpc.html
http://xistechnical.blogspot.com/2014/06/raspberry-pi-carputer-project.html
https://kivy.org/docs/
https://github.com/notandy/ympd
http://www.dimrobotics.com/2013/06/olinuxino-a13-touchscreen-support-in.html
https://en.wikipedia.org/wiki/Uzbl
https://github.com/elalemanyo/raspberry-pi-kiosk-screen
http://ozzmaker.com/matchbox-desktop-raspberry-pi/
https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=105755

