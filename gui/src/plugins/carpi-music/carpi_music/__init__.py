from __future__ import unicode_literals
from os.path import dirname

__version__ = '0.1.0'
__name__ = "Music"
__title__ = "Music Library"
__icon__ = dirname(__file__) + "/icon.png"

from mpdclient import Music
from mpcwrapper import MpcWrapper as mpc
#from audioplayer import AudioPlayer


class Plugin():
    version = __version__
    title = __title__
    icon = __icon__
    name = __name__

    def screen(self):

#        self.mpc = mpc(
#            host=self.config.get('mpd', 'host'),
#            port=self.config.get('mpd', 'port')
#        )

        self.mpc = mpc(host='10.0.0.10', port=6600)

        MusicScreen = Music(self.mpc, name="music")
        return MusicScreen

