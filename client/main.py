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

port = 8081
backendhost = "http://127.0.0.1:8080/"
myhost = "http://127.0.0.1:" + str(port) + "/"

if len(sys.argv) >= 2:
    port = sys.argv[1]

if len(sys.argv) >= 3:
    backendhost = sys.argv[2]

if len(sys.argv) >= 4:
    myhost = sys.argv[3]

print("CONFIG:")
print("\tListening on port:", port, ". You can specify the port as an argument.")
print("\tUsing backend on:", backendhost, ". You can specify it as the second argument.")
print("\tTelling backend we're:", myhost, ". You can specify the port as the third argument.")

b = backend.Backend(backendhost, myapp.show_connection_error)
backend.instance = b


def controller():
    views = {}

    r = b.init(myhost)
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
        host="0.0.0.0"
        port=port)

threadserv = Thread(target=webserver)
threadserv.daemon = True
threadserv.start()

# start the program
myapp.mainloop()
sys.exit(0)
