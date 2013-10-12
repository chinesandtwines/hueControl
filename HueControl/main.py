from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

#kivy.require('1.7.2')

class PageLayout(Widget):
    pass

class TestApp(App):
    PageLayout()

if __name__ == '__main__':
    TestApp().run()

