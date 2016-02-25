






































            plugin "curl"
        name        "My ALSA Device"
        name        "My ALSA Device"
        type        "alsa"
        type        "alsa"
    ; load-module module-suspend-on-idle
    audio_output {
    audio_output {
    bind_to_address     "localhost"
    ctl.!default { type pulse }    
    ctl.pulse { type pulse }
    db_file         "/home/pi/mpd/tag_cache"
    DISALLOW_MODULE_LOADING=0
    filesystem_charset      "UTF-8"
    id3v1_encoding          "UTF-8"
    input {
    load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1;10.0.0.0/24 auth-anonymous=1
    load-module module-zeroconf-publish
    log_file            "/home/pi/mpd/mpd.log"
    mpd/
    music_directory     "/home/pi/mpd/mp3"
    pcm.!default { type pulse }our money like I did or time. Koubachi didn't put a lot of work on their software design either. Very plain and poor on the data. It upda
    pcm.pulse { type pulse }
    pid_file            "/home/pi/mpd/run/mpd/pid"
    playlist_directory      "/home/pi/mpd/playlists"
    PULSEAUDIO_SYSTEM_START=1
    state_file          "/home/pi/mpd/state"
    sticker_file                   "/home/pi/mpd/sticker.sql"
    sudo apt-get install pulseaudio-module-zeroconf    
    sudo nano /etc/asound.conf
    sudo update-rc.d mpd defaults
    user                "pi"
    }
    }
    }
    │       └── pid
    │   └── mpd/
    └── tag_cache
    ├── mp3/
    ├── mpd.log
    ├── playlists/
    ├── run/
    ├── state
    ├── sticker.sql
# Music Info
## Configuring the sound subsystem
## MPD Setup
### Installation
### mpd.conf
**/etc/default/pulseaudio**   
**/etc/pulse/default.pa** and **/etc/pulse/system.pa**   
**Configure mpd to run at boot**   
**Convert the ALSA configuration libraries to PulseAudio**    
**Directory structure of /home/pi/mpd/**   
**Disable suspend-on-idle in default.pa and system.pa**   
**Install pulseaudio and pulseaudio-zeroconf**   
**mpd.conf**   
**Note**: You'll need to change *10.0.0.0/24* to your own local subnet
- Configure mpd via /etc/mpd.conf
- Create directory structure as defined in mpd.conf
- Install mpd via **apt-get install mpd**
- Launch on boot **sudo update-rc.d mpd defaults**
- Verify permissions
Add a semicolon (;) before the *module-suspend-on-idle* line:   
Add these entries to the file
Configure /etc/default/pulseaudio with default options for pulseaudio init   
Example mpd.conf.  This resides in /etc. All mpd files are housed under /home/pi/mpd, and the mpd process runs under the *pi* user, so we have access to everything.
Good instructions found here:   
http://raspberrypi.stackexchange.com/questions/12339/pulseaudio-mpd-http-streaming-installation-guide
If you're receiving an error when trying to change volume, and get no sound, follow the instructions below. 
In **/etc/pulse/default.pa** and **/etc/pulse/system.pa** add these lines to enable TCP access and setup ACL permissions:    
Information on the MPD Browser, player, and other music-related features. 
Now reboot the pi, and MPD / setvol should be working properly.
This installs and configures pulseaudio, but we still use ALSA...after doing this though, everything appears to work...go figure.
Your **audio_output** section of */etc/mpd.conf*  should be setup to use alsa, as configured above:   