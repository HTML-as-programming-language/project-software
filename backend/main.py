from backend import Backend
from time import sleep
import threading

import api

b = Backend()

def client_maintenance():
    while True:
        b.client_maintenance()
        sleep(1)

maintenance_thread = threading.Thread(target=client_maintenance)
maintenance_thread.daemon = True
maintenance_thread.start()

api.set_backend(b)

api.app.run(
    debug=True,
    port=8080,
)
