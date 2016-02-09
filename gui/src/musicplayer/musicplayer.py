#from ../util import dump

from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView, ListItemButton, ListItemLabel
from kivy.adapters.dictadapter import DictAdapter
from kivy.adapters.listadapter import ListAdapter

from kivy.uix.screenmanager import ScreenManager, Screen
from utils import dump
import mpd

__all__ = ('MusicPlayerScreen', )

class MusicPlayerScreen(Screen):
    def __init__(self, app, **kwargs):
        super(MusicPlayerScreen, self).__init__(**kwargs)    
        self.app = app

        adapter = ListAdapter(
                                   data=[str(index) for index in range(100)],
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   cls=ListItemButton)        
        list_view = ListView(adapter=adapter)
        adapter.bind(on_selection_change=self.do_selection)        
#        self.add_widget(list_view)

        #print "Attempting dump"
        #dump(list_view)

    def do_selection(self, list):
        print "Selected: {}".format(list.selection[0].text)
        #dump(list)


#    def build(self):
#        return MusicList().build()

class MusicList(GridLayout):

    def __init__(self, **kwargs):

        kwargs['cols'] = 2
        super(MusicList, self).__init__(**kwargs)

        self.mpd_client = mpd.MPDClient(use_unicode=True)
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
                                        'height': 25}
        
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
