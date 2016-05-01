# Kivy

Notes on Kivy implementation and design

## Good Example files   

- demo/kivycatalog/main.py
- demo/showcase/main.py
- keyboard/main.py
- settings/main.py
- widgets/effectwidget3_advanced.py

## Kivy Garden
- **navigationdrawer** Used for the playing / volume config screen
- **recycleview** Replacement for ListView - see [Known Isssues] below.

### NavigationDrawer Enhancements

I updated NavigationDrawer to support docking on Top/Bottom/Right instead of just left.  Still has some issues with right docking / main under. 

But after doing so...I realized someone had already submitted a pull request to thje NavigationDrawer repo for the same feature! 

Hmmm...I was going to submit my own, but maintainer doesn't seem very active so....whatever. It's been modded a little bit. My change examples are in

gui/navdrawer if anything ever gets overwritten.

## Known Issues

### ListView items are selected when trying to scroll

Fixed in 1.9.2-dev0. See: https://github.com/kivy/kivy/issues/3783

Also applied a fix in the MpdBrowser ListView to require a DoubleClick on a ListView item, which addresses this issue. However this issue is mute since we're replacing ListView with RecycleView (see below).

### Poor ListView performance on Raspberry PI

The Raspberry PI doesn't handle large ListViews well, and per Kivy docs, ListView is going to be replaced with RecycleView once RecycleView is 'complete'. 

The MPD screen lists have been updated to RecycleView ahead of it's release for testing, and RecycleView does perform much better than ListView.  However, at the time of this writing, RecycleView does not support selections...so you can't really click on anything! (Sigh...).  As a temporary workaround, I've put buttons on each of the RecycleView Items so they can be 'selected', but this is just a temporary hack until RecycleView is ready. 

The Original MpdBrowser ListView implementation is in mpdux/mpdbrowser.py.  This has been replaced in the **userecycleview** branch (which will soon be merged to master), and the RecycleView MpdBrowser now lives in mpdux/mpdclient.py.

## Kivy config.ini

We're still using the Global config.ini under /home/pi/.kivy/config.ini. 

Below are the non-default changes to config.ini:

[graphics]
display = -1
fullscreen = 1
maxfps = 60
# This is for Landscape wide orientation
width = 800
height = 480
rotation = 0
# This is for the Portrait tall orientation
#width=480
#height=800
#rotation = 90

[input]
mouse = mouse
hid_ads7846 = hidinput,/dev/input/touchscreen,invert_y=0,invert_x=0

[postproc]
# Haven't noticed any jitter issues, so jitter is set to 0 and Kivy processes all touch events
jitter_distance = 0

[widgets]
scroll_timeout = 55
scroll_distance = 20
# These next settings have no effect since Kivy 1.7.0...
scroll_friction = 1.
scroll_stoptime = 300
scroll_moves = 5


## Kivy Versions and Upgrading

We're currently using a development version of Kivy to address known issues w/ the RPi.  Custom built versions are located in *lib/* and require the *PYTHONPATH* environment variable to be included correctly.

v1.9.2-dev is from Feb 23, 2016. As referenced here:   
http://kivypie.mitako.eu/kivy-download.html   
From commit 1029f09366bff06d41b23c7e9b001aad29e49aba
https://github.com/kivy/kivy/commit/1029f09366bff06d41b23c7e9b001aad29e49aba

### Working with older commit example

    git clone https://github.com/kivy/kivy.git
    git reset --hard 1029f09366bff06d41b23c7e9b001aad29e49aba

### Building from source

    cd kivy-version
    make

Remember you must either move/copy the build into your dist-packages (/usr/local/lib/dist-packages/kivy), or include it in PYTHONPATH so it takes precedence over the system dist-packages.   

    echo "export PYTHONPATH=$(pwd):\$PYTHONPATH" >> path-profile
    source ./path-profile

