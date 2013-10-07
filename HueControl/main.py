from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

# define the Base Class of our Kivy App
class MyApp(App):
    # initialize and return Root Widget in build(self)
    def build(self):
        # Label will be the Root Widget of this App
        return Label(text='Hello World')

if __name__ == '__main__':
    MyApp().run()

