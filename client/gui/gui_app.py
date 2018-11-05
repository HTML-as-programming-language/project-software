from tkinter import *

from gui.widgets.module_widget import ModuleWidget
from gui.widgets.modules_list import ModulesList


class GUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.modules_list = ModulesList(self, self.on_module_select)
        self.module_widget = ModuleWidget(self)

        self.modules_list.pack(side=LEFT, fill=Y)
        self.module_widget.pack(side=RIGHT, fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)

    def on_module_select(self, module):
        self.module_widget.show_module(module)

    def update_modules(self, modules):
        self.modules_list.update_list(modules)

    def add_module(self, module):
        self.modules_list.add(module)

    def remove_module(self, module_id):
        self.modules_list.remove(module_id)

    def show_connection_error(self, msg=""):
        win = Toplevel()
        win.wm_title("Error")

        l = Label(win, text="Error connecting to server")
        l.grid(row=0, column=0)

        l2 = Label(win, text=msg)
        l2.grid(row=1, column=0)

        b = Button(win, text="Quit", command=self.quit)
        b.grid(row=3, column=0)

