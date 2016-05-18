from __future__ import unicode_literals
from os.path import dirname

__version__ = '0.1.6'
__name__ = "Info"
__title__ = "System Information"
__icon__ = dirname(__file__) + "/icon.png"

#def launch():
#    from .main import karpc_info as info
#    return info().build()


class Plugin():
    version = __version__
    title = __title__
    icon = __icon__
    name = __name__

    def screen(self):
        from .main import karpc_info as info
        return info().build()