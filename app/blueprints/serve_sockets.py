import json
import random
from time import sleep

import requests
from flask_socketio import SocketIO
from threading import Thread, Event

from app.main import app


socketio = SocketIO(app)

update_thread = Thread()
update_thread_stop_event = Event()

# history_update_thread = Thread()
# history_update_thread_stop_event = Event()

connected_clients = {}

history = {}


@socketio.on('iWantHistory')
def i_want_history(arg):
    socketio.emit('historyUpdate', history[arg])


@socketio.on('iDontWantHistory')
def i_dont_want_history(arg):
    socketio.emit('historyUpdate', history[arg])


@socketio.on('request')
def handle_message(message):
    requests.post('http://localhost:8080/'+str(message["path"]), json=message["body"])
    # print("\n\n\n")
    # print(type(message), message)
    # print("\n\n\n")


@socketio.on('connect')
def test_connect(socket):
    socketio.emit('init', json.loads(requests.post('http://localhost:8080/init', json="http://localhost:8081/api/update_me").text ))
    # global update_thread
    print('\n\nClient connected\n\n')

    # if not update_thread.isAlive():
    #     update_thread = updateThread()
    #     update_thread.start()


@app.route('/api/update_me/<path:path>', methods=['post'])
def backend_callback(path):
    socketio.emit('update', json.loads(requests.post('http://localhost:8080/init', json="http://localhost:8081/api/update_me").text ))  # TEMPORARILY
    print("\n\n"+str(path)+"\n\n")
    return "bedankt voor uw donatie"


# class updateThread(Thread):
#     def __init__(self):
#         self.delay = 1
#         super(updateThread, self).__init__()
#
#     def init(self):
#         while not update_thread_stop_event.isSet():
#             n = str(round(random.random()*10, 3))
#             socketio.emit('update', json.loads('{"modules": [{"data":{"hatch_status":'+n+',"labelHatch open":"'+n+'%"}, "id":"devttyACM0", "label":"/dev/ttyACM0", "sensors":[{"data":{"label":"'+n+'C","temp":'+n+'}, "id":"0", "label":"Temperature", "settings":[{"id":"temp_threshold","label":"Temperature thresholds","max":'+n+',"min":0,"subtype":"minmax","type":"int"}],"type":"TEMP"}]}]}'))
#             sleep(self.delay)
#
#     def run(self):
#         self.init()