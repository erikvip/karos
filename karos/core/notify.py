'''
Notify
==========

Growl style notification that appears near the bottom of the screen

'''
import pkg_resources

# For PluginIcon
from kivy.uix.bubble import Bubble
from kivy.uix.label import Label

from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.logger import Logger

from utils import dump

Builder.load_string('''
<-Notify@Label>:
    text: ''
    canvas.after:
        Color:
            rgba: (12, 12, 12, 0.5)    # Background color
#        BorderImage:
#            pos: int(self.center_x - self.texture_size[0] / 2.), int(self.center_y - self.texture_size[1] / 2.)
#            size: self.texture_size
#            border: [0, 0, 0, 0]
#        Color:
#            rgba:(127, 0, 255, 0.7)
        Line:
            rounded_rectangle: [self.x, self.y, self.width, self.height, 10, 100]
            width: 1
        Color:
            rgba: (255, 127, 255, 1)    # Foreground color
#        Rectangle:
#            texture: self.texture
#            size: self.texture_size
#            pos: int(self.center_x - self.texture_size[0] / 2.), int(self.center_y - self.texture_size[1] / 2.)
#        Line:
#            points: [0, 0, self.width, 0, self.width, self.height, 0, self.height, 0, 0]
#            width: 2
#            cap: 'square'
    halign: 'center'
    valign: 'middle'
    text_size: (400, None)
    #text_size: (None, None)
    size_hint: (None, None)
    size: self.texture_size
    padding: (10, 6)
    pos_hint: {'center_x':0.5, 'y':0.25}
    

''')

class Notify(Label):
    text = StringProperty()
    def __init__(self, text, **kwargs):
        self.text = text
        Logger.info("karos: Notify: new message: {}".format(self.text))
        super(Notify, self).__init__(**kwargs)

