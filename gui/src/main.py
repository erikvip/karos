import random
from utils import dump

from kivy.interactive import InteractiveLauncher
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.actionbar import ActionBar, ActionView, ActionButton

#from kivy.properties import NumericProperty

from musicplayer.musicplayer import *
#from musicplayer.musicplayer.MusicPlayerScreen import MusicPlayerScreen

#from pudb import set_trace; set_trace()
'''
class MainViewport(ScrollView):
    def __init__(self, **kwargs):
        super(MainViewport, self).__init__(**kwargs)
    def scroll(self, item, vp):
        print "Scrolling!"  
    def touch(args):
        print "Touch event: {}".format(args)    
'''

class PluginIcon(Button, Label):
    source = ObjectProperty()
    text = ObjectProperty()
    direction = ObjectProperty()
    name = ObjectProperty()
    def __init__(self, **kwargs):
        super(PluginIcon, self).__init__(**kwargs)
        self.bind(on_press=self.launch)

    def launch(self, event):
        #dump(app.screens)
        pass
        #app.p(event)


class SettingsScreen(Screen):
    pass


'''
Layout is like this:

ScreenManager
    Screen: MainScreen <GridLayout>:
        ScrollView:
            PluginIcon
    Screen: MusicPlayer 
'''
class CarPiApp(App):
    use_kivy_settings = False
    direction = "vertical"
    screens = []

    def launch(self, icon):

        Logger.info("CarPiApp: Attempting to launch screen {}".format(str(icon.name)))
        self.sm.current = str(icon.name)

    def build(self):
        global app
        app = self

        #self.container = FloatLayout(size=(800, 480))

        self.sm = ScreenManager()

        MainScreen = Screen(name="main")
        self.screens.append(MainScreen)

        Builder.load_file('musicplayer/musicplayer.kv')

        #config = self.config

        #self.direction = "horizontal"

        # Grid layout holds our main icons. 40 px padding on bottom
        if (self.direction == "vertical"):
            grid = GridLayout(cols=5, padding=(0, 40, 0, 0), spacing=18,
                    size_hint=(None, None), width=800)
        else:
            grid = GridLayout(rows=3, padding=(20, 80, 40, 0), spacing=18,
                    size_hint=(None, None), height=480)
        
        # This is the magic that makes ScrollView work when scroll event occurs on a nested child item
        if (self.direction == "vertical"):
            grid.bind(minimum_height=grid.setter('height'))
        else:
            grid.bind(minimum_width=grid.setter('width'))


        #ab = ActionBar(pos_hint={'top':1})
        #grid.add_widget(ab)


        for i in range(30):
            r = random.randrange(1,4)
           
            icon = PluginIcon(text="Media Player with a long name", 
                    direction=self.direction,
                    size=(128, 128), 
                    size_hint=(None, None),
                    source="static/"+str(r)+".png")
            grid.add_widget(icon)

        # create a scroll view, with a size < size of the grid
        if (self.direction == "vertical"):
            root = ScrollView(size_hint=(None, None), size=(800, 480),
                    pos_hint={'center_x': .48, 'center_y': .5}, do_scroll_x=False, do_scroll_y = True)
        else:
            root = ScrollView(size_hint=(None, None), size=(800, 480),
                    pos_hint={'center_x': .42, 'center_y': .5}, do_scroll_x=True, do_scroll_y = False)



        root.add_widget(grid)
        MainScreen.add_widget(root)
        self.sm.add_widget(MainScreen)

        MusicPlayer = MusicPlayerScreen(self, name='musicplayer')

        #self.screens.append(MusicPlayer.build() )
        self.sm.add_widget(MusicPlayer)

       
        #self.container.add_widget(self.sm)

        return self.sm
        #return self.container


    def build_config(self, config):
        config.setdefaults('Global', {
            'volume': '50'
        })


    def p(self, arg):
        dump(arg)
        return "P"

#launcher = InteractiveLauncher(CarPiApp())
#launcher.run()

if __name__ == '__main__':
    app = CarPiApp().run()
