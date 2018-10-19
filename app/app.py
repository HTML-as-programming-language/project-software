import sys
import time
from threading import Thread

from backend.backend import Backend
from gui.gui_app import GUI

# create the application
from moduleview import ModuleView

myapp = GUI()

myapp.master.title("App")
myapp.master.protocol("WM_DELETE_WINDOW", lambda: myapp.master.destroy())


def controller():
    b = Backend()
    views = {}

    while True:
        time.sleep(1)
        b.client_maintenance()

        delete = [client for client in views.keys() if client not in b.clients.values()]
        for client in delete:
            del views[client]

        for name, client in b.clients.items():
            if client not in views and client.initialized:
                views[client] = ModuleView(client)

        myapp.update_modules(
            list(views.values())
        )


thread = Thread(target=controller)
thread.daemon = True
thread.start()

# start the program
myapp.mainloop()
sys.exit(0)
