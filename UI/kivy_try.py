import select
import threading
from functools import partial

from kivy.graphics import Color, Rectangle
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from CbsClasses.CbsPageUtility import CbsPageUtility
from database import DataBase
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.uix.recycleview import RecycleView
from kivy.uix.bubble import Bubble, BubbleButton

from kivy.config import Config
from MapPage.HePage.NewMainProcess import main
from multiprocessing import Pool, Queue
from kivy.core.text import LabelBase



class PageSelection(DropDown):
    pass

class MyMainApp(App):
    def build(self):
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        self.title  = r'CBS site test'
        self.icon = r'D:\Current\Selenium\NewAutomationEnv\Images\1200px-LOGO_LAMAS.jpg'
        self.f_layout = FlLayout()
        # Window.bind(on_request_close=self.__del__)

        return self.f_layout

    def print_terminal(self, text):
        self.f_layout.terminal.text = text


# class Scroll(RecycleView):
#     def __init__(self, **kwargs):
#         super(Scroll, self).__init__(**kwargs)
#         self.data = [{'text': str(x)} for x in range(30)]
#         # self.size = (Window.width, Window.height)
#         # self.size_hint = (1, None)

class FlLayout(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.2,0.2,0.2, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=(Window.width, Window.height),
                                  pos=self.pos)

        self.progress = Queue()
        self.pb = ProgressBar(max=1000, pos=(0, -200))
        self.pb.value = 0
        self.add_widget(self.pb)


        self.terminal = TextInput(focus=True, pos=(0, 230), size_hint=(.5, .6), background_color=(0.3,0.3,0.3, 1), readonly = True)
        self.terminal.font_name = "Arial"
        self.add_widget(self.terminal)


        self.start_btn = Button(text='Start', pos=(450, 150), size_hint=(.2, .1))
        self.cancel_btn = Button(text='Cancel', pos=(216, 150), size_hint=(.2, .1))
        self.start_btn.bind(on_press=partial(self.start_button_click, self.start_btn))
        self.cancel_btn.bind(on_press=partial(self.cancel_button_click, self.cancel_btn))
        self.add_widget(self.start_btn)
        self.add_widget(self.cancel_btn)

        self.right_layout = GridLayout(cols=1, spacing=30, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.right_layout.bind(minimum_height=self.right_layout.setter('height'))
        for i in range(100):
            grid = GridLayout(cols=2,spacing=2)
            cb = CheckBox(active=True)
            cb.add_widget(Label(text= '22222'))
            grid.add_widget(cb)
            # grid.add_widget(Label(text=str(i)))
            self.right_layout.add_widget(grid)
            # self.right_layout.add_widget(Label(text='Male'))
            # self.active = CheckBox(active=True)
            # self.right_layout.add_widget(self.active)



            # btn = Button(text=str(i), size_hint_y=None, height=40)
            # self.right_layout.add_widget(btn)
        #     size=(Window.width/4, Window.height/2)
        root = ScrollView(size_hint=(.5, .6), pos=(Window.width*0.5, Window.height*0.383) )
        root.add_widget(self.right_layout)
        self.add_widget(root)

        # self.progress_label = Label(text='0%', pos=(), size_hint=())

        Window.clearcolor = (1,1,1,0.5)
        LabelBase.register(name="Arial", fn_regular="Arial.ttf")

        # self.selection_box = RecycleView(pos =(450, 150),size_hint =(.5, .6), background_color=(0,0,0, 1))
        # self.add_widget(self.selection_box)

    def print_terminal(self, text):
        old_text = self.terminal.text + '\n'
        self.terminal.text = old_text + str(text)

    def clear_button_click(self, instance, event):
        self.terminal.text = ''
        self.terminal.remove_widget(self.bubble)

    def get_pages_to_choose(self):
        return CbsPageUtility.get_cbs_map_pages()

    def second_thread(self, shared_data:Queue, end_process:Queue):
        print('second thread enter')
        while True:
            if self.progress.qsize() >0:
                self.pb.value =  self.progress.get()*1000
            if shared_data.qsize() >0:
                self.print_terminal(shared_data.get())
            if end_process.qsize() >0:
                print('second thread exit')
                while end_process.qsize() >0:
                    shared_data.put(end_process.get())
                shared_data.put('exiting second process')
                break

    def main_thread(self, shared_data:Queue, progress:Queue, end_flag:Queue):
        try:
            main(shared_data, progress, end_flag)
        except Exception:
            end_flag.put('end for exception')
            progress.put(0.99*1000)
            if shared_data.qsize() >0:
                data = shared_data.get()
                self.print_terminal(data)
                print(data)
            else:
                print('shared data is empty')
        finally:
            self.start_btn.disabled = False


    def start_button_click(self, instance, value):
        self.start_btn.disabled = True
        print('start button clicked')
        self.print_terminal('start clicked')
        data = Queue()
        self.end_flag = Queue()
        threading.Thread(target=self.main_thread, args=(data, self.progress, self.end_flag)).start()
        threading.Thread(target=self.second_thread, args=(data,self.end_flag)).start()

    def cancel_button_click(self, instance, value):
        # print('cancel clicked')
        self.print_terminal('cancel clicked')
        self.end_flag.put('canceled')

if __name__ == "__main__":
    try:
        MyMainApp().run()
    except Exception:
        pass

 # # def onPressed_terminal(self, instance):
 #    #     self.print_terminal('right click')
 #    #     clear_button = BubbleButton(text='clear')
 #    #     clear_button.bind(on_press=partial(self.clear_button_click, clear_button))
 #    #     self.bubble = Bubble(arrow_pos='top_mid', orientation = 'vertical', size_hint = (.1,.1), pos=(300,230))
 #    #     self.bubble.add_widget(clear_button)
 #    #     self.terminal.add_widget(self.bubble)
 #
 #    import asyncio
 #    # from async_gui.engine import Task, MultiProcessTask
 #    # from async_gui.toolkits.kivy import KivyEngine
 #
 #    # from cpu_work import is_prime, PRIMES
 #    from kivy.graphics.context_instructions import Color
 #
 #    # engine = KivyEngine()
 #    from kivy.graphics.vertex_instructions import Rectangle