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

        self.shown_module = None

    def on_module_select(self, module):
        print(module)
        self.module_widget.show_module(module)
        self.shown_module = module.module["id"]

    def update_modules(self, modules):
        self.modules_list.update_list(modules)

    def add_module(self, module):
        self.modules_list.add(module)

    def remove_module(self, module_id):
        self.modules_list.remove(module_id)

    def change_module_sensor_dataitem(self, module_id, sensor_id, key, value):
        m = self.modules_list.change_sensor_dataitem(module_id, sensor_id, key, value)

        #print("yes or not:", m and self.shown_module == m.module["id"], self.shown_module, m.module["id"])
        if m and self.shown_module == m.module["id"]:
            self.module_widget.update_module_data(m)

    def change_module_dataitem(self, module_id, key, value):
        m = self.modules_list.change_dataitem(module_id, key, value)

        #print("yes or not:", m and self.shown_module == m.module["id"], self.shown_module, m.module["id"])
        if m and self.shown_module == m.module["id"]:
            self.module_widget.update_module_data(m)

    def show_connection_error(self, msg=""):
        win = Toplevel()
        win.wm_title("Error")

        l = Label(win, text="Error connecting to server")
        l.grid(row=0, column=0)

        l2 = Label(win, text=msg)
        l2.grid(row=1, column=0)

        b = Button(win, text="Quit", command=self.quit)
        b.grid(row=3, column=0)

