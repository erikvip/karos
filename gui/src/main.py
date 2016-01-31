import json
import pprint

from kivy.interactive import InteractiveLauncher
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

from kivy.graphics import Line

from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
'''    
class PluginIcon(Image, Label):
    file = ObjectProperty()
    pass

    file = ObjectProperty()

    def __init__(self, **kwargs):

        #rect = Line(rectangle=(0, 0, 32, 32))
        if (self.file != None):
            dump(self.file)
            self.source = self.file
            self.reload()
        
      
        super(PluginIcon, self).__init__(**kwargs)
        #self.add_widget(l)
        #self.size = [32,32]
        #self.reload()
        #dump(self)
'''
        
        

def dump(arg):
    print "="*80, "\n", bcolors.BOLD, arg, bcolors.ENDC, "\n" + "="*80, bcolors.WARNING
    col_width = max(len(row) for row in dir(arg)) + 3
    for d in dir(arg):
        print d.ljust(col_width) + " : " + str(getattr(arg,d))

    try:
        pprint.pprint(vars(arg))
    except TypeError:
        pass
    print bcolors.ENDC    

#get_center_x, get_top, get_right(), .height
'''
class PluginIcon(Image):
    name = ObjectProperty()
    x = NumericProperty()
    y = NumericProperty()

    def __init__(self, **kwargs):
        super(PluginIcon, self).__init__(**kwargs)

    def on_press(self, args):
        #from pudb import set_trace; set_trace()
        print "Pressed {}".format(args)
        pp(self)

    def wtf():
        return "wtf"
'''
class MainViewport(ScrollView):
    def __init__(self, **kwargs):
        self.width = 760
        self.height = 440
        super(MainViewport, self).__init__(**kwargs)

        #layout = GridLayout(cols=1, padding=10, spacing=10)

        #self.previous_text = open(self.kv_file).read()
        #parser = Parser(content=self.previous_text)
        #widget = Factory.get(parser.root.name)()
        #Builder._apply_rule(widget, parser.root, parser.root)
        #layout.add_widget(Button(text='Hello 1'))
        #layout.add_widget(Button(text='Hello 2'))

#        self.add_widget(layout)
      #self.add_widget(widget)

    def touch(args):
        print "Touch event: {}".format(args)    
'''
class PluginIcon(Button):
    def __init__(self, **kwargs):

        super(PluginIcon, self).__init__(**kwargs)
        #self.canvas.clear()
        #dump(self.canvas.children)
        self.clear_widgets()
        self.add_widget(Image(source="static/1.png"))
        dump(self)
'''


class CarPiApp(App):
    use_kivy_settings = False

    def build_config(self, config):
        config.setdefaults('Global', {
            'volume': '50'
        })

    def build(self):
        self.width=300
        config = self.config
        return MainViewport()

    def p(self, arg):
        dump(arg)
        return "P"



if __name__ == '__main__':
#    i = InteractiveLauncher(CarPiApp())
#   i.run()
    CarPiApp().run()
#else:
#    print "Not running in main: " + __name__
#    i = InteractiveLauncher(CarPiApp())