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

    modules = []
    for name, client in b.clients.items():
        modules.append(Module(
            name, data={"light": "30%"},
            actions={
                "open": client.open_hatch,
                "close": client.close_hatch,
            }
        ))
        print(name, client)

    myapp.update_modules(
        modules,
    )


Thread(target=test).start()

# start the program
myapp.mainloop()
