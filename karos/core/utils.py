import pprint

#from kivy.uix.label import Label
#from kivy.properties import ObjectProperty
#from kivy.clock import Clock

# Console color termcap codes
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def dump(arg):
    print "="*80, "\n", bcolors.BOLD, arg, bcolors.ENDC, "\n" + "="*80, bcolors.WARNING
    col_width = max(len(row) for row in dir(arg)) + 3
    for d in dir(arg):
        try:
            print d.ljust(col_width) + " : " + str(getattr(arg,d))
        except AttributeError:
            print "AttributeError: {} -- {}".format(d, d  )

    try:
        pprint.pprint(vars(arg))
    except TypeError:
        pass
    print bcolors.ENDC    

'''
class Growl(Label):

    text = ObjectProperty()
    #size=(300, 20)
    text_size=(300, None)
    close_after=5
    def __init__(self, app, **kwargs):
        # Center position...
        self.pos_hint={'center_x':.5, 'center_y':.5}
        super(Growl, self).__init__(**kwargs)

        # Automagically add ourself
        #app.container.add_widget(self)

        # And then remove ourself
        #Clock.schedule_once(lambda dt: app.container.remove_widget(self), self.close_after)
'''