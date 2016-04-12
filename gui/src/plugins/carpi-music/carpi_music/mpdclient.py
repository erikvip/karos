#from ../util import dump

'''
==Known issues==

- Scrolling / Last selected item   
    When you drill down to the song level, then go back up one level to album view, 
    the upper items are hidden. This is on purpose, since when going back, we re-select
    the last index from the breadcrumb trail...on bigger lists, just scrolling up/down will show the top, 
    but on small lists (artists with only 1-2 albums...), we can't scroll up and we're prevented from going back.

    Seems like this could be fixed if we just disable the previous menu auto scroll...but it's really needed on the
    large artist list...even though that isn't working right either ! (See below...)
    Fuck...can we just do absolute x / y position scrolling instead of this selected item index B.S ... ?
        - But only when the # of list items * row_height would exceed the available screen height...
    or
        - Wouldn't be an issue if it wasn't for the NavigationalDrawer / Status thing...but that's really useful...
            - Can we move it to the right? or....maybe the bottom? hmm

- The 'selected previously selected index' feature appears to work...until you scroll. Then we go back to 0!
    - Example:
        - Go down a ways on Artist view 
        - Select an artist. Then hit '..' to go back...
        - We're at the correct artist view...but now try to Scroll...
        - We're back at the top of the $@#$@# list!
    - This is implemented at the end of do_selection. Via list_view.scroll_to ...
'''


from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListItemButton, ListItemLabel
from kivy.adapters.dictadapter import DictAdapter
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.bubble import Bubble
from kivy.uix.bubble import BubbleButton

from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty

from kivy.logger import Logger
from kivy.lang import Builder

from kivy.garden.recycleview import RecycleView

from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label import Label

from kivy.uix.screenmanager import ScreenManager, Screen
from utils import dump
from utils import Growl
from os.path import dirname
import mpd


import string
import random


__all__ = ('Music', )

class MpdItem(BoxLayout):
    index = NumericProperty()
    mpd_name = ObjectProperty()
    mpd_media = ObjectProperty()
    mpd_data = ObjectProperty()

    def __init__(self, **kwargs):
        super(MpdItem, self).__init__(**kwargs)

    def on_press(self, app, btn):
        # Call the on_press method of the RecycleView
        sm = app.root.ids.sm
        music = sm.get_screen('music')
        item = btn.parent
        music.mpd_select(item)


class MpdLibrary(RecycleView):
    pass


'''
Test using RecycleView instead of ListView...
'''
class Music(Screen):
    mpc = None
    mpd_root_data = []
    mpd_level = 0
    mpd_history = {0:"/"}

    def __init__(self, mpc, **kwargs):
        Logger.info("Music: init")
        Builder.load_file(dirname(__file__) + '/mpdclient.kv')
        self.mpc = mpc
        self.mpd_root_data = self.fetch_data()
        super(Music, self).__init__(**kwargs)


    def fetch_data(self, item="/"):
        Logger.info("Music: Querying mpd for: {}".format(item))

        data = []
        if (item != "/"):
            data = [{'text':"..", 'type':'directory'}]

        count_dirs = 0
        count_files = 0

        for entry in self.mpc.lsinfo(item):
            if 'directory' in entry:
                data.append({'text':str(entry['directory']), 'type':'directory'})
                count_dirs+=1
            if 'title' in entry:
                data.append({'text':str(entry['title']), 'type':'file', 'file':entry['file']})
                count_files+=1

        Logger.info("Music: MPD Stats, directories: {}, files: {}".format(count_dirs, count_files))
        
        result = []
        x = 1;
        for r in data:
            x+=1
            result.append({
                "index": x,
                "viewclass": "MpdItem",
                "mpd_data": r,
                "mpd_name": r['text'],
                "mpd_media": "http://rocketdock.com/images/screenshots/Aphex-Clock.png"
            })

        return result

    def mpd_select(self, item):

        text = item.mpd_data['text']

        if (text == ".."):
            del self.mpd_history[self.mpd_level]
            self.mpd_level -= 1
            text = self.mpd_history[self.mpd_level]
        else:
            self.mpd_level += 1
            self.mpd_history[self.mpd_level] = text

        data = self.fetch_data(text)
        self.ids.mpdlibrary.data = data


