from backend import Backend
from time import sleep
import threading
import queue
import sys

import api
from constants import SPAM_DEBUG

state_change_queue = queue.Queue()

b = Backend(state_change_queue)


def client_maintenance():
    while True:
        b.client_maintenance()
        sleep(1)


maintenance_thread = threading.Thread(target=client_maintenance)
maintenance_thread.start()

api.set_backend(b)

api_thread = threading.Thread(target=api.handler_api_clients)
api_thread.start()


def handle_state_change():
    while True:
        change = state_change_queue.get()

        url = "/module/" + change.module_id
        if change.new is not None:
            url += "/add"
            print(change.value.name)
            change.value = api.format_module(change.value.name, change.value)
            print(change.value)
        elif change.sensor_id is not None:
            url += ("/sensor/" + change.sensor_id + "/dataitem/"
            + change.data_item)
        else:
            url += "/dataitem/" + change.data_item

        count = api.send_request(url, change.value)
        if SPAM_DEBUG:
            print("Informed api clients of modified state", url,
                    change.value, ". Clients count:", count)


thread2 = threading.Thread(target=handle_state_change)
thread2.start()

thread3 = threading.Thread(target=handle_state_change)
thread3.start()

thread4 = threading.Thread(target=handle_state_change)
thread4.start()

print("MAIN!", __name__)

port = 8080

if len(sys.argv) >= 2:
    port = sys.argv[1]

print("Listening on port:", port, ". You can specify the port as an argument.")

api.app.run(
    # debug=True,
    host="0.0.0.0",
    port=port,
)
