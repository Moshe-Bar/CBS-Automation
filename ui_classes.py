from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        login = LogInScreen()
        login.name = 'login'
        main_window = MainWindow()
        main_window.name = 'main'
        screens = [login, main_window]
        for screen in screens:
            self.add_widget(screen)
        self.current = 'login'


class LogInScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        login_label = Label(text="Log in")
        self.login_button = Button(label=login_label)


class MainWindow(Screen):
    pass


class MainApp(App):
    def build(self):
        screen_manager = WindowManager()
        return screen_manager
        # return


if __name__ == "__main__":
    MainApp().run()
