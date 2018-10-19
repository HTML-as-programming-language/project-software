import time
from threading import Thread
from tkinter import *

from backend.backend import Backend
from gui.widgets.module_widget import ModuleWidget
from gui.widgets.modules_list import ModulesList
from module import Module


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


# create the application
myapp = GUI()

myapp.master.title("App")


def test():
    time.sleep(1)
    b = Backend()
    b.client_maintenance()
    for name, client in b.clients.items():
        print(name, client)

    myapp.update_modules([
        Module(
            "harry", data={"light": "30%"},
            actions={
                "naar boven": lambda: print("doe iets!?!?!"),
                "doe iets anders": lambda: print("doe iets anders!?!?!")
            }
        ),
        Module(
            "test", data={"temp.": "20°C"},
            actions={
                "doe iets": lambda: print("doe iets!?!?!"),
                "doe iets anders": lambda: print("doe iets anders!?!?!")
            }

        ),
        Module(
            "henk", data={"temp.": "30°C"},
            actions={
                "doe iets": lambda: print("doe iets!?!?!"),
                "doe iets anders": lambda: print("doe iets anders!?!?!")
            },
            config={
                "temp0": Module.ConfigItem(
                    "Min. and max. temperature",
                    Module.ConfigItem.Type.MIN_MAX
                ),
                "temp1": Module.ConfigItem(
                    "Something else?!?!?!",
                    Module.ConfigItem.Type.MIN_MAX
                ),
                "temp2": Module.ConfigItem(
                    "Something..",
                    Module.ConfigItem.Type.ONE_VALUE
                ),
            }
        )
    ])


Thread(target=test).start()

# start the program
myapp.mainloop()

