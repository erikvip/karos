from utils import dump
import os.path
from datetime import datetime

from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivy.uix.actionbar import ActionBar, ActionView, ActionButton, ActionPrevious, ActionLabel, ActionOverflow, ActionGroup
from kivy.uix.bubble import Bubble

from kivy.clock import Clock

from floatingdrawer import FloatingDrawer

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
            app_icon: "../plugins/karos-wifi/karos_wifi/icon.png"
            on_release: app.sm.current='main'; self.title='Back';
        ActionButton:
            id: systemicon-settings
            icon: "../plugins/karos-wifi/karos_wifi/icon.png"
            #on_release: app.open_settings()
            on_release: systembar.notify("Notify message", self)
        ActionLabel:
            id: systemtime
            align: "right"
            text: root.get_time()

<SystemNotify>:
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
        id: label
        valign: 'top'
        text: root.message
        color: [255, 255, 255, 1]
''')


class SystemBar(ActionBar):
    time = ObjectProperty("")
    def __init__(self, **kwargs):
        super(SystemBar, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 0.1)

    def notify(self, msg, item):
        notify = SystemNotify(message=msg, item=item)
        item.add_widget(notify)

    def update_time(self, val=0):
        self.ids.systemtime.text = self.get_time()

    def get_time(self):
        return datetime.now().strftime("%X %p");

    def set_back_title(self, title):
        self.ids.systemback.title = title


class SystemNotify(Bubble):
    item = ObjectProperty("")
    message = ObjectProperty("")
    fade_clock = None

    def __init__(self, **kwargs):
        super(SystemNotify, self).__init__(**kwargs)
        Clock.schedule_once(self.fadeout, 2)

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

