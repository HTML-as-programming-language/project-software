import logging
from threading import Thread, Event
from time import sleep
import random

from flask import Flask
from flask_appbuilder import SQLA, AppBuilder
from flask_socketio import SocketIO, emit
from app.index import MyIndexView


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, base_template='base.html', indexview=MyIndexView)
socketio = SocketIO(app)


thread = Thread()
thread_stop_event = Event()
class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()
    def randomNumberGenerator(self):
        # infinite loop of magical random numbers
        print("Making random numbers")
        while not thread_stop_event.isSet():
            number = round(random.random()*10, 3)
            print(number)
            socketio.emit('newnumber', {'number': number})
            sleep(self.delay)

    def run(self):
        self.randomNumberGenerator()


@socketio.on('my event')
def handle_message(message):
    print('\n\n\nreceived message: ', message, "\n\n\n\n")

@socketio.on('connect')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('\n\nClient connected\n\n')
    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("\n\nStarting Thread\n\n")
        thread = RandomThread()
        thread.start()


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""
