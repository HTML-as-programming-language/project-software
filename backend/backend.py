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

    def __init__(self):
        self.clients = {}
        self.client_stop_queue = Queue()
        self.client_state_change_queue = Queue()

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
                print("Added client:", port)
                api.send_request("/module/" + name + "/add", api.format_module(name, c))
                print("Informed api clients of added module")
        
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
    def __handle_state_changes(self):
        while True:
            try:
                change = self.client_state_change_queue.get(block=False)
                if change is None:
                    break
                url = "/module/"
                if change.sensor_id is not None:    
                    url += "/sensor/" + change.sensor_id + "/dataitem/" + change.data_item
                else:
                    url += "/dataitem/" + change.data_item

                api.send_request(url, change.value)
                print("Informed api clients of modified state", url, change.value)
            except Empty:
                break

    def client_maintenance(self):
        self.__check_quit_queue()
        self.__check_new_clients()
        self.__handle_state_changes()
