# Raspberry PI KarOS Setup Notes

**This is an unfinished, early alpha version, and as such is not ready for production use. It is here for historical purposes only. The ads7846 touchscreen is also a resistive touch screen and performs rather poorly. Won't be updated until I get new hardware and motivation.**

## Overview   

The main goal of this project is to provide an touch screen mp3 player for my vehicle using a Raspberry PI.  Also looking to add MTP support so Android (iphone?) phones can be played directly by passengers. 

The main goal is just as a media player, but will hopefully add additional features once the main goal is working well.

## Dependencies

- MPD - For music player
- python-wifi - For wifi scanning / connecting
- python-mpd2 - For MPD usage (Note that's mpd2 - not just mpd)
- Kivy Garden Modules:
  - Recycleview (ListView)
  - Navigationdrawer

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

## Design Notes / Overview for individual modules

### WiFi Manager / WarDriving

- Connect
  - Scan / Interface Select
  - List of SSIDs
  - Signal Graph
  - Connect / PSK / IP-dhcp config
  - Saved Networks
  - Network History
  - Keep Scanning / WarDrive mode
- AP
  - AP Mode / Interface Select
  - SSID & key setup
  - Router IP, DCHPd range
  - Client Listing
  - ip forwarding...
- Monitor mode
  - Interface select
  - Client / traffic list
  - Site survey
- Connect Network Scanner
  - nmap results
    

## What not to do (Deprecation)   

When I first started looking at this project, it seemed like PyGame would fit the bill, and since I hadn't worked with an RPi touchscreen before, I just found one on Amazon that also came with a case.  I purchased the 5" HDMI LCD Touch screen:

http://www.amazon.com/gp/product/B00U21UA16?colid=3DDQ5WN4Z8JOE&coliid=I1X9PBTUCQ8EEK&ref_=wl_it_dp_o_pC_nS_ttl

Which I guess is sold by XYG-Study? Honestly I'm still not sure who the manufacturer of this screen is, but I haven't been super impressed with it...I did get it working, but on my next LCD project, I'm thinking the Official Raspberry PI LCD screen would have better support. 

It came with very little info, and finding drivers or any information about it took some google-fu...Finally got it working via the ads7846 driver, which is natively supported on Raspbian.  The touch screen reports itself as a HID device (like a mouse) though, so Gestures didn't work quite as expected...in researching it appears the official RPi touch screen handles input better than just emulating a mouse HID. 

See the [[Touchscreen]] section for information on configuration. 

In sort, this is the software that **didn't** work well enough for me:

- **libts** - Apparently this was the official Linux touch screen driver for some time, and there's a lot of info on the web.  But it is no longer actively maintained and has been superseded by *evdev*.  It was useful to install just to confirm ts_calibrate and ts_test were working properly, but nothing else worked...X11 did not identify the device at all. And PyGame / SDL did identify it, but wouldn't pick up the X-axis properly (it was always 0).  After playing with it for some time, I found **evdev** has much better support. So don't use libts...
- **PyGame** - May be useful if you're writing a game, but doesn't have many UI widgets available, and gestures are non-existent. 
- **LXDE / Gnome** - No gesture support & doesn't play nice with the touch screen. 
- **Kodi / XBMC** - Did not work with the ads7846 HID...didn't seem to like it pretending to be a mouse or something. I never got it working, and the interface was too sluggish anyway. 
- **Chromium in Kiosk mode or Firefox** This was the best route I'd found, but Scrolling / Gestures didn't have any native support (Firefox maybe...) and a lot of interface handling would have to be done via Javascript. Also no clear way to use an onscreen keyboard. 


## Final Solution

Finally I found Kivy.  A very nice UI toolkit for building mobile / touch screen devices.  It works on RPi, but had to be compiled manually (The apt-get package had some issue I don't recall now...).  But a great tool for building touch interfaces, many widgets available, advanced scroll and gesture support that *just work*. 

- **Matchbox Window Manager** - This could be the main solution, as it's purpose built for touch screens, and has some native gesture support.  It also wraps existing Linux applications, so existing software runs under this window manager.  But it's still rather new.  I'm planning on still using the Matchbox Window Manager for running any 3rd party applications (web browser) that won't be handled via Kivy. 

 
