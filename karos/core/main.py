from __future__ import unicode_literals
from os.path import dirname
import pkg_resources

import random
#from utils import dump
from karos.core.utils import dump

from pkg_resources import iter_entry_points # For importing plugins

from kivy.app import App

# For PluginIcon
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.logger import Logger
#from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.popup import Popup
from floatingdrawer import FloatingDrawer

from systembar import SystemBar
from mediabar import MediaBar

#from pudb import set_trace; set_trace()

class PluginIcon(Button, Label):
    text = ObjectProperty()
    icon = ObjectProperty()
    name = ObjectProperty()
    source = ObjectProperty()
    def __init__(self, **kwargs):
        super(PluginIcon, self).__init__(**kwargs)


class KarosApp(App):
    lsuse_kivy_settings = False
    settings_cls = 'SettingsWithSidebar'
    settings_popup = ObjectProperty(None, allownone=True)
    #direction = "vertical"
    config = False
    plugins = []

    def __init__(self, **kwargs):
        Logger.info("karos: Init")
        Logger.info("karos: main location: {}".format(__file__))

        self.register_plugins()
        super(KarosApp, self).__init__(**kwargs)
        self.bind(on_start=self.startup)

    def register_plugins(self):
        Logger.info("karos: registering plugins")
        for entry_point in iter_entry_points(group='karos.plugin', name=None):
            p = entry_point.load()
            self.plugins.append(p)
            Logger.info("karos: Plugin: {} title: {} version: {}".format(entry_point.dist, p.title, p.version))
        Logger.info("karos: Found {} plugins".format(len(self.plugins)))

    def build_config(self, config):
        '''Kivy callback. Setup our default ConfigParser object values'''
        self.config = config
        self.config.setdefaults('MPD', {'host': 'localhost','port': 6600})

    def get_application_config(self):
        '''Kivy callback. Return the path to our app config file.'''
        return super(KarosApp, self).get_application_config(
            '~/.karos/%(appname)s.ini')

    def build_settings(self, settings):
        '''Kivy callback. Build our settings info screen'''
        json = '''
        [
            {
                "type": "string",
                "title": "MPD Host",
                "desc": "Music Player Host to connect (Default: localhost)",
                "section": "MPD",
                "key": "host"
            },
            {
                "type": "numeric",
                "title": "MPD Port",
                "desc": "Music Player Port to connect (Default: 6600)",
                "section": "MPD",
                "key": "port"
            }
        ]
        '''
        settings.add_json_panel('MPD', self.config, data=json)

    def display_settings(self, settings):
        p = self.settings_popup
        if p is None:
            self.settings_popup = p = Popup(content=settings,
                                            title='Settings',
                                            size_hint=(0.8, 0.8))
        if p.content is not settings:
            p.content = settings
        p.open()
    def close_settings(self, *args):
        p = self.settings_popup
        if p is not None:
            p.dismiss()



    def launch(self, icon):
        '''
        Launch a given screen / icon
        '''
        Logger.info("karos: Attempting to launch screen {}".format(str(icon.name)))
        if (not self.sm.has_screen(str(icon.name))):
            # Build and launch the plugin screen, first time run
            Logger.info("karos: First view for screen, init: {}".format(icon.name))
            screen = icon.source().screen()
            self.sm.add_widget(screen) 

        # Set the Back button title to our plugin
        if ('systembar' in self.root.ids):
            self.root.ids.systembar.set_back_title(' Back | ' + icon.text)
        self.sm.current = str(icon.name)

    def startup(self, app):
        Logger.info("karos: Startup method called")
        grid = self.root.ids['maingrid']
        self.sm = self.root.ids['sm']

        # Add each of the plugins to the main screen
        '''
        for p in range(30):
            icon = PluginIcon(
                    text='Test ' + str(p) ,
                    icon='../plugins/karos-wifi/karos_wifi/icon.png',
                    name='abc',
                    source='')
            grid.add_widget(icon)            
        '''
        for p in self.plugins:
            icon = PluginIcon(
                    text=p.title,
                    icon=p.icon,
                    name=p.name.lower(),
                    source=p)
            grid.add_widget(icon)
        

    def get_desktop_icon_size(self):
        return 128

    def deprecatedbuild(self):
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
            app_icon="../plugins/karos-wifi/karos_wifi/icon.png", 
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

        self.container.add_widget(self.sm)

#        self.bind(on_start=self.wtf)

        return self.container


        '''
        floatingdrawer = FloatingDrawer()
        panel = BoxLayout(orientation='horizontal')
        self.av = AudioPlayer(self.mpc);
        panel.add_widget(self.av)
        floatingdrawer.add_widget(panel)
        floatingdrawer.dock = 'top'
        floatingdrawer.anim_type = 'reveal_below_anim'
        #floatingdrawer.anim_type = 'reveal_below_simple'
        #floatingdrawer.anim_type = 'slide_above_simple'
        floatingdrawer.toggle_main_above()
        floatingdrawer.add_widget(self.container)

        return floatingdrawer
        '''

    def p(self, arg):
        dump(arg)
        return "P"

#if __name__ == '__main__':
#    app = KarosApp().run()
