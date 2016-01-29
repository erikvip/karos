# Raspberry PI Car PC Setup

## Overview   

The main goal of this project is to provide an touch screen mp3 player for my vehicle using a Raspberry PI.  Also looking to add MTP support so Android (iphone?) phones can be played directly by passengers. 

The main goal is just as a media player, but will hopefully add additional features once the main goal is working well. 


### Feature overview and wishlist

- mp3 playback via mpd
- MTP support for playing directly over phones
- Copy over MTP so I can copy my passenger's music and/or files
- Movie / video support
- Youtube streaming / direct download & save UI. Maybe soundcloud too...
- Web browser
- Music visualization / spectrum eye candy
- NavIt navigation software and/or mapping interface
- Audiobook support / fine tuned mp3 handling for audiobook
- Automatic media syncing over WIFI when home
- Toggling RPi On/Off based on Stereo Deck Remote Lead / Engine Status...

** In the far far future: **    

- Bluetooth support
- GPS module integration
- Backup camera (Dash camera?) module
- ODB support to display engine diagnostics / speed
- AM/FM Radio integration


### What not to do (Deprecation)   

When I first started looking at this project, it seemed like PyGame would fit the bill, and since I hadn't worked with an RPi touchscreen before, I just found one on Amazon that also came with a case.  I purchased the 5" HDMI LCD Touch screen:

http://www.amazon.com/gp/product/B00U21UA16?colid=3DDQ5WN4Z8JOE&coliid=I1X9PBTUCQ8EEK&ref_=wl_it_dp_o_pC_nS_ttl

Which I guess is sold by XYG-Study? Honestly I'm still not sure who the manufacturer of this screen is, but I haven't been super impressed with it...I did get it working, but on my next LCD project, I'm thinking the Official Raspberry PI LCD screen would have better support. 

It came with very little info, and finding drivers or any information about it took some google-fu...Finally got it working via the ads7846 driver, which is natively supported on Raspbian.  The touch screen reports itself as a HID device (like a mouse) though, so Gestures didn't work quite as expected...in researching it appears the official RPi touch screen handles input better than just emulating a mouse HID. 

See the [[Touchscreen]] section below for information on configuration. 

In sort, this is the software that **didn't** work well enough for me:

- **libts** - Apparently this was the official Linux touch screen driver for some time, and there's a lot of info on the web.  But it is no longer actively maintained and has been superseded by *evdev*.  It was useful to install just to confirm ts_calibrate and ts_test were working properly, but nothing else worked...X11 did not identify the device at all. And PyGame / SDL did identify it, but wouldn't pick up the X-axis properly (it was always 0).  After playing with it for some time, I found **evdev** has much better support. So don't use libts...
- **PyGame** - May be useful if you're writing a game, but doesn't have many UI widgets available, and gestures are non-existent. 
- **LXDE / Gnome** - No gesture support & doesn't play nice with the touch screen. 
- **Kodi / XBMC** - Did not work with the ads7846 HID...didn't seem to like it pretending to be a mouse or something. I never got it working, and the interface was too sluggish anyway. 
- **Chromium in Kiosk mode or Firefox** This was the best route I'd found, but Scrolling / Gestures didn't have any native support (Firefox maybe...) and a lot of interface handling would have to be done via Javascript. Also no clear way to use an onscreen keyboard. 


### Final Solution

