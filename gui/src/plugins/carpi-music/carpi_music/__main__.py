if __name__ == '__main__':
    from kivy.app import App
    
    from main import CarPI_info
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.interactive import InteractiveLauncher

    class DemoApp(App):
        def build(self):
            
            root = ScreenManager()

            #info = CarPI_info().build()
            root.add_widget(CarPI_info().build())
            
            return root

    #app = DemoApp().run()
