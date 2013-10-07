from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse

class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 0) #rgb
            d = 30.
            # position specifies bottom left of the ellipse's bounding box
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d,d))

class MyPaintApp(App):
    def build(self):
        return MyPaintWidget()
if __name__ == '__main__':
    MyPaintApp().run()
