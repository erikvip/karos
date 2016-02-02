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
    direction = ObjectProperty()
    def __init__(self, **kwargs):
        super(PluginIcon, self).__init__(**kwargs)
        self.bind(on_press=self.launch)

    def launch(self, event):
        dump(self)


class CarPiApp(App):
    use_kivy_settings = False
    direction = "vertical"

    def build(self):
        #config = self.config
        #self.width=300
        #return MainViewport()
        self.direction = "horizontal"

        # Grid layout holds our main icons. 40 px padding on bottom
        if (self.direction == "vertical"):
            layout = GridLayout(cols=5, padding=(0, 40, 0, 0), spacing=18,
                    size_hint=(None, None), width=800)
        else:
            layout = GridLayout(rows=3, padding=(20, 80, 40, 0), spacing=18,
                    size_hint=(None, None), height=480)
        
        # This is the magic that makes ScrollView work when scroll event occurs on a nested child item
        if (self.direction == "vertical"):
            layout.bind(minimum_height=layout.setter('height'))
        else:
            layout.bind(minimum_width=layout.setter('width'))

        for i in range(30):
            r = random.randrange(1,4)
           
            icon = PluginIcon(text="Media Player with a long name", 
                    direction=self.direction,
                    size=(128, 128), 
                    size_hint=(None, None),
                    source="static/"+str(r)+".png")
            layout.add_widget(icon)

        # create a scroll view, with a size < size of the grid
        if (self.direction == "vertical"):
            root = ScrollView(id="main", size_hint=(None, None), size=(800, 480),
                    pos_hint={'center_x': .48, 'center_y': .5}, do_scroll_x=False, do_scroll_y = True)
        else:
            root = ScrollView(id="main", size_hint=(None, None), size=(800, 480),
                    pos_hint={'center_x': .42, 'center_y': .5}, do_scroll_x=True, do_scroll_y = False)
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