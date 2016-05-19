import kivy
kivy.require('1.0.8')

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from kivy.logger import Logger
from wifi import Cell, Scheme

import subprocess

class karos_wifi(Screen):
    def __init__(self, **kwargs):
        Logger.info("karos_wifi: init")
        self.name="wifi"
        #Builder.load_file(dirname(__file__) + "/main.kv")
        super(karos_wifi, self).__init__(**kwargs)


    def get_wireless_interfaces(self):
        Logger.info("karos_wifi: Getting wireless interfaces from /proc/net/wireless")

        try:
            proc = subprocess.Popen("cat /proc/net/wireless  | tail -n +3 | cut -d ':' -f1 | tr -d ' \t'", stdout=subprocess.PIPE, shell=True)
            (output, error) = proc.communicate()
        except:
            Logger.error("karos_wifi: Failed to gather wireless interfaces")
            throw

        inf = [i.strip() for i in output.splitlines()]
        Logger.info("karos_wifi: Found {} wireless interfaces: {}".format(len(inf), inf))
        return inf


    def build(self):
        interfaces = self.get_wireless_interfaces()

        if len(interfaces) > 0:
            inf = interfaces[0]
        else:
            inf = False
            root = Label(text="[color=ff0000]No wireless interfaces found[/color]", markup=True)
            self.add_widget(root)
            return self

        Logger.info("karos_wifi: Using {} for wireless scan".format(inf))

        # create a default grid layout with custom width/height
        layout = GridLayout(cols=4, padding=10, spacing=10,
                size_hint=(1, 0))

        # when we add children to the grid layout, its size doesn't change at
        # all. we need to ensure that the height will be the minimum required to
        # contain all the childs. (otherwise, we'll child outside the bounding
        # box of the childs)
        layout.bind(minimum_height=layout.setter('height'))

        scan = Cell.all('wlan0')

        Logger.info("karos_wifi: Results from iw scan: {}".format(scan))

        for s in scan:
            Logger.info("karos_wifi: Network info - ssid: {} signal: {} quality: {} bitrates: {} channel: {} encrypted: {}".format(
                    s.ssid, 
                    s.signal, 
                    s.quality, 
                    s.bitrates, 
                    s.channel, 
                    s.encrypted
                ))

            l_ssid = Label(text=s.ssid)
            l_info = Label(text="{} [{}] Ch: {}".format(s.quality, s.signal, s.channel))

            if (s.encrypted == True):
                enc_text = "[color=ff0000]{}[/color]".format(s.encryption_type)
            else:
                enc_text = "[color=00ff00]Open[/color]"

            l_encrypt = Label(text=enc_text, markup=True)

            btn = Button(text="Join", size=(80, 40),
                         size_hint=(None, None))

            layout.add_widget(l_ssid)
            layout.add_widget(l_encrypt)
            layout.add_widget(l_info)

            layout.add_widget(btn)

        # create a scroll view, with a size < size of the grid
        root = ScrollView(size_hint=(0.8, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}, do_scroll_x=False)
        root.add_widget(layout)

        self.add_widget(root)

        return self

#if __name__ == '__main__':
#    karos_wifi().run()
