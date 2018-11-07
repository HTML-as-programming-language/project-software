import glob
from multiprocessing import Queue
from queue import Empty
from time import sleep
import sys
from serial.serialutil import SerialException
from client import Client

import api


class Backend:
    #clients = {}

    def __init__(self, state_change_queue):
        self.clients = {}
        self.client_stop_queue = Queue()
        self.client_state_change_queue = state_change_queue

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
                    c = Client(
                            name,
                            port,
                            quit=self.client_stop_queue,
                            state_change=self.client_state_change_queue)
                    c.port = port
                except SerialException as e:
                    # print("Could not add client:", port, e)
                    continue

                self.clients[name] = c
                        
    def __check_quit_queue(self):
        while True:
            try:
                port = self.client_stop_queue.get(block=False)
                if port is None:
                    break
                if port in self.clients:
                    name = self.clients[port].name
                    del self.clients[port]
                    print("Removed client:", port)


                    api.send_request("/module/" + name + "/delete")
                    print("Informed api clients of removed module")

            except Empty:
                break

    def client_maintenance(self):
        self.__check_quit_queue()
        self.__check_new_clients()
