# Touchscreen setup

Setup framebuffer dimensions and disable overscan.  Use hdmi_mode 87 for the 800x480 display, and enable SPi. 

## RPi config.txt

This is my working /boot/config.txt file for the ads7846 touchscreen:   

```
    # Framebuffer width/ height
    framebuffer_width=800
    framebuffer_height=480

    # Audio through mic/aux jack 
    dtparam=audio=on

    # Screen lines up nicely, no need for overscan
    disable_overscan=1

    # GPU
    #gpu_mem=64

    # Issue with Kivy - ListView won't do more than 72 items with only 64MB of gpu_mem...
    gpu_mem=128

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

```

Once your config.txt file is setup, you should now have a working LCD! But we still need to calibrate and configure the touchscreen input driver. 

## /dev/input/touchscreen udev setup

With just the touchscreen connected (no keyboard / mouse), the touchscreen input device is created as */dev/input/event0*

However, if you connect a keyboard/mouse, they will take precedence and become event0 and event1, while the touchscreen driver runs last and it becomes event2. The udev rule below will create a symlink to /dev/input/touchscreen, linked to whichever input matches the ADS7846 driver. 

You must also configure the touchscreen device in Kivy's config.ini. See [[Kivy]] for more info. 

Create a new file called **95-ads7846.rules** under **/etc/udev/rules.d/**

**/etc/udev/rules.d/95-ads7846.rules**   
```
  SUBSYSTEM=="input", KERNEL=="event[0-9]*", ATTRS{name}=="ADS7846*", SYMLINK+="input/touchscreen"
```

After creating this file, you'll need to reboot to take effect.  Afterwards, /dev/input/touchscreen will always be symlinked during boot to the touchscreen device.

## TSLIB

As noted above, tslib is deprecated, and I couldn't get it working outside of the test programs anyway.  But if you want to test it, install libts and run:    

    sudo TSLIB_FBDEVICE=/dev/fb0 TSLIB_TSDEVICE=/dev/input/event0 ts_calibrate

But it doesn't work under X11, and PyGame would never pick up the Y axis.

Instead use evdev ...


## Evdev / X11 configuration

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
