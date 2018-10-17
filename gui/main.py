from tkinter import *

from widgets.module_widget import ModuleWidget
from widgets.modules_list import ModulesList


class App(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.modules_list = ModulesList(self)
        self.module_widget = ModuleWidget(self)

        self.modules_list.pack(side=LEFT, fill=Y)
        self.module_widget.pack(side=RIGHT, fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)


# create the application
myapp = App()

myapp.master.title("App")

# start the program
myapp.mainloop()
