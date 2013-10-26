from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '500')
Config.set('graphics', 'resizable', 0)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty,\
     ReferenceListProperty
from kivy.graphics import Color, Ellipse, Line
from random import randint
from kivy.animation import Animation

Builder.load_file('hueLayout.kv')

class DataPoint(Widget):
    pass

class ColorLoopWidget(Widget):
    xlabel = ObjectProperty
    ylabel = ObjectProperty
##    def on_touch_down(self, touch):
##        with self.canvas:
##            self.canvas.clear()
##            d = 10
##            if touch.x < 500:
##                Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d,d))
##                touch.ud['line'] = Line(points=(touch.x, touch.y))
##                self.xlabel.text = 'x: '+str(touch.x)
##                self.ylabel.text = 'y: '+str(touch.y)

class HueLayout(Widget):
    colorloopwidget = ObjectProperty()
    xlabel = ObjectProperty()
    ylabel = ObjectProperty()
    pt1_x = ObjectProperty()
    pt1_y = ObjectProperty()
    pt1 = ObjectProperty()
    
    def clear_canvas(self):
        self.xlabel.text = value
        self.colorloopwidget.canvas.clear()

    def x1_adj(self, instance, value):
        x = value
        y = self.pt1.pos[1]
        self.pt1.pos = x, y
        self.xlabel.text = 'x: ' + str(round(x,2))

    def y1_adj(self, instance, value):
        x = self.pt1.pos[0]
        y = value
        self.pt1.pos = x, y
        self.ylabel.text = 'y: ' + str(round(y,2))

    

class HueApp(App):
    def build(self):
        return HueLayout()

if __name__ == '__main__':
    HueApp().run()
