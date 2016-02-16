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




