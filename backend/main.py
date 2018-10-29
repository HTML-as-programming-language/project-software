from backend import Backend
from time import sleep

import api

b = Backend()


#while True:
b.client_maintenance()
sleep(1)

for _, c in b.clients.items():
    c.set_threshold_open_temperature(80)
    c.open_hatch()

api.app.run(debug=True, port=8080)
