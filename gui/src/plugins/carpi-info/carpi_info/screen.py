from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen
from os.path import dirname

class CarPI_info(Screen):
    def __init__( self, **kwargs):
        Logger.info("Info: init")
        super(CarPI_info, self).__init__(**kwargs)

    def build(self):
        Builder.load_file("main.kv")
        return self