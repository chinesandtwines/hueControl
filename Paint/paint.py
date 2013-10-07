from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
# Line accepts list of 2D point coordinates
# i.e. (x1, y1, x2, y2, ...)

class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 0) #rgb
            d = 30.
            # position specifies bottom left of the ellipse's bounding box
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d,d))
            #touch.ud is a Python dict that stores custom attributes for touch
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

class MyPaintApp(App):
    def build(self):
        return MyPaintWidget()
if __name__ == '__main__':
    MyPaintApp().run()
