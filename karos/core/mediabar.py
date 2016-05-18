from utils import dump
import os.path
from datetime import datetime

from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivy.uix.actionbar import ActionBar, ActionView, ActionButton, ActionPrevious, ActionLabel, ActionOverflow, ActionGroup
from floatingdrawer import FloatingDrawer

Builder.load_string('''
<MediaBar>:
    id: mediabar
    pos_hint: {'bottom':1}
    ActionView:
        id: mediaview
        ActionPrevious:
            id: mediaapp
            title: ''
            with_previous: True
            app_icon_height: 42
            app_icon_width: 42
            app_icon: "../plugins/karos-wifi/karos_wifi/icon.png"
            on_press: root.do("omgwtf")
        ActionButton:
            id: skip-back
            icon: "core/data/images/skip-back.png"
            on_press: root.do("skip-back")
        ActionButton:
            id: play-pause
            media_state: 'pause'
            pause_icon: "core/data/images/pause.png"
            play_icon: "core/data/images/pause.png"
            #on_state: self.pause_icon if self.state == 'play' else self.play_icon
            icon: self.pause_icon if self.media_state == 'play' else self.play_icon
            on_press: print("Skip back")
        ActionButton:
            id: skip-forward
            icon: "core/data/images/skip-forward.png"
            on_press: print("Skip back")


''')


class MediaBar(ActionBar):
    def __init__(self, **kwargs):
        super(MediaBar, self).__init__(**kwargs)

    def do(self, action):
        print action
