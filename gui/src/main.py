from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image

from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
#get_center_x, get_top, get_right(), .height
class PluginIcon(Image):
    name = ObjectProperty()
    x = NumericProperty()
    y = NumericProperty()
    def on_press(args):
        #from pudb import set_trace; set_trace()
        print "Pressed {}".format(args)
    def wtf():
        return "wtf"

class MainViewport(ScrollView):
    def __init__(self, **kwargs):
        super(MainViewport, self).__init__(**kwargs)

        #layout = GridLayout(cols=1, padding=10, spacing=10)

        #self.previous_text = open(self.kv_file).read()
        #parser = Parser(content=self.previous_text)
        #widget = Factory.get(parser.root.name)()
        #Builder._apply_rule(widget, parser.root, parser.root)
        #layout.add_widget(Button(text='Hello 1'))
        #layout.add_widget(Button(text='Hello 2'))

#        self.add_widget(layout)
      #self.add_widget(widget)

    def touch(args):
        print "Touch event: {}".format(args)    

class CarPiApp(App):
    def build(self):
        return MainViewport()


if __name__ == '__main__':
    CarPiApp().run()