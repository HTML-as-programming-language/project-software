import glob
from multiprocessing import Queue
from queue import Empty
from time import sleep
import sys
from serial.serialutil import SerialException
from client import Client

class Backend:
    #clients = {}

    def __init__(self):
        self.clients = {}
        self.client_stop_queue = Queue()

    def __check_new_clients(self):
        ports = []
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/ttyACM*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError("Unsupported platform(?)")

        for port in ports:
            name = port.replace("/", "")

            if name not in self.clients:
                try:
                    c = Client(port, quit=self.client_stop_queue)
                    c.port = port
                except SerialException as e:
                    # print("Could not add client:", port, e)
                    continue


                self.clients[name] = c
                print("Added client:", port)
        
        # TODO: Cleanup disconnected/inactive clients.
        # Give Clients a queue to send a message to when they finish.

    def __check_quit_queue(self):
        while True:
            try:
                port = self.client_stop_queue.get(block=False)
                if port is None:
                    break
                del self.clients[port]
                print("Removed client:", port)
            except Empty:
                break

    def client_maintenance(self):
        self.__check_quit_queue()
        self.__check_new_clients()
