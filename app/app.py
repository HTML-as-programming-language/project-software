import time
from threading import Thread

from backend.backend import Backend
from gui.gui_app import GUI

# create the application
from module import Module

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