Finally I found Kivy.  A very nice UI toolkit for building mobile / touch screen devices.  It works on RPi, but had to be compiled manually (The apt-get package had some issue I don't recall now...).  But a great tool for building touch interfaces, many widgets available, advanced scroll and gesture support that *just work*. 

- **Matchbox Window Manager** - This could be the main solution, as it's purpose built for touch screens, and has some native gesture support.  It also wraps existing Linux applications, so existing software runs under this window manager.  But it's still rather new.  I'm planning on still using the Matchbox Window Manager for running any 3rd party applications (web browser) that won't be handled via Kivy. 

 
## LCD / Touchscreen configuration

Setup framebuffer dimensions and disable overscan.  Use hdmi_mode 87 for the 800x480 display, and enable SPi. 

### RPi config.txt

This is my working /boot/config.txt file for the ads7846 touchscreen:

    # Framebuffer width/ height
    framebuffer_width=800
    framebuffer_height=480

    # Audio through mic/aux jack 
    dtparam=audio=on

    # Screen lines up nicely, no need for overscan
    disable_overscan=1

    # GPU
    gpu_mem=64

    # Uhm...I'm not sure...
    framebuffer_ignore_alpha=1
    framebuffer_swap=1
    init_uart_clock=16000000

    # HDMI setup for 800x480@60hz
    hdmi_group=2
    hdmi_mode=87
    hdmi_force_hotplug=1
    hdmi_cvt=800 480 60

    # Increase HDMI signal (I don't think this is really necessary...)
    config_hdmi_boost=4

    # Enable SPi and i2c...
    dtparam=spi=on
    dtparam=i2c_arm=on

    # This is the ads7846 configuration. If you want to run it in a Portrait mode instead of Landscape, change swapxy to 1
    # From: https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=105755
    dtoverlay=ads7846, cs=1 speed=50000 penirq=25, penirq_pull=2, swapxy=0, xmin=200, ymin=200, xmax=3900, ymax=3900, pmin=0, pmax=155, xohms=150

    # err...I dunno if I really need this or not...
    dtoverlay=w1-gpio-pullup,gpiopin=4,extpullup=1

    # Increase amperage available to USB devices (from 600ma (default) to 1.2a).  I only did this in hopes to support large external HDD's being powered through USB (it didn't work). Also may be useful for charging phones connected via USB to the RPi
    max_usb_current=1


Once your config.txt file is setup, you should now have a working LCD! But we still need to calibrate and configure the touchscreen input driver. 

### TSLIB

As noted above, tslib is deprecated, and I couldn't get it working outside of the test programs anyway.  But if you want to test it, install libts and run:    

    sudo TSLIB_FBDEVICE=/dev/fb0 TSLIB_TSDEVICE=/dev/input/event0 ts_calibrate

But it doesn't work under X11, and PyGame would never pick up the Y axis.

Instead use evdev ...


### Evdev / X11 configuration

Install these packages:

    apt-get install xserver-xorg-input-evdev xserver-xorg-input-evdev-dev python-evdev xinput-calibrator

Calibration wasn't really necessary for my screen...but I did it anyway (and it was kind of a PITA). First need to run xinput-calibrator under an X11 session, and since I was running my RPi headless, I could only SSH into the system...this presented some challenges. 

* Launch xinput-calibrator via .xinitrc and log the output to a file. 
* Edit ~/.xinitrc (create it) and enter:   
 
    exec /usr/bin/xinput_calibrator --output-type xorg.conf.d -v 2> /home/pi/xinputerr.log 1> /home/pi/xinput.log

Now start X11 with the **startx** command. 

You'll be asked to click the screen a few times, then X kicks you back out.  Note for newcomers: your local .xinitrc overrides the system xinitrc, so if all you run is xinput_calibrator, then that's all X11 will do. If you wanted to e.g., get to a regular LXDE / X session after calibration, then include **/etc/X11/xinit/xinitrc** after the *exec* command. 

Now check your /home/pi/xinput.log file, it should spit out calibration config file like this:
    Section "InputClass"
        Identifier  "calibration"
        MatchProduct    "ADS7846 Touchscreen"
        Option  "Calibration"   "189 4002 225 3945"
        Option  "SwapAxes"  "0"
    EndSection

The **Calibration** numbers are what we really needed here.  Add **Driver "evdev"** to tell X to use the evdev driver.  And optional InvertX and InvertY parameters are available if you need them. 

Save this file as /usr/share/X11/xorg.conf.d/99-calibration.conf :    

    Section "InputClass"
        Identifier   "calibration"
        MatchProduct    "ADS7846 Touchscreen"
        Option  "Calibration"   "189 4002 225 3945"
        Option "SwapAxes" "no"
        Option "InvertY" "no"
        Option "InvertX" "no"
        Driver "evdev"
    EndSection

You should now have Touchscreen support in X11 (!). Make sure you have **/etc/X11/xinit/xinitrc** in your /home/pi/.xinitrc file (or just delete /home/pi/.xinitrc) and then run **startx**.  You can now click stuff on the screen! woohoo!


Likewise, if you wish to use PyGame, you can add a launcher via .xinitrc and launch the pygame script when X starts. Just remember to use the **evdev** driver, and **NOT tslib** in your Environment variables, or declare them in python directly:

    import os
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb0')
    os.putenv('SDL_MOUSE', '/dev/input/event0')
    os.putenv('SDL_MOUSEDEV', '/dev/input/event0')
    os.putenv('SDL_MOUSEDRV', 'evdev')

Touchscreen should be ready to go at this point.  The rest of this document details setting up the car interface, and various notes on the setup. 

## Questions and Answers for random things

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



## Useful links

http://www.engineering-diy.blogspot.ro/2015/03/raspberry-pi-2-carpc.html
http://xistechnical.blogspot.com/2014/06/raspberry-pi-carputer-project.html
https://kivy.org/docs/
https://github.com/notandy/ympd
http://www.dimrobotics.com/2013/06/olinuxino-a13-touchscreen-support-in.html
https://en.wikipedia.org/wiki/Uzbl
https://github.com/elalemanyo/raspberry-pi-kiosk-screen
http://ozzmaker.com/matchbox-desktop-raspberry-pi/