'''
 This script just loads random characters into a ListView. 

 On the raspberry pi, when gpu_mem was set to 64MB, the ListView would crap out after 72 items.
 You could still see the items in the list, and the empty space in the List was present, but the text
 lables were not there...increasing gpu_mem fixed the issue.  You can use this script to test.

 This is set to 500 (see the **for index in range(N)** below).  If you cannot scroll to the bottom
 of this list, then you'll want to increase your gpu_mem setting in /boot/config.txt (Raspberry PI)
'''
from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListView, ListItemButton, ListItemLabel
import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class MainView(GridLayout):
    '''Implementation of a simple list view with 100 items.
    '''

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(MainView, self).__init__(**kwargs)

#        list_view = ListView(item_strings=[str(index) for index in range(100)])
        data = []
        for index in range(500):
            n = int(random.choice([str(i) for i in range(8, 30)]));
            data.append({'text':id_generator(size=n)})

        list_item_args_converter = \
                lambda row_index, rec: {'text': rec['text'],
                                        'size_hint_y': None,
                                        'height': 80}

        adapter = ListAdapter(
                                   data=data,
                                   args_converter=list_item_args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   cls=ListItemButton)

        #list_view = ListView(adapter=adapter)

        adapter.bind(on_selection_change=self.do_selection)                
        list_view = ListView(adapter=adapter, size_hint_x=1)

        self.add_widget(list_view)
    def do_selection(self, item):
        print "Selected: {}".format(item)


if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MainView(width=800))
