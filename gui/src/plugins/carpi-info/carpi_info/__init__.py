from __future__ import unicode_literals
from os.path import dirname

__version__ = '0.1.1'
__name__ = "Info"
__icon__ = dirname(__file__) + "/icon.png"

def launch():
    from .main import CarPI_info as info
    return info().build()

def info():
    return __version__

