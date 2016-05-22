from __future__ import unicode_literals
from os.path import dirname
import pkg_resources
from kivy.logger import Logger

__version__ = '0.1.0'
__title__ = "Music Library"
__icon__ = pkg_resources.resource_filename(__name__, 'icon.png')

from mpdclient import Music
from mpcwrapper import MpcWrapper as mpc
#from audioplayer import AudioPlayer

class Plugin():
    version = __version__
    title = __title__
    icon = __icon__
    name = __name__

    def screen(self):
        Logger.info("{}: Plugin screen init. Name:{} Version:{} Title:{} File:{} Icon:{}".format(
            __name__, __name__, __version__, __title__, __file__, __icon__))

    	self.mpc = mpc(host='10.0.0.10', port=6600)
        MusicScreen = Music(self.mpc, name=__name__)
        return MusicScreen

