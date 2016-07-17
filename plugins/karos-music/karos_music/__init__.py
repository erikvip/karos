from __future__ import unicode_literals
from os.path import dirname
import pkg_resources
from kivy.logger import Logger

__version__ = '0.1.0'
__title__ = "Music Library"
__description__ = "Music Player and MPD client"
__config_section__ = "Music_Library"
__icon__ = pkg_resources.resource_filename(__name__, 'icon.png')
__default_config__ = {'host': 'localhost','port': 6600}
__default_settings__ = '''
[
    {
        "type": "string",
        "title": "MPD Host",
        "desc": "Music Player Host to connect (Default: localhost)",
        "section": "'''+__config_section__+'''",
        "key": "host"
    },
    {
        "type": "numeric",
        "title": "MPD Port",
        "desc": "Music Player Port to connect (Default: 6600)",
        "section": "'''+__config_section__+'''",
        "key": "port"
    }
]
'''

from mpdclient import Music
from mpcwrapper import MpcWrapper as mpc
#from audioplayer import AudioPlayer

from karos.core.utils import dump

class Plugin(object):
    #default_config = __default_config__
    default_settings = __default_settings__
    version = __version__
    title = __title__
    icon = __icon__
    name = __name__
    config_section = __config_section__
    description = __description__
    config = False

    def __init__(self, **kwargs):
        self.config = kwargs.get('config')

    def screen(self):
        Logger.info("{}: Plugin screen init. Name:{} Version:{} Title:{} File:{} Icon:{}".format(
            __name__, __name__, __version__, __title__, __file__, __icon__))

        self.mpc = mpc(host=self.config.get('host'), port=self.config.get('port'))
        MusicScreen = Music(self.mpc, name=__name__)
        return MusicScreen

    @staticmethod
    def default_config():
        return __default_config__
