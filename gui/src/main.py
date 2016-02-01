import json
import pprint
import random

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
        try:
            print d.ljust(col_width) + " : " + str(getattr(arg,d))
        except AttributeError:
            print "AttributeError: {} -- {}".format(d, d  )

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
        #self.width = 760
        #self.height = 440
        super(MainViewport, self).__init__(**kwargs)

        #self.bind(on_scroll_start=self.scroll)

        #layout = GridLayout(cols=1, padding=10, spacing=10)

        #self.previous_text = open(self.kv_file).read()
        #parser = Parser(content=self.previous_text)
        #widget = Factory.get(parser.root.name)()
        #Builder._apply_rule(widget, parser.root, parser.root)
        #layout.add_widget(Button(text='Hello 1'))
        #layout.add_widget(Button(text='Hello 2'))

#        self.add_widget(layout)
      #self.add_widget(widget)

    def scroll(self, item, vp):
        print "Scrolling!"  
    def touch(args):
        print "Touch event: {}".format(args)    


class PluginIcon(Button, Label):
    source = ObjectProperty()
    text = ObjectProperty()
    def __init__(self, **kwargs):
        super(PluginIcon, self).__init__(**kwargs)
        dump(self)



class CarPiApp(App):
    use_kivy_settings = False

    def build(self):
        #config = self.config
        #self.width=300
        #return MainViewport()

        # Grid layout holds our main icons. 40 px padding on bottom
        layout = GridLayout(cols=4, padding=(0, 0, 0, 40), spacing=18,
                size_hint=(None, None), width=700)
        
        # This is the magic that makes ScrollView work when you
        # scroll on a nested child item
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(30):
            r = random.randrange(1,4)
           
            icon = PluginIcon(text="Media Player With a Long Name", 
                    size=(128, 128), 
                    size_hint=(None, None),
                    source="static/"+str(r)+".png")
            layout.add_widget(icon)

                    # create a scroll view, with a size < size of the grid
        root = ScrollView(size_hint=(None, None), size=(700, 480),
                pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        root.add_widget(layout)

        return root




    def build_config(self, config):
        config.setdefaults('Global', {
            'volume': '50'
        })


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