from __future__ import unicode_literals
from os.path import dirname

__version__ = '0.2.4'
__name__ = "Wifi"
__icon__ = dirname(__file__) + "/icon.png"

def launch():
    from .main import CarPI_wifi as wifi
    return wifi().build()

def info():
    return __version__
