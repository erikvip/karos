from __future__ import unicode_literals
from os.path import dirname
import pkg_resources
from kivy.logger import Logger

__version__ = '0.2.5'
__title__ = "Wifi Manager"
__description__ = "description"
__icon__ = pkg_resources.resource_filename(__name__, 'icon.png')

class Plugin():
    version = __version__
    title = __title__
    icon = __icon__
    name = __name__
    description = __description__

    def screen(self):
        Logger.info("{}: Plugin screen init. Name:{} Version:{} Title:{} File:{} Icon:{}".format(
            __name__, __name__, __version__, __title__, __file__, __icon__))

        from .main import karos_wifi as wifi
        return wifi(name=__name__).build()