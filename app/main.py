import random
from time import sleep, time
from datetime import datetime

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

import json
import requests
from threading import Thread, Event

from pprint import pprint

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

history = {"example": [("time1", 10), ("time2", 5), ("time3", 2), ("time4", 20)]}
history_index = None


@socketio.on('iWantHistory')
def i_want_history(arg):
    global history_index
    history_index = arg
    socketio.emit('historyInit', {"names": ["Timestamp", "Temperature", "Light thresholds"] ,"data" : history[history_index]})


@socketio.on('iDontWantHistory')
def i_dont_want_history():
    global history_index
    history_index = None


@socketio.on('request')
def handle_message(message):
    requests.post('http://localhost:8080/'+str(message["path"]), json=message["body"])


@socketio.on('connect')
def test_connect():
    try:
        data = json.loads(requests.post('http://localhost:8080/init', json="http://localhost:8081/api/update_me").text)
        socketio.emit('init', data)
        print(" >>> INIT")
        pprint(data)
        if len(data["modules"]) > 0:
            update_history(data)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("\n\n\n We hebben de Centrale niet kunnen vinden op het address http://localhost:8080/init \n\n\n")

    global update_thread
    if not update_thread.isAlive():
        update_thread = updateThread()
        update_thread.start()


@app.route('/api/update_me/<path:path>', methods=['post'])
def backend_callback(path):
    data = json.loads(requests.post('http://localhost:8080/init', json="http://localhost:8081/api/update_me").text)
    socketio.emit('update', data)  # TEMPORARILY
    print(" >>> UPDATE")
    update_history(data)
    # print("\n\n"+str(path)+"\n\n") # TODO: v2
    return "bedankt voor uw donatie"


class updateThread(Thread):
    def __init__(self):
        self.delay = 1
        super(updateThread, self).__init__()

    def init(self):
        while not update_thread_stop_event.isSet():
            if history_index in history.keys():
                last_history = list(history[str(history_index)][-1])
                last_history[0] = int(time())
                socketio.emit('historyUpdate', last_history)
                print(" >>> historyUpdate")
                sleep(self.delay)
                pprint(history)

    def run(self):
        self.init()


def update_history(data):
    new_data = [int(time())]
    for sensor in data["modules"][0]["sensors"]:
        # pprint(list(sensor["data"].values())[1])
        new_data.append(list(sensor["data"].values())[1])

    if data["modules"][0]["id"] not in history.keys():
        history[data["modules"][0]["id"]] = []

    history[data["modules"][0]["id"]].append(tuple(new_data))


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8081)
    # app.run(debug=True, port=8081)