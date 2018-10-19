import time
from threading import Thread

from backend.backend import Backend
from gui.gui_app import GUI
from backend.client import SensorType

# create the application
from moduleview import ModuleView

myapp = GUI()

myapp.master.title("App")


def test():
    b = Backend()
    views = {}

    while True:
        time.sleep(1)
        b.client_maintenance()

        delete = [client for client in views.keys() if client not in b.clients.values()]
        for client in delete:
            del views[client]

        for name, client in b.clients.items():
            if client not in views:
                views[client] = ModuleView(client)

        myapp.update_modules(
            list(views.values())
        )


Thread(target=test).start()

# start the program
myapp.mainloop()
