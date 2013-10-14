from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse


class ColorLoopWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1,1,1,1)
            d = 10
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d,d))


class ColorLoopApp(App):
    def build(self):
        return ColorLoopWidget()


if __name__ == '__main__':
    ColorLoopApp().run()
