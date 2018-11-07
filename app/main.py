from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from time import sleep
import random

app = Flask(__name__)
socketio = SocketIO(app)

socketio_thread = Thread()
socketio_thread_stop_event = Event()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def recourse(path):
    return send_from_directory('templates', path)



class RandomThread(Thread):
    def __init__(self):
        self.delay = 10
        super(RandomThread, self).__init__()

    def init(self):
        while not socketio_thread_stop_event.isSet():
            number = round(random.random()*10, 3)
            socketio.emit('init', "nice")
            sleep(self.delay)

    def run(self):
        self.init()


@socketio.on('my event')
def handle_message(message):
    print('\n\n\nreceived message: ', message, "\n\n\n\n")


@socketio.on('connect')
def test_connect():
    socketio.emit('init', """
{"modules": [
    {"data":{"hatch_status":8,"labelHatch open":"8%"},
    "id":"devttyACM0",
    "label":"/dev/ttyACM0",
    "sensors":[{"data":{"label":"16C","temp":16},
    "id":"0",
    "label":"Temperature",
    "settings":[{"id":"temp_threshold","label":"Temperature thresholds","max":30,"min":0,"subtype":"minmax","type":"int"}],"type":"TEMP"}]}
]}""")

    # need visibility of the global thread object
    global socketio_thread
    print('\n\nClient connected\n\n')
    # Start the random number generator thread only if the thread has not been started before.
    if not socketio_thread.isAlive():
        print("\n\nStarting Thread\n\n")
        socketio_thread = RandomThread()
        socketio_thread.start()


if __name__ == '__main__':
    app.run(debug=True, port=8081)