import time
from threading import Thread

from backend.backend import Backend
from gui.gui_app import GUI
from backend.client import SensorType

# create the application
from module import Module

myapp = GUI()

myapp.master.title("App")


def test():
    b = Backend()

    while True:
        time.sleep(1)
        # TODO: Find a way to do client_maintanance (maybe own thread)
        # and add/remove modules if arduino's were added/removed.
        b.client_maintenance()

        modules = []
        for name, client in b.clients.items():
            d = {}
            if SensorType.TEMP in client.supported_sensors:
                print("YO DIT IS MIJN CURRENT TEMP", client.current_temp)
                d["Current Temperature"] = f"{client.current_temp}°C"
            if SensorType.LIGHT in client.supported_sensors:
                d["Light level"] = f"{client.current_light}%"
            modules.append(Module(
                name, d,
                actions={
                    "open": client.open_hatch,
                    "close": client.close_hatch,
                },
                config={
                    "temp0": Module.ConfigItem(
                        "Min. and max. temperature",
                        Module.ConfigItem.Type.MIN_MAX),
                    "temp1": Module.ConfigItem(
                        "Something else?!?!?!",
                        Module.ConfigItem.Type.MIN_MAX),
                    "temp2": Module.ConfigItem(
                        "Something..",
                        Module.ConfigItem.Type.ONE_VALUE),
                }
            ))
            print(name, client)

        myapp.update_modules(
            modules,
        )


Thread(target=test).start()

# start the program
myapp.mainloop()
