import random
from time import sleep
from datetime import datetime

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

import json
import requests
from threading import Thread, Event

app = Flask(__name__)
socketio = SocketIO(app, manage_session=False)



###################
##    ROUTES     ##
###################

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/<path:path>')
def recourse(path):
    return send_from_directory('templates', path)



###################
##    SOCKETS    ##
###################

update_thread = Thread()
update_thread_stop_event = Event()

connected_clients = {}

history = {"example": [("time1", 10),("time2", 5),("time3", 2),("time4", 20)]}
history_index = None


@socketio.on('iWantHistory')
def i_want_history(arg):
    global history_index
    history_index = arg


@socketio.on('iDontWantHistory')
def i_dont_want_history(arg):
    global history_index
    history_index = None


@socketio.on('request')
def handle_message(message):
    requests.post('http://localhost:8080/'+str(message["path"]), json=message["body"])


@socketio.on('connect')
def test_connect(*args):
    socketio.emit('init', json.loads(requests.post('http://localhost:8080/init', json="http://localhost:8081/api/update_me").text ))
    print(" >>> INIT")
    global update_thread
    print('\n\nClient connected\n\n')

    if not update_thread.isAlive():
        update_thread = updateThread()
        update_thread.start()


@app.route('/api/update_me/<path:path>', methods=['post'])
def backend_callback(path):
    data = json.loads(requests.post('http://localhost:8080/init', json="http://localhost:8081/api/update_me").text)
    socketio.emit('update', data)  # TEMPORARILY
    print(" >>> UPDATE")
    for module in data:
        # module["devttyACM0"]
        new_data = []
        for sensor in module["sensors"]:
            new_data.append(sensor["data"].val)

    # print("\n\n"+str(path)+"\n\n")
    return "bedankt voor uw donatie"


class updateThread(Thread):
    def __init__(self):
        self.delay = 1
        super(updateThread, self).__init__()

    def init(self):
        while not update_thread_stop_event.isSet():
            n = str(round(random.random()*10, 3))
            if history_index is not None:
                socketio.emit('v', n)
                print(" >>> historyUpdate")
                sleep(self.delay)

    def run(self):
        self.init()


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8081)