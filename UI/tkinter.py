# import tkinter as tk
import  tkinter as tk


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
       

    def create_widgets(self):
        self.StartTest_button  = tk.Button(self)
        self.StartTest_button["text"] = "Start Test"
        self.StartTest_button["command"] = self.MapSiteTest
        self.StartTest_button.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def MapSiteTest(self):
        print("test is starting!")
       


root = tk.Tk()
app = MainWindow(master=root)
app.mainloop()
