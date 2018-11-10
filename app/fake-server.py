import json
from pprint import pprint

api_str = """ {"modules":[{"data":{"automatic":"True","distance":_,"hatch_status":_,"labelAutomatic":"True","labelDistance":"__cm","labelHatch open":"___%"},"id":"devttyACM0","label":"/dev/ttyACM0","sensors":[{"data":{"label":"_C","temp":_},"id":"0","label":"Temperature","settings":[{  "id":"temp_threshold","label":"Temperature thresholds","max":30,"min":0,"subtype":"minmax","type":"int"}],"type":"TEMP"},{"data":{"label":"36%","light":36},"id":"1","label":"Light","settings":[{"id":"light_threshold","label":"Light thresholds","max":100,"min":0,"subtype":"minmax","type":"int"}],"type":"LIGHT"}]}]}"""

import random
from time import sleep, time

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

import requests
from threading import Thread, Event


app = Flask(__name__)
socketio = SocketIO(app, manage_session=False)



########################
##    FAKE ROUTES     ##
########################

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/<path:path>')
def recourse(path):
    return send_from_directory('templates', path)



########################
##    FAKE SOCKETS    ##
########################

update_thread = Thread()
update_thread_stop_event = Event()

history = {"devttyACM0": [(time(), 10, 0), (time(), 5), (time(), 2), (time(), 20)]}


@socketio.on('iWantHistory')
def i_want_history(arg):
    socketio.emit('historyInit', {"names": ["Timestamp", "Temperature", "Light"] ,"data" : history["devttyACM0"]})


@socketio.on('iDontWantHistory')
def i_dont_want_history():
    i_want_history()


@socketio.on('request')
def handle_message(message):
    pprint(message)


@socketio.on('connect')
def test_connect():
    socketio.emit('init', json.loads(api_str.replace("_", str(random.randint(0, 10)))))

    global update_thread
    if not update_thread.isAlive():
        update_thread = updateThread()
        update_thread.start()


class updateThread(Thread):
    def __init__(self):
        self.delay = 1
        super(updateThread, self).__init__()

    def init(self):
        while not update_thread_stop_event.isSet():
            socketio.emit('historyUpdate', [time(), random.randint(0, 10), random.randint(0, 10)])
            socketio.emit('update', json.loads(api_str.replace("_", str(random.randint(0, 10)))))
            sleep(self.delay)

    def run(self):
        self.init()


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8081)
