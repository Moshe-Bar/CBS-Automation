from kivy.app import App
from kivy.uix.button import Button


class MyWindow(App):
    def build(self):
        return Button(text='my button')


MyWindow().run()