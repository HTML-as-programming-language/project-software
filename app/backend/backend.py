import glob
from backend.client import Client
from multiprocessing import Queue
from queue import Empty
from time import sleep

class Backend:
    #clients = {}

    def __init__(self):
        self.clients = {}
        self.client_stop_queue = Queue()

    def __check_new_clients(self):
        ports = glob.glob('/dev/ttyACM[0-9]*')

        for port in ports:
            if port not in self.clients:
                try:
                    c = Client(port, quit=self.client_stop_queue)
                    c.port = port
                except Exception as e:
                    print("Could not add client:", port, e)
                    continue

                self.clients[port] = c
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


if __name__ == "__main__":
    b = Backend()

    while True:
        b.client_maintenance()
        sleep(1)

        for _, c in b.clients.items():
            c.set_threshold_open_temperature(80)
            c.open_hatch()