'''

class MpdBrowserzz(Screen):
    def __init__(self, mpc, **kwargs):
        Logger.info("MpdBrowser: Init")        
        Builder.load_file(dirname(__file__) + '/mpdclient.kv')
        # Setup mpd connection
        self.mpc = mpc
        #Logger.info("MpdBrowser: Connected to MPD")
        super(MpdBrowser, self).__init__(**kwargs)

        self.selection_history=[{'text':'/', 'index':0}];
        self.selection_last_item_index=0


        dump(self)

        #self.build()

    def fetch_data(self, item="/"):
        Logger.info("MpdBrowser: Querying mpd for: {}".format(item))

        self.data = []
        if (item != "/"):
            self.data = [{'text':"..", 'type':'directory'}]

        count_dirs = 0
        count_files = 0

        for entry in self.mpc.lsinfo(item):
            if 'directory' in entry:
                self.data.append({'text':str(entry['directory']), 'type':'directory'})
                count_dirs+=1
            if 'title' in entry:
                self.data.append({'text':str(entry['title']), 'type':'file', 'file':entry['file']})
                count_files+=1

        Logger.info("MpdBrowser: MPD Stats, directories: {}, files: {}".format(count_dirs, count_files))


        return self.data

    def convert_data_for_recycleview(self, data):
        result = []
        x = 1; 
        for r in data:
            x+=1
            result.append({
                "index": x, 
                "viewclass": "MpdItem",
                "mpd_data": r, 
                "mpd_name": r['text'], 
                "mpd_media": "http://rocketdock.com/images/screenshots/Aphex-Clock.png"
            })

        return result            

    def create_recycleview(self, data):
        self.rv = RecycleView(
            width=800,
            height=400,
            data=data,
            key_viewclass="viewclass",
            key_size="height"
        )

#        adapter = self.rv._get_adapter()

#       RecycleView doesn't support FREAKING SELECTIONS YET!! *Of course
#        adapter.bind(
#            on_selection_change=self.do_selection,
#            selection_mode="single"
#        )

        return self.rv
            

    def build(self):
        data = self.fetch_data("/")
        data = self.convert_data_for_recycleview(data)
        recycleview = self.create_recycleview(data)
        

        panel = TabbedPanel(do_default_tab=False, size_hint=(1,0.75) )

        list_panel = TabbedPanelItem(text='Library')
        

        lib_list = AccordionItem(title="Music Library")
        lib_list.add_widget(self.rv)

        lib_dev = AccordionItem(title="Devices")

        lib_accordion = Accordion()
        lib_accordion.add_widget(lib_dev)
        lib_accordion.add_widget(lib_list)

        list_panel.add_widget(lib_accordion)


        #list_panel.add_widget(list_view)

        playlist_panel = TabbedPanelItem(text='Playlist')
        

        playlist_current = AccordionItem(title="Current Queue")
        playlist_mpd = AccordionItem(title="Saved Playlists")
        playlist_accordion = Accordion()
        
        playlist_accordion.add_widget(playlist_mpd)
        playlist_accordion.add_widget(playlist_current)

        playlist_panel.add_widget(playlist_accordion)


        panel.add_widget(list_panel)
        panel.add_widget(playlist_panel)
        

        self.add_widget(panel)

        return self

    def on_press(self, item):
        text = item.mpd_data['text']
        if (text == '..'):
            text = "/"
        else:
            self.last_item = item
        response = self.fetch_data(text)
        data = []
        x = 1; 
        for r in response:
            x+=1
            data.append({
                "index": x, 
                "viewclass": "MpdItem",
                "mpd_data": r, 
                "mpd_name": r['text'], 
                "mpd_media": "http://rocketdock.com/images/screenshots/Aphex-Clock.png"
            })

        self.rv.data = data
        if (text == "/"):
            print "last item"
            dump(self.last_item)
            self.rv.goto_node(self.last_item.index, self.item, self.item.index)
            #self.rv.scroll_to(self.last_item.x)
            #self.rv.scroll_to(self.last_item.to_window(self.last_item.pos))


    def deprecated_do_selection(self, list):
        #self.app.p(list)
        # I'm TIRED of the damn scroll / child selection issue!
        # So we're REQUIRING you to double click and item to open it...but Kivy
        # doesn't seem to support double clicking a list item...so what we're doing is:
        # - Set allow_empty_selection to True
        # - Whenever we have a valid select, save the index
        # - Next time when we don't have a valid select, it means our last index was selected...
        # - Use the last index to open the item
        if (len(list.selection) > 0):
            index = list.selection[0].index
        else:
            index = self.selection_last_item_index

        Logger.info("MpdBrowser: Selection. Current index: {}, last_index: {}".format(index, self.selection_last_item_index));

        # Our current item has only been tapped once. Deselect it, but remember the index
        if (self.selection_last_item_index != index):
            self.selection_last_item_index = index;
            list.deselect_data_item(index)
            return

        item = self.data[self.selection_last_item_index]
        text = item.get('text')
        self.selection_last_item_index = -1;

        Logger.info("MpdBrowser: Selected text: {}".format(text))

        if ( str(text) == ".." ):
            s = len(self.selection_history)
            if (len(self.selection_history) > 1):
                current_item = self.selection_history.pop();
                last_item = self.selection_history.pop();
            elif (len(self.selection_history) == 1):
                last_item = self.selection_history.pop();
                current_item = last_item;
            else:
                text = "/"

            try:
                text = last_item['text']
                index = current_item['index']
            except NameError:
                pass


            Logger.info("MpdBrowser: Navigating up to: {}. Selection history size: {}".format(text, s))
            item = {'type':'directory', 'text':text}

#        else:
#            self.selection_history.append(text)

        if (item.get('type') == 'file'):
            Logger.info("MpdBrowser: Start playing song: {}".format(text))
            #Growl(self.app, text="Added {} to queue".format(text))
            file = item.get('file')
            self.mpc.add(file)
            #self.mpc.play()
        else:
            if (text != '/'):
                self.selection_history.append({'text':text, 'index':int(index) })
                Logger.info('MpdBrowser: Added {} to selection history. Currently: {}'.format(text, self.selection_history))
            else:
                self.selection_history = [{'text':'/', 'index':0}]
                Logger.info('MpdBrowser: Cleared selection history')

            self.clear_widgets()

            data = self.fetch_data(text)
            list_view = self.create_list(data)

            self.add_widget(list_view)

            # If we're navigating up, scroll to the previously selected item
            try:
                di = self.data[current_item['index']];
                Logger.info("MpdBrowser: Scrolling to previous text: {} index: {} data_item: {}".format(last_item['text'], current_item['index'], di))

                self.list_view.scroll_to(index=current_item['index'])
            except NameError:
                pass


    def deprecated_create_list(self, data):

        list_item_args_converter = \
                lambda row_index, rec: {'text': rec['text'],
                                        'size_hint_y': None,
                                        'height': 80}

        adapter = ListAdapter(
                                   data=data,
                                   args_converter=list_item_args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=True,
                                   cls=ListItemButton)

        adapter.bind(on_selection_change=self.do_selection)                
        self.list_view = ListView(
            adapter=adapter,
            size_hint=(1, 0.8),
            #pos_hint={'x':0, 'y': -0.20}
        )
        return self.list_view



if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from mpcwrapper import MpcWrapper as mpc
    Builder.load_file('mpdbrowser.kv')

    class DemoApp(App):
        mpc = False
        def build(self):
            app = self
            #self.container = FloatLayout(size=(800, 480))
            #self.sm = ScreenManager()
            #self.sm.add_widget(MpdBrowserScreen(app, name="main"))
            #self.container.add_widget(self.sm)
            #return self.container;
            #return self.sm;
            self.mpc = mpc(host="10.0.0.10")
            Logger.info("MpdBrowser: Running in standalone mode")
            return MpdBrowser(app, self.mpc)

    app = DemoApp().run()

'''    