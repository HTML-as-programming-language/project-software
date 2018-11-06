from backend import Backend
from time import sleep
import threading
import queue

import api

state_change_queue = queue.Queue()

b = Backend(state_change_queue)

def client_maintenance():
    while True:
        b.client_maintenance()
        sleep(1)

maintenance_thread = threading.Thread(target=client_maintenance)
maintenance_thread.start()

api.set_backend(b)

api_thread = threading.Thread(target=api.handler)
api_thread.start()

def handle_state_change():
    while True:
        change = state_change_queue.get()

        url = "/module/" + change.module_id
        if change.sensor_id is not None:    
            url += "/sensor/" + change.sensor_id + "/dataitem/" + change.data_item
        else:
            url += "/dataitem/" + change.data_item

        count = api.send_request(url, change.value)
        print("Informed api clients of modified state", url, change.value, count)

thread2 = threading.Thread(target=handle_state_change)
thread2.start()

api.app.run(
    debug=True,
    port=8080,
)
