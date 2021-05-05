import threading
from functools import partial

from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.text import Label as CoreLabel

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label

from Testing.CbsPageUtility import CbsPageUtility

from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar

from Testing.TestUtility import TestUtility
# from UI.NewMainProcess import main
from multiprocessing import Queue
from kivy.core.text import LabelBase



class PageSelection(DropDown):
    pass

class MyMainApp(App):
    def build(self):
        # Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

        self.title  = r'CBS Site Test'
        self.icon = r'D:\Current\Selenium\NewAutomationEnv\Images\1200px-LOGO_LAMAS.jpg'
        self.f_layout = FlLayout()
        # Window.bind(on_request_close=self.__del__)

        return self.f_layout



# class Scroll(RecycleView):
#     def __init__(self, **kwargs):
#         super(Scroll, self).__init__(**kwargs)
#         self.data = [{'text': str(x)} for x in range(30)]
#         # self.size = (Window.width, Window.height)
#         # self.size_hint = (1, None)

class FlLayout(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('kivy_try.kv')
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
        # self.right_layout.bind(minimum_height=self.right_layout.setter('height'))
        # grid = GridLayout(cols=2, spacing=2, rows=None)
        for i in range(10):
            cb = CheckBox(active=True)
            cb.add_widget(Label(text= '22222'))
            self.right_layout.add_widget(CheckBox(), index=i)
            # grid.add_widget(Label(text=str(i)))
        # self.right_layout.add_widget(grid)
            # self.right_layout.add_widget(Label(text='Male'))
            # self.active = CheckBox(active=True)
            # self.right_layout.add_widget(self.active)

        self.new_progress = CircularProgressBar()
        self.add_widget(self.new_progress)


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
                # self.new_progress.set_value(self.progress.get()*100)
            if shared_data.qsize() >0:
                self.print_terminal(shared_data.get())
            if end_process.qsize() >0:
                print('second thread exit')
                temp = end_process.get()
                shared_data.put(temp)
                end_process.put(temp)
                shared_data.put('exiting second process')
                break

    def main_thread(self, shared_data:Queue, progress:Queue, end_flag:Queue, pages=None):
        try:
            print('start test')
            TestUtility.test(shared_data=shared_data, progress_status=progress, end_flag=end_flag,pages=pages)
            print('after test')
        except Exception:
            print(Exception)
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
        self.end_flag.put('canceled')

class CircularProgressBar(ProgressBar):

    def __init__(self, **kwargs):
        # Builder.load_file('kivy_try.kv')
        super(CircularProgressBar, self).__init__(**kwargs)

        # Set constant for the bar thickness
        self.thickness = 40

        # Create a direct text representation
        self.label = CoreLabel(text="0%", font_size=self.thickness)

        # Initialise the texture_size variable
        self.texture_size = None

        # Refresh the text
        self.refresh_text()

        # Redraw on innit
        self.draw()

    def draw(self):
        with self.canvas:
            # Empty canvas instructions
            self.canvas.clear()

            # Draw no-progress circle
            Color(0.26, 0.26, 0.26)
            Ellipse(pos=self.pos, size=self.size)

            # Draw progress circle, small hack if there is no progress (angle_end = 0 results in full progress)
            Color(1, 0, 0)
            Ellipse(pos=self.pos, size=self.size,
                    angle_end=(0.001 if self.value_normalized == 0 else self.value_normalized * 360))

            # Draw the inner circle (colour should be equal to the background)
            Color(0, 0, 0)
            Ellipse(pos=(self.pos[0] + self.thickness / 2, self.pos[1] + self.thickness / 2),
                    size=(self.size[0] - self.thickness, self.size[1] - self.thickness))

            # Center and draw the progress text
            Color(1, 1, 1, 1)
            # added pos[0]and pos[1] for centralizing label text whenever pos_hint is set
            Rectangle(texture=self.label.texture, size=self.texture_size,
                      pos=(self.size[0] / 2 - self.texture_size[0] / 2 + self.pos[0],
                           self.size[1] / 2 - self.texture_size[1] / 2 + self.pos[1]))

    def refresh_text(self):
        # Render the label
        self.label.refresh()

        # Set the texture size each refresh
        self.texture_size = list(self.label.texture.size)

    def set_value(self, value):
        # Update the progress bar value
        self.value = value

        # Update textual value and refresh the texture
        self.label.text = str(int(self.value_normalized * 100)) + "%"
        self.refresh_text()

        # Draw all the elements
        self.draw()


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