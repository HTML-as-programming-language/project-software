import sys
import time
import requests
from threading import Thread

from gui.gui_app import GUI

# create the application
from moduleview import ModuleView

myapp = GUI()

myapp.master.title("App")
myapp.master.protocol("WM_DELETE_WINDOW", lambda: myapp.master.destroy())

API = "http://127.0.0.1:8080"

def controller():
    views = {}

    r = requests.post(API + "/init", data='"http://127.0.0.1:8081"')
    if r.status_code is not 200:
        print("cannot init:", r.status_code)
        sys.exit(0)

    data = r.json()

    for m in data["modules"]:
        views[m["id"]] = ModuleView(m)

    myapp.update_modules(
        list(views.values())
    )

thread = Thread(target=controller)
thread.daemon = True
thread.start()

# start the program
myapp.mainloop()
sys.exit(0)
