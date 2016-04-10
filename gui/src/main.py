import random
from utils import dump

from pkg_resources import iter_entry_points # For importing plugins

from kivy.interactive import InteractiveLauncher
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.actionbar import ActionBar, ActionView, ActionButton, ActionPrevious, ActionLabel, ActionOverflow, ActionGroup


from kivy.garden.navigationdrawer import NavigationDrawer

#from kivy.properties import NumericProperty


#from mpdux.mpdbrowser import MpdBrowser
#from mpdux.mpdclient import MpdBrowser
#from mpdux.mpcwrapper import MpcWrapper as mpc
#from mpdux.audioplayer import AudioPlayer



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
    icon = ObjectProperty()

    def __init__(self, **kwargs):
        super(PluginIcon, self).__init__(**kwargs)
        #self.bind(on_press=self.launch)

#    def launch(self, event):
#        pass



class SettingsScreen(Screen):
    pass


'''
Layout is like this:

ScreenManager
    Screen: MainScreen <GridLayout>:
        ScrollView:
            PluginIcon
    Screen: MpdBrowser 
'''
class CarPiApp(App):
    use_kivy_settings = False
    direction = "vertical"
    screens = []
    mpd = False
    config = False
    plugins = []

    def __init__(self, **kwargs):
        Logger.info("CarPiApp: Init")
        self.register_plugins()
        super(CarPiApp, self).__init__(**kwargs)

    def register_plugins(self):
        Logger.info("CarPiApp: registering plugins")
        for entry_point in iter_entry_points(group='carpi.plugin', name=None):
            p = entry_point.load()
            self.plugins.append(p)
            Logger.info("CarPiApp: Plugin: {} title: {} version: {}".format(entry_point.dist, p.title, p.version))
        Logger.info("CarPiApp: Found {} plugins".format(len(self.plugins)))

    def build_config(self, config):
        self.config = config
#        self.config.setdefaults('mpd', {
#            'host': mpc.host,
#            'port': mpc.port
#        })

    def launch(self, icon):
        '''
        Launch a given screen / icon
        '''
        Logger.info("CarPiApp: Attempting to launch screen {}".format(str(icon.name)))
        #dump(self.sm)
        #dump(icon.source.na)
        if (not self.sm.has_screen(str(icon.name))):
            # Build and launch the plugin screen, first time run
            Logger.info("CarPiApp: First view for screen, init: {}".format(icon.name))
            screen = icon.source().screen()
            self.sm.add_widget(screen)
        self.sm.current = str(icon.name)

    def go_back(self, ap):

        self.sm.current='main'

 #   def wtf(self, r):
        #w = self.get_root_window()
        #dump(self.root_window)
#        self.root_window._rotation = 90

#        print r.children


    def build(self):
        global app
        app = self

        # MPD Connection
#        self.mpc = mpc(
#            host=self.config.get('mpd', 'host'),
#            port=self.config.get('mpd', 'port')
#        )

        #self.container = BoxLayout(size=(800, 480), id='container', orientation='vertical')
        self.container = FloatLayout()

        self.ab = ActionBar(id="ab", pos_hint={'top':1})
        self.ab2 = ActionBar(id="ab2", pos_hint={'bottom':1})

        self.av = ActionView(id="av")
        self.av2 = ActionView(id="av2")

        btn = ActionPrevious(
            title="Back", 
            with_previous=True, 
            app_icon_height=42,
            app_icon_width=42,
            app_icon="/home/erikp/work/pi/car/gui/src/plugins/carpi-wifi/carpi_wifi/icon.png", 
            on_press=self.go_back

        )

        ag = ActionGroup(size_hint=(0.5, 1), pos_hint={'center_x':0.5, 'center_y':0.5})

        lb = ActionLabel(text='Abadsfaasdfasdffffff', size_hint=(0.25, 1))
        lb2 = ActionLabel(text='Abadsfasd', size=(100, 20), pos_hint={'center_x':0.5, 'center_y':0.5})

        #ag.add_widget(btn)
        ag.add_widget(lb)
        ag.add_widget(lb2)
        
        self.av.add_widget(btn)
        #self.av.add_widget(lb)
        #self.av.add_widget(lb2)
        self.av.add_widget(ag)

        self.ab.add_widget(self.av)
        #self.ab2.add_widget(self.av2)

        self.container.add_widget(self.ab)
        #self.container.add_widget(self.ab2)

        self.sm = ScreenManager(id='sm')

        MainScreen = Screen(name="main")
        self.screens.append(MainScreen)

#        Builder.load_file('mpdux/mpdbrowser.kv')
#        Builder.load_file('mpdux/audioplayer.kv')

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


        for p in self.plugins:
            icon = PluginIcon(
                    text=p.title,
                    direction=self.direction,
                    size=(128, 128),
                    size_hint=(None, None),
                    icon=p.icon,
                    name=p.name.lower(),
                    source=p)
            grid.add_widget(icon)


        # create a scroll view, with a size < size of the grid
        if (self.direction == "vertical"):
            root = ScrollView(size_hint=(1, 0.75), #size=(800, 480),
                    pos_hint={'center_x': .48, 'center_y': 0.5}, do_scroll_x=False, do_scroll_y = True)
        else:
            root = ScrollView(size_hint=(None, None), size=(800, 480),
                    pos_hint={'center_x': .42, 'center_y': .5}, do_scroll_x=True, do_scroll_y = False)



        root.add_widget(grid)
        MainScreen.add_widget(root)
        self.sm.add_widget(MainScreen)


#        MpdBrowserScreen = MpdBrowser(self, self.mpc, name='mpdbrowser')
#        self.sm.add_widget(MpdBrowserScreen)

        #dump(self)
        self.container.add_widget(self.sm)

#        self.bind(on_start=self.wtf)
        #self.root.ids.container.add_widget(self.sm)

        #self.add_widget(self.container)

        return self.container


        #self.donebuild()
        #return self.container
        '''
        navigationdrawer = NavigationDrawer()
        panel = BoxLayout(orientation='horizontal')
        self.av = AudioPlayer(self.mpc);
        panel.add_widget(self.av)
        navigationdrawer.add_widget(panel)
        navigationdrawer.dock = 'top'
        navigationdrawer.anim_type = 'reveal_below_anim'
        #navigationdrawer.anim_type = 'reveal_below_simple'
        #navigationdrawer.anim_type = 'slide_above_simple'
        navigationdrawer.toggle_main_above()
        navigationdrawer.add_widget(self.container)

        return navigationdrawer
        '''
        #return self.sm
#        return self.container


    def donebuild(self):
        print self.root.ids

    def p(self, arg):
        dump(arg)
        return "P"

#launcher = InteractiveLauncher(CarPiApp())
#launcher.run()

if __name__ == '__main__':
    app = CarPiApp().run()
