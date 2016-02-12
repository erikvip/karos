from kivy.app import App
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.metrics import dp

from kivy.garden.navigationdrawer import NavigationDrawer

from kivy.lang import Builder


class NavigationPopout(NavigationDrawer):
    pass

class ExampleApp(App):

    def dump_geom(self, s, m, n):
        print "side_panel[w:{} h:{} x:{} y:{}] main_panel[w:{} h:{} x:{} y:{}] navigationdrawer[w:{} h:{} x:{} y:{}]".format(
            s.width, s.height, s.x, s.y,
            m.width, m.height, m.x, m.y,
            n.width, n.height, n.x, n.y )

    def build(self):


        navigationdrawer = NavigationDrawer()

        top_panel = BoxLayout(orientation='vertical')
        top_panel.add_widget(Label(text='Panel label'))
        top_panel.add_widget(Button(text='A button'))
        top_panel.add_widget(Button(text='Another button'))
        navigationdrawer.add_widget(top_panel)
        navigationdrawer.anim_type = 'slide_above_simple'
        main_panel = FloatLayout()
        navigationdrawer.add_widget(main_panel)

        button = Button(text='toggle NavigationDrawer state (animate)',
                        size_hint=(0.2, 0.2), pos_hint={'x':0.5, 'y':0.5})
        button.bind(on_press=lambda j: navigationdrawer.toggle_state())

        button2 = Button(text='dump stuff', 
                        size_hint=(0.2, 0.2), pos_hint={'x':0.3, 'y':0.3})
        button2.bind(on_press=lambda z: self.dump_geom(top_panel, main_panel, navigationdrawer))

        main_panel.add_widget(button)
        main_panel.add_widget(button2)
        return navigationdrawer
'''
        label_head = (
            '[b]Example label filling main panel[/b]\n\n[color=ff0000](p'
            'ull from left to right!)[/color]\n\nIn this example, the le'
            'ft panel is a simple boxlayout menu, and this main panel is'
            ' a BoxLayout with a label and example image.\n\nSeveral pre'
            'set layouts are available (see buttons below), but users ma'
            'y edit every parameter for much more customisation.')
        main_panel = BoxLayout(orientation='vertical')
        label_bl = BoxLayout(orientation='horizontal')
        label = Label(text=label_head, font_size='15sp',
                      markup=True, valign='top')
        label_bl.add_widget(Widget(size_hint_x=None, width=dp(10)))
        label_bl.add_widget(label)
        label_bl.add_widget(Widget(size_hint_x=None, width=dp(10)))
        main_panel.add_widget(Widget(size_hint_y=None, height=dp(10)))
        main_panel.add_widget(label_bl)
        main_panel.add_widget(Widget(size_hint_y=None, height=dp(10)))
        main_panel.add_widget(Image(source='red_pixel.png', allow_stretch=True,
                                    keep_ratio=False, size_hint_y=0.2))
        navigationdrawer.add_widget(main_panel)
        label.bind(size=label.setter('text_size'))
'''
#        def set_anim_type(name):
#            navigationdrawer.anim_type = name

        
'''        
        modes_layout = BoxLayout(orientation='horizontal')
        modes_layout.add_widget(Label(text='preset\nanims:'))
        slide_an = Button(text='slide_\nabove_\nanim')
        slide_an.bind(on_press=lambda j: set_anim_type('slide_above_anim'))
        slide_sim = Button(text='slide_\nabove_\nsimple')
        slide_sim.bind(on_press=lambda j: set_anim_type('slide_above_simple'))
        fade_in_button = Button(text='fade_in')
        fade_in_button.bind(on_press=lambda j: set_anim_type('fade_in'))
        reveal_button = Button(text='reveal_\nbelow_\nanim')
        reveal_button.bind(on_press=
                           lambda j: set_anim_type('reveal_below_anim'))
        slide_button = Button(text='reveal_\nbelow_\nsimple')
        slide_button.bind(on_press=
                          lambda j: set_anim_type('reveal_below_simple'))
        modes_layout.add_widget(slide_an)
        modes_layout.add_widget(slide_sim)
        modes_layout.add_widget(fade_in_button)
        modes_layout.add_widget(reveal_button)
        modes_layout.add_widget(slide_button)
        main_panel.add_widget(modes_layout)

        button = Button(text='toggle NavigationDrawer state (animate)',
                        size_hint_y=0.2)
        button.bind(on_press=lambda j: navigationdrawer.toggle_state())
        button2 = Button(text='toggle NavigationDrawer state (jump)',
                         size_hint_y=0.2)
        button2.bind(on_press=lambda j: navigationdrawer.toggle_state(False))
        button3 = Button(text='toggle _main_above', size_hint_y=0.2)
        button3.bind(on_press=navigationdrawer.toggle_main_above)
        main_panel.add_widget(button)
        main_panel.add_widget(button2)
        main_panel.add_widget(button3)
'''
#        return navigationdrawer

ExampleApp().run()
