from __future__ import unicode_literals
from os.path import dirname

__version__ = '0.2.5'
__name__ = "Wifi"
__title__ = "Wifi Manager"
__icon__ = dirname(__file__) + "/icon.png"

class Plugin():
    version = __version__
    title = __title__
    icon = __icon__
    name = __name__

    def screen(self):
        from .main import karos_wifi as wifi
        return wifi().build()