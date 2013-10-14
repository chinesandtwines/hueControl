from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '500')
Config.set('graphics', 'resizable', 0)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('hueLayout.kv')

class HueControl(Widget):
    pass

class HueLayout(Widget):
    pass


class HueApp(App):
    def build(self):
        return HueLayout()


if __name__ == '__main__':
    HueApp().run()
