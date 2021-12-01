import threading
from ast import literal_eval
from multiprocessing import Queue
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext as st

import tkinter as tk
from tkinter.ttk import Progressbar, Style

from Utility.TestUtility import TestUtility


class TestProgress(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.start_button = tk.Button(master, text='Start', width=20, height=3, command=self.start_test)
        self.start_button.pack()
        self.start_button.place(x=500, y=400)

        self.cancel_button = tk.Button(master, text='Cancel', width=20, height=3, command=self.abort_test)
        self.cancel_button.pack()
        self.cancel_button.place(x=200, y=400)

        self.text_area = st.ScrolledText(master, wrap=tk.WORD, width=300, height=10, font=("Times New Roman", 15))

        # Placing cursor in the text area
        self.text_area.config(state=DISABLED)
        self.text_area.focus()
        self.text_area.pack()

        # s = Style()
        # s.theme_use("default")
        # s.configure("TProgressbar", thickness=50)
        self.progress = Progressbar(root, orient=HORIZONTAL,
                                    length=600, mode='determinate')
        self.progress.pack(ipady=10)

        self.shared_data= Queue()
        self.progress_status = Queue()
        self.end_flag = Queue()

        self.test_thread = threading.Thread(target=TestUtility.test,args=(self.shared_data,self.progress_status, self.end_flag))

        self.test_observer = threading.Thread(target=self.observer,args=(self.test_thread,))

    def observer(self,test_thread):
        i=1
        while self.end_flag.empty() and test_thread.is_alive():
            print('inside observer',i)
            i+=1
            if not self.progress_status.empty():
                data = self.progress_status.get()
                self.update_progress(data)
            if not self.shared_data.empty():
                data = self.shared_data.get()
                self.update_monitor(data)


    def start_test(self):
        if self.start_button['state'] == NORMAL:
            self.start_button['state'] = DISABLED
        if self.cancel_button['state'] == DISABLED:
            self.cancel_button['state'] =  NORMAL
        self.update_monitor('Initiate test environment... ')
        self.test_thread.start()
        self.test_observer.start()
        # self.thread_pool.start(self.test_runner)

    def abort_test(self):

        self.end_flag.put('test aborted')
        self.start_button['state'] = NORMAL
        self.cancel_button['state'] = DISABLED


    def update_monitor(self, data):
        self.text_area.config(state=NORMAL)
        self.text_area.insert(tk.INSERT, '\n'+data)
        self.text_area.config(state=DISABLED)

    def convert_to_hyper_text(self, data):
        dict_data = literal_eval(data)
        error = 'style="color:#FF0000;"'
        if dict_data['error']:
            info = '<a href="{}" {} >{}</a>'.format(dict_data['url'], error, dict_data['name'])
        else:
            info = '<a href="{}" >{}</a>'.format(dict_data['url'], dict_data['name'])
        self.text_area.insert(tk.INSERT, info)

    def update_progress(self, value):
        self.progress['value'] = int(value[0])


class TestProperties(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()


class Terminal(st.ScrolledText):
    def __init__(self, master, width=50, height=15, wrap="word"):
        super().__init__(master)
        self.grid(column=3, row=1, rowspan=12)


root = tk.Tk()
root.geometry("800x600")

tab_control = ttk.Notebook(root)
test_progress_tab = TestProgress(root)
tab_control.add(test_progress_tab, text='Progress')

test_progress_tab.mainloop()
