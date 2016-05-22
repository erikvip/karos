'''
PluginIcon
==========

This is the wrapper widget for displaying Icons on the Main Desktop screen

'''
import pkg_resources

# For PluginIcon
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.logger import Logger

Builder.load_string('''
<-PluginIcon>:
    text:""
    icon:""
    name:""
    source:""
#    direction: "vertical"
    on_press: app.launch(self)
    size: (app.get_desktop_icon_size(), app.get_desktop_icon_size() )
    size_hint: (None, None)

#    canvas.before:
#        Color:
#            rgb: (255, 0, 0)
#        Rectangle:
#            size: self.size
#            pos: self.pos

    canvas.after:
        BorderImage:
            #auto_scale: True
            source: root.icon
            #tex_coords: (0, 0, 25, 25, 50, 50, 128, 128)
            #pos: (128, 128)
            #pos: (root.center_x, app.p(self))
            #pos: root.center
            #pos: (self.center_x, self.center_y)
            pos: (root.pos)
    Label:
        text: root.text
        #pos: (root.center_x, root.y) 
        pos: (root.x, root.y-(root.height/2))
        text_size: (root.width, None) 
        halign: 'center'
        valign: 'bottom'
        font_size: 13

''')

class PluginIcon(Button, Label):
    text = ObjectProperty()
    icon = ObjectProperty()
    name = ObjectProperty()
    source = ObjectProperty()
    def __init__(self, **kwargs):
        super(PluginIcon, self).__init__(**kwargs)

