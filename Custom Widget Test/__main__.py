from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '500')
Config.set('graphics', 'resizable', 0)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Ellipse, Line

Builder.load_file('hueLayout.kv')

class ColorLoopWidget(Widget):
    
    def on_touch_down(self, touch):
        with self.canvas:
            self.canvas.clear()
##            Color(1,1,1,1)
            d = 10
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d,d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

    

class HueLayout(Widget):
    colorloopwidget = ObjectProperty
    def clear_canvas(self):
        self.colorloopwidget.canvas.clear()
    

class HueApp(App):
    def build(self):
        return HueLayout()

if __name__ == '__main__':
    HueApp().run()
