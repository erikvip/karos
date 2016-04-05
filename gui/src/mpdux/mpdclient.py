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

from kivy.properties import ObjectProperty
from kivy.logger import Logger
from kivy.lang import Builder

from kivy.garden.recycleview import RecycleView

from kivy.uix.screenmanager import ScreenManager, Screen
from utils import dump
from utils import Growl
from os.path import dirname
import mpd


import string
import random


__all__ = ('MpdClient', )

'''
Test using RecycleView instead of ListView...
'''
class MpdBrowser(Screen):

    def __init__(self, app, mpc, **kwargs):
        Logger.info("MpdBrowser: Init")        
        super(MpdBrowser, self).__init__(**kwargs)
        self.app = app
        
        # Setup mpd connection
        self.mpc = mpc

        Logger.info("MpdBrowser: Connected to MPD")        

        self.selection_history=[{'text':'/', 'index':0}];
        self.selection_last_item_index=0

        self.build()

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


    def do_selection(self, list):
        self.app.p(list)
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
                #print current_item['index'] * 80;

                self.list_view.scroll_to(index=current_item['index'])
                #self.list_view._scroll(current_item['index'] * 80)
                #self.list_view.populate(300)


                #self.list_view.populate()

                #list_view.adapter.select_data_item(di)
            except NameError:
                pass
        #Logger.info('MpdBrowser: Selection history: {}'.format(self.select


    def create_list(self, data):

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


    def create_recycleview(self, response):
        data = []
        x = 1; 
        for r in response:
            x+=1
            data.append({
                "index": x, 
                "viewclass": "MpdItem", 
                "mpd_name": r['text'], 
                "mpd_media": "http://rocketdock.com/images/screenshots/Aphex-Clock.png"
            })

        self.rv = RecycleView(
            width=800, 
            height=400, 
            data=data, 
            key_viewclass="viewclass", 
            key_size="height"
        )
        adapter = self.rv._get_adapter()

#       RecycleView doesn't support FREAKING SELECTIONS YET!! *Of course
#        adapter.bind(
#            on_selection_change=self.do_selection,
#            selection_mode="single"
#        )

        return self.rv
            

    def build(self):
        Builder.load_file(dirname(__file__) + '/mpdclient.kv')
        data = self.fetch_data("/")


        list_view = self.create_recycleview(data)
        self.add_widget(list_view)
        #self.app.p( self.rv._get_adapter() )
        #self.app.p(list_view)
        #self.app.sm.add_widget(list_view)
        return self


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
class MusicList(GridLayout):

    def __init__(self, **kwargs):

        kwargs['cols'] = 2
        super(MusicList, self).__init__(**kwargs)

        #self.mpd_client = mpd.MPDClient(use_unicode=True)
        self.mpd_client = mpd.MPDClient()
        self.mpd_client.connect("10.0.0.10", 6600)

        self.add_data()

    def add_data(self, item="/"):
        self.music_data = []

        print "Querying MPD listinfo for: {}".format(item)
        #for entry in self.mpd_client.lsinfo("/"):
        for entry in self.mpd_client.lsinfo(item):
            if 'directory' in entry:
                #print entry['directory']
                self.music_data.append({'text' : entry['directory']})

#        music_data = [{'text': 'Aphex Twin', 'is_selected' : False},
#            {'text': 'Bob Marley', 'is_selected' : False},
#            {'text': 'Pretty Lights', 'is_selected' : False},
#        ]

        list_item_args_converter = \
                lambda row_index, rec: {'text': rec['text'],
                                        'size_hint_y': None,
                                        'height': 45}
        
        #dict_adapter = DictAdapter(
        dict_adapter = ListAdapter(
                #sorted_keys=sorted(music_header.keys()),
                                   data=self.music_data,
                                   args_converter=list_item_args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   cls=ListItemButton)

        master_list_view = ListView(adapter=dict_adapter,
                                    size_hint=(.3, 1.0))

        dict_adapter.bind(on_selection_change=self.do_selection)

        self.add_widget(master_list_view)
        #return self
        
        #self.add_widget(detail_view)

    def do_selection(self, list):
        #dump(arg);
        #self.parent.app.p(event)
        #self.parent.app.p(args)
        #self.parent.app.p(kwargs)
        #item = list.get_data_item()
        #self.parent.app.p(list)
        #print list.selection['text']
        selection = list.selection[0]

        print selection.text
        #self.music_data = [{'text': 'Aphex Twin', 'is_selected' : False},
        #    {'text': 'Bob Marley', 'is_selected' : False},
        #    {'text': 'Pretty Lights', 'is_selected' : False},
        #]
        #for f in list.data:
        #    list.data.remove(f)
        #while list.data.count() > 0:
         #   list.data.pop()
        #dump(self)
        self.clear_widgets()

        #for f in list.data:
#                list.data.remove(f)

        #list.data.append({'text':'Blah', 'is_selected': False})
        #list.data.append({'text':'Foobar', 'is_selected': False})

        #self.populate()
        item = selection.text;

 #       self.add_data(item)

        data = []

        for entry in self.mpd_client.lsinfo(item):
            if 'directory' in entry:
                #print entry['directory']
                #data.append({'text' : entry['directory']})
                data.append(str(entry['directory']))
            if 'title' in entry:
                data.append(str(entry['title']))


        list_view = ListView(item_strings=data)
        self.add_widget(list_view)

#        self.item_strings = [str(index) for index in range(20)]

 #       list_view = ListView(item_strings=[str(index) for index in range(100)])

#        self.add_widget(list_view)

        #self.update_minimum_size()
        #list._trigger_reset_populate()
#        self.do_layout()


'''
