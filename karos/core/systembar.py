'''
SystemBar
========

ActionBar containing global Back button, Time, and additional SystemTray icons

This is docked at the top of the screen and provides the global Back button to exit from plugin screens, 
as well as System Tray icons, and the Time display.

'''
from utils import dump
import os.path
import pkg_resources
from datetime import datetime

from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivy.uix.actionbar import ActionBar, ActionView, ActionButton, ActionPrevious, ActionLabel, ActionOverflow, ActionGroup
from kivy.uix.bubble import Bubble

from kivy.clock import Clock

from floatingdrawer import FloatingDrawer

from mediabar import MediaBar

Builder.load_string('''
<SystemBar>:
    id: systembar
    pos_hint: {'top':1}
    ActionView:
        id: systemview
        ActionPrevious:
            id: systemback
            title: 'Back'
            with_previous: False
            app_icon_height: 42
            app_icon_width: 42
            app_icon: "''' + '../../plugins/karos-wifi/karos_wifi/icon.png' + '''"
            on_release: root.go_back(app);  #app.sm.current='main'; self.title='Back';
        ActionButton:
            id: systemicon-settings
            icon: "../../plugins/karos-wifi/karos_wifi/icon.png"
            #on_release: app.open_settings()
            on_release: systembar.notify("Notify message", item=self)
        ActionLabel:
            id: systemtime
            align: "right"
            text: root._get_time()

<SystemNotify>:
    opacity: 2
    id: notify
    item: ""
    message: ""
    size_hint: (None, None)
    size: (160, 120)
    background_color: [12, 12, 12, 1]
    y: root.item.y - root.item.height - (self.height/2) - (self.height/8)

    #arrow_pos: 'top_right'
    #right: root.item.right

    arrow_pos: 'top_mid'
    center_x: root.item.center_x
    Label:
        canvas:
            Color:
                rgba: (12, 12, 12, 0.5)
            Color:
                rgba: (1, 0, 0, 0.5)
        id: label
        valign: 'top'
        text: root.message
        color: [255, 255, 255, 1]
        background_color: [255, 255, 255, 1]
''')


class SystemBar(ActionBar):
    time = ObjectProperty("")
    def __init__(self, **kwargs):
        super(SystemBar, self).__init__(**kwargs)
        Clock.schedule_interval(self._update_time, 0.1)

    def go_back(self, app):
        '''Handle back button press. Relaunch main grid screen'''
        self.ids.systemback.title = '';
        app.sm.current = 'main'
        #dump(app.root.ids.mediabar)        
        # Stupid hack...readd the media bar...This works but only once...
        app.root.ids.container.add_widget(MediaBar(id="mediabar"))

    def notify(self, msg, **kwargs):
        '''
            Send a notification from a tray icon. 
            If item is not specified, we default to the Title area
        '''

        # Default to title area if item is not specified
        item = kwargs.get('item', self.ids.systemback.ids.title)
        timeout = kwargs.get('timeout', None)        

        notify = SystemNotify(message=msg, item=item, timeout=timeout)
        item.add_widget(notify)

    def _update_time(self, val=0):
        self.ids.systemtime.text = self._get_time()

    def _get_time(self):
        return datetime.now().strftime("%X %p");

    def set_back_title(self, title):
        self.ids.systemback.title = title


class SystemNotify(Bubble):
    item = ObjectProperty("")
    message = ObjectProperty("")
    fade_clock = None
    default_timeout = 5

    def __init__(self, **kwargs):
        super(SystemNotify, self).__init__(**kwargs)
        timeout = kwargs.get('timeout', self.default_timeout)
        if (timeout == None):
            timeout = self.default_timeout

        if (timeout > 0):
            Clock.schedule_once(self.fadeout, timeout)

    def fadeout(self, val=0):
        opacity = self.background_color[3]
        if (opacity <= 0):
            Clock.unschedule(self.fade_clock)
            self.parent.remove_widget(self)
        else:
            opacity -= 0.1
            self.background_color[3] = opacity
            self.ids.label.color[3] = opacity
            if (self.fade_clock == None):
                self.fade_clock = Clock.schedule_interval(self.fadeout, 0.02)

