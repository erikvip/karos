# Music Info

Information on the MPD Browser, player, and other music-related features. 

## MPD Setup

### Installation

- Install mpd via **apt-get install mpd**
- Configure mpd via /etc/mpd.conf
- Create directory structure as defined in mpd.conf
- Verify permissions
- Launch on boot **sudo update-rc.d mpd defaults**

### mpd.conf

Example mpd.conf.  This resides in /etc. All mpd files are housed under /home/pi/mpd, and the mpd process runs under the *pi* user, so we have access to everything.

**mpd.conf**   

    music_directory     "/home/pi/mpd/mp3"
    playlist_directory      "/home/pi/mpd/playlists"
    db_file         "/home/pi/mpd/tag_cache"
    log_file            "/home/pi/mpd/mpd.log"
    pid_file            "/home/pi/mpd/run/mpd/pid"
    state_file          "/home/pi/mpd/state"
    sticker_file                   "/home/pi/mpd/sticker.sql"
    user                "pi"
    bind_to_address     "localhost"
    input {
            plugin "curl"
    }
    audio_output {
        type        "alsa"
        name        "My ALSA Device"
    }
    filesystem_charset      "UTF-8"
    id3v1_encoding          "UTF-8"


**Directory structure of /home/pi/mpd/**   

    mpd/
    ├── mp3/
    ├── mpd.log
    ├── playlists/
    ├── run/
    │   └── mpd/
    │       └── pid
    ├── state
    ├── sticker.sql
    └── tag_cache

**Configure mpd to run at boot**   

    sudo update-rc.d mpd defaults

## Configuring the sound subsystem

If you're receiving an error when trying to change volume, and get no sound, follow the instructions below. 

This installs and configures pulseaudio, but we still use ALSA...after doing this though, everything appears to work...go figure.

Good instructions found here:   

http://raspberrypi.stackexchange.com/questions/12339/pulseaudio-mpd-http-streaming-installation-guide

**Install pulseaudio and pulseaudio-zeroconf**   

    sudo apt-get install pulseaudio-module-zeroconf    

Configure /etc/default/pulseaudio with default options for pulseaudio init   
**/etc/default/pulseaudio**   

    PULSEAUDIO_SYSTEM_START=1
    DISALLOW_MODULE_LOADING=0

In **/etc/pulse/default.pa** and **/etc/pulse/system.pa** add these lines to enable TCP access and setup ACL permissions:    

    load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1;10.0.0.0/24 auth-anonymous=1
    load-module module-zeroconf-publish

**Note**: You'll need to change *10.0.0.0/24* to your own local subnet

**Disable suspend-on-idle in default.pa and system.pa**   

**/etc/pulse/default.pa** and **/etc/pulse/system.pa**   

Add a semicolon (;) before the *module-suspend-on-idle* line:   

    ; load-module module-suspend-on-idle

**Convert the ALSA configuration libraries to PulseAudio**    

    sudo nano /etc/asound.conf

Add these entries to the file

    pcm.pulse { type pulse }
    ctl.pulse { type pulse }
    pcm.!default { type pulse }
    ctl.!default { type pulse }    

Your **audio_output** section of */etc/mpd.conf*  should be setup to use alsa, as configured above:   

    audio_output {
        type        "alsa"
        name        "My ALSA Device"
    }


Now reboot the pi, and MPD / setvol should be working properly.


