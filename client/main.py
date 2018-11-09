import sys
from threading import Thread

import backend

from gui.gui_app import GUI

# create the application
from moduleview import ModuleView

import api

myapp = GUI()

myapp.master.title("App")
myapp.master.protocol("WM_DELETE_WINDOW", lambda: myapp.master.destroy())

API = "http://127.0.0.1:8080"

b = backend.Backend(API, myapp.show_connection_error)
backend.instance = b


def controller():
    views = {}

    r = b.init()
    if r is None:
        return

    data = r.json()
    print(data)

    for m in data["modules"]:
        views[m["id"]] = ModuleView(m)

    myapp.update_modules(
        list(views.values())
    )


thread = Thread(target=controller)
thread.daemon = True
thread.start()

api.set_app(myapp)


def webserver():
    api.app.run(
        debug=False,
        port=8081)


threadserv = Thread(target=webserver)
threadserv.daemon = True
threadserv.start()

# start the program
myapp.mainloop()
sys.exit(0)
