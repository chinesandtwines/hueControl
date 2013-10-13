from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '300')
Config.set('graphics', 'resizable', 0)
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.switch import Switch

Builder.load_file('hueLayout.kv')

class hueLayout(BoxLayout):
    pwr1_switch = ObjectProperty()

    def callback(instance, value):
        print 'instance: ', instance
        print 'value: ', value

class HueController(App):
    def build(self):
        #self._app_window_size = 5, 20
        return hueLayout()

if __name__ == '__main__':
    
    Config.write()
    HueController().run()
